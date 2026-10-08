---
title: "Touch Grass, Pack Your Docs: An Offline Coding Agent on a 4 GB Laptop GPU"
published: false
description: "Gemma 4 E4B, llama.cpp and opencode on a GTX 1650 Ti with the network off. Thinking, a tuned agent profile and a reference doc attached to the request take the same task from zero passes to four of four."
tags: devchallenge, hf26challenge, gemma, opencode
cover_image: https://raw.githubusercontent.com/xbill9/dev-hacktoberfest/main/article/devto-cover.53468eac.jpg
---

*Built for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05) on dev.to.*

This article provides a step-by-step build of an offline coding agent on a laptop with a 4 GB GPU, from the first context sweep to the setup that passes. Gemma 4 runs locally under llama.cpp, opencode drives it, and an independent grader scores every run.

https://github.com/xbill9/dev-hacktoberfest

**Gemma 4 E4B on a GTX 1650 Ti writes working code offline when it has three things: thinking on, an agent profile that keeps the requirements in front of it, and the reference material attached to the request. With all three it passed 4 of 4 runs in 3 to 6.5 minutes. Every other combination tested passed 0 of 16.**

---

## What I Built

A coding agent that goes outside with you. The laptop leaves the desk, the network stays behind, and the agent still works: model, server, agent and documentation all live on the machine.

It is for anyone who wants to take a laptop to a park bench, a campsite or a train with no signal and keep building. The rule it is built around is the one hikers already follow: you carry what you need. Offline, the model cannot look anything up, so the documents you pack decide whether the agent produces working code.

The whole stack is open: Google's open-weight Gemma 4, an exact Q4_0 rebuild of its QAT checkpoint published on Hugging Face, llama.cpp for inference and opencode as the agent.

---

## Demo

One command runs the agent on a task with a reference document attached. The task asks for NOAA sunrise and sunset times plus pytest tests, then for the tests to pass:

```bash
./touchgrass-agent.sh run "$(cat bench/agent_task.txt)" docs/NOAA_SOLAR.md
```

The benchmark runner does the same thing headless and then checks the result two ways, with the agent's own tests and with a separate grader the agent never sees:

```plaintext
gemma-4-e4b-attach-1 rc=0 wall=178s tools={('write', 'completed'): 2, ('bash', 'completed'): 1} own_tests='1 passed in 0.00s' grader='GRADER 3/3'
```

Three tool calls: write the module, write the tests, run pytest. The grader checks London, New York and Sydney against the astral library and accepts each time within 10 minutes. The output of every run is in [`bench/runs/`](https://github.com/xbill9/dev-hacktoberfest/tree/main/bench/runs).

---

## Code

Everything is in [xbill9/dev-hacktoberfest](https://github.com/xbill9/dev-hacktoberfest): the wrapper script, the benchmark runners, the grader, and the raw event stream of every opencode run next to the code the agent wrote, in [`bench/runs/`](https://github.com/xbill9/dev-hacktoberfest/tree/main/bench/runs). The first passing run is [`agent-attach/gemma-4-e4b-attach-1.jsonl`](https://github.com/xbill9/dev-hacktoberfest/blob/main/bench/runs/agent-attach/gemma-4-e4b-attach-1.jsonl).

---

## How I Built It

#### At This Point You Should Have…

- A machine with an NVIDIA GPU. This one is a GTX 1650 Ti Max-Q with 4096 MiB, an Intel Core i7-10750H and 15 GiB of RAM.
- llama.cpp built with CUDA. These runs used commit `fc343a8`.
- opencode 1.18.35, run once while still online, because it downloads its provider package on first use.
- The model: [xbill9/gemma-4-E4B-it-qat-q4_0-exact-gguf](https://huggingface.co/xbill9/gemma-4-E4B-it-qat-q4_0-exact-gguf).

---

#### Step 1 — Fit the Model and the Context on 4 GB

Gemma 4 E4B keeps its 1.59 GB per-layer embedding table in host memory through mmap, so only 2.43 GiB of the GGUF has to sit on the card. The rest of the budget goes to context. `ctx_sweep.sh` starts the server at each context size and fills 90% of the window with a real prompt:

```bash
bench/ctx_sweep.sh e4b ~/models/gemma-4-E4B-it-qat-q4_0-exact/gemma-4-E4B-it-q4_0-exact.gguf 8192 16384 32768 65536
```

```plaintext
e4b ctx=8192 vram_idle=2853MiB vram_after=2857MiB prompt_tok=7194 prefill=153 t/s (46.9s) decode=34.6 t/s
e4b ctx=16384 vram_idle=2989MiB vram_after=2993MiB prompt_tok=14567 prefill=140 t/s (103.7s) decode=32.1 t/s
e4b ctx=32768 vram_idle=3261MiB vram_after=3265MiB prompt_tok=29313 prefill=121 t/s (241.9s) decode=27.8 t/s
e4b ctx=65536 LOAD_FAIL ... cudaMalloc failed: out of memory
```

| Context | E2B VRAM | E2B decode | E4B VRAM | E4B decode |
|---|---|---|---|---|
| 8k | 1485 MiB | 68.9 t/s | 2853 MiB | 34.6 t/s |
| 16k | 1541 MiB | 62.6 t/s | 2989 MiB | 32.1 t/s |
| 32k | 1653 MiB | 55.9 t/s | 3261 MiB | 27.8 t/s |
| 64k | 1877 MiB | 44.7 t/s | out of memory | — |

Sliding-window attention keeps the KV cache small, so E4B runs at 32k with room to spare and stops at 64k. Prompt processing speed sets the pace: a cold 29k-token prompt takes four minutes on E4B. Everything below runs at 32k.

---

#### Step 2 — Give the Agent One Task and an Independent Grader

The task is the same for every run, in [`bench/agent_task.txt`](https://github.com/xbill9/dev-hacktoberfest/blob/main/bench/agent_task.txt): write `daylight.py` with `sun_times(lat, lon, date)` using the NOAA sunrise equation and the standard library only, write pytest tests that put London's sunrise on 2026-06-21 between 03:35 and 03:55 UTC and sunset between 20:10 and 20:30, then run the tests until they pass.

An agent's own tests can be made to pass by changing the tests, so a run counts only when [`grade.py`](https://github.com/xbill9/dev-hacktoberfest/blob/main/bench/grade.py) agrees. It imports the agent's function and checks three cities on three dates against reference times from astral, within 10 minutes each.

The agent can edit files and run `python3` or `pytest`, and every other shell command is denied:

```json
"permission": {
  "edit": "allow",
  "webfetch": "deny",
  "bash": { "*": "deny", "python3 *": "allow", "pytest *": "allow" }
}
```

---

#### Step 3 — Run the Agent with Default Settings

Default settings mean the server as a chat demo runs it, with thinking off, and opencode as installed. Both E2B GGUFs ran three times each and E4B once:

```plaintext
gemma-4-e2b-google-rvb1 ... own_tests='2 passed in 0.01s' grader='GRADER ERROR NotImplementedError: Only specific test case implemented due to complexity of NOAA equation without external libraries.'
gemma-4-e2b-rvb1 ... own_tests='2 passed in 0.00s' grader='GRADER 0/3'
```

Seven runs, zero passes, and in most of them the agent's own tests passed. The code shows how. One run hard-coded London and raised an error for every other input. Another returned 06:00 and 18:00 for every place on Earth, under tests that only checked the results were dates in 2026.

In four of the six E2B runs the model handed the whole job to opencode's `task` subagent, which works from a prompt the model writes for it. In the 06:00 run that prompt left out the acceptance windows, and the subagent never saw them.

The other failure is the `edit` tool, which replaces a string only when the model quotes the existing text exactly. E4B without thinking failed 10 of its 11 edits with `Could not find oldString in the file`, and one E2B run failed 7 of 7.

---

#### Step 4 — Tune the Agent

Three changes, all on the E4B server at 32k:

1. **Thinking on** (`--reasoning on`).
2. **The `task` subagent off**, so the requirements stay in the conversation that does the work.
3. **An [`AGENTS.md`](https://github.com/xbill9/dev-hacktoberfest/blob/main/bench/AGENTS.md)** in the work directory: put the acceptance criteria in the tests exactly as given, never loosen a test to make it pass, never hard-code expected outputs.

```json
{
  "permission": { "task": "deny" },
  "agent": { "build": { "tools": { "skill": false, "task": false } } }
}
```

With thinking on, 3 of 5 edits landed in the first tuned run. The rules did not hold every time: the second run still special-cased London (`if lat == 51.5 and lon == -0.13 ...`). The grader passed neither run, and the first run's code shows the deeper problem:

```python
# Solar declination (delta)
delta = 23.45 * math.asin(math.sin(L) * math.cos(math.pi / 180.0))
```

The structure is right: declination, hour angle, solar noon, a longitude correction. The formulas are invented. The model does not reproduce the NOAA equations from memory, and offline there is nowhere to look them up.

---

#### Step 5 — Pack the Docs

[`docs/NOAA_SOLAR.md`](https://github.com/xbill9/dev-hacktoberfest/blob/main/bench/docs/NOAA_SOLAR.md) is one page of equations with no code: fractional year, equation of time, declination, hour angle and the sunrise and sunset minutes. Implemented directly, it matches astral within 2 minutes for all three cities.

Placed in the repository with a line in `AGENTS.md` pointing to it, the document went unread. The run's one `read` call opened its own `daylight.py`, and the grader failed it.

Attached to the request with `-f`, it is in the context from the first turn:

```bash
opencode run -m llamacpp/gemma-4-e4b "$(cat agent_task.txt)" -f docs/NOAA_SOLAR.md
```

```plaintext
gemma-4-e4b-attach-1 rc=0 wall=178s  ... own_tests='1 passed in 0.00s' grader='GRADER 3/3'
gemma-4-e4b-attach-2 rc=0 wall=393s  ... own_tests='1 passed in 0.00s' grader='GRADER 3/3'
gemma-4-e4b-attach-3 rc=0 wall=218s  ... own_tests='1 passed in 0.00s' grader='GRADER 3/3'
gemma-4-e4b-attach2-1 rc=0 wall=316s ... own_tests='1 failed, 1 passed in 0.02s' grader='GRADER 3/3'
```

Four of four. All four kept the acceptance windows in their tests and none special-cased London. The fourth run also wrote an extra test that expects a sunset at 80°N on the solstice, when the sun never sets there; its code correctly returns none, so that test fails and the grader still passes the code. The passing runs were also faster than any failing E4B run, because the model stopped cycling through edits and test failures.

---

#### Step 6 — The Smaller E2B, and the Repack Against Google's GGUF

The same E2B task ran on Google's QAT GGUF and on the exact Q4_0 repack, three runs each, with identical server flags:

| E2B, default settings | Google QAT GGUF | Exact Q4_0 repack |
|---|---|---|
| VRAM at 32k | 1771 MiB | **1653 MiB** |
| Decode, mean of 3 runs | 61.5 t/s | **65.3 t/s** |
| Grader passes | 0/3 | 0/3 |

The repack uses 118 MiB less memory and decodes 6% faster. E2B decodes at twice E4B's speed, and with the reference attached it still passed none of six runs: one got two cities of three, one got one, and four broke on syntax or on a function that does not exist (`calendar.dayofyear`). Across those six runs E2B landed 3 of its 12 edits, so its first bug is usually its last.

---

#### 🔎 Tip: `opencode run` Waits on Standard Input

Started from a script whose standard input is an open pipe, `opencode run` stops after `init` and never sends a request. Give it `< /dev/null`.

---

#### 🔎 Tip: opencode Loads Your Claude Code Skills

opencode reads skills from `~/.claude/skills` and lists them in its system prompt. Measured on a cold server with the request `Reply with exactly: pong`:

```plaintext
default profile, Claude skills imported: 11434 tokens, cold prefill 44.4 s on E2B
tuned profile, skill and task tools off: 6565 tokens, cold prefill 23.3 s on E2B
```

On a small GPU that is half the wait on every new session. Set tools per agent, under `agent.build.tools`: a top-level `tools` key does not reach the agent, and `edit: false` turns off `write` as well.

---

#### 🔎 Tip: Write Docs a Small Model Can Paste

A small model copies a reference literally. A formula written across three lines without enclosing parentheses became `IndentationError` in all three E2B runs; E4B rewrote the same lines as valid Python. Wrap multi-line expressions in parentheses and give units at every step.

---

#### Compare and Contrast

| Setup | Model | Grader passes | Wall time |
|---|---|---|---|
| 🥇 Thinking + tuned profile + doc attached | E4B | 4 of 4 | 178–393 s |
| Thinking + tuned profile + doc in the repo | E4B | 0 of 1 | 433 s |
| Thinking + tuned profile | E4B | 0 of 2 | 565–1116 s |
| Default settings | E4B | 0 of 1 | 711 s |
| Thinking + tuned profile + doc attached | E2B | 0 of 6 | 137–313 s |
| Default settings | E2B, both GGUFs | 0 of 6 | 88–334 s |

---

#### So, Which One?

E4B, the exact Q4_0 repack, at 32k with thinking on, opencode with the `task` and `skill` tools off, an `AGENTS.md` of rules, and the reference material attached to the request. [`touchgrass-agent.sh`](https://github.com/xbill9/dev-hacktoberfest/blob/main/touchgrass-agent.sh) wraps it: `serve` starts llama-server, `run` takes a task and any number of documents to attach, and `tui` opens opencode interactively.

Keep the server running between tasks: llama-server reuses the cached prompt prefix, so only the first request of a session pays the cold prefill.

---

## Why Does Open Innovation Matter?

This build exists only because every layer is open. A closed API needs a network, and the point of the project is to work where there is none.

Open weights made the model small enough to fit. Google published the QAT checkpoint, and an exact Q4_0 rebuild of it runs E4B at 32k on a 4 GB laptop card, with the per-layer embeddings left in system memory. Open inference let me read the server's logs to the token, which is where every number in this article comes from. An open agent let me see what it sends, so its 11434-token prompt became 6565 and the subagent that dropped requirements could be switched off.

Each failure in Steps 3 to 5 was diagnosed from a log, a config file or a source line. With a closed stack, each would have been a support ticket.

---

#### Summary

The goal of this article was to build a coding agent that works offline on a 4 GB laptop GPU. The key to the solution was attaching the reference material to the request, on top of thinking and an agent profile that keeps the requirements in view. The agent results were:

- 🟢 E4B with thinking, the tuned profile and the doc attached passed 4 of 4 runs, in 178 to 393 seconds.
- 🟢 E4B fits a 32k context in 3261 MiB of a 4096 MiB card.
- 🟢 The exact E2B repack used 118 MiB less VRAM and decoded 6% faster than Google's GGUF.
- ❌ Every other combination passed 0 of 16, including E2B with the doc attached.
- ❌ Without the formulas in context, E4B invents them.
- ⚠️ A document left in the repository went unread; attach it.
- ⚠️ `AGENTS.md` rules reduce test gaming without ending it: one of two tuned runs still special-cased London.
- ⚠️ opencode imports Claude Code skills into its prompt; turning off the `skill` tool cut 11434 tokens to 6565.

Scope: one laptop (GTX 1650 Ti Max-Q, 4096 MiB, i7-10750H, 15 GiB RAM), one task, llama.cpp `fc343a8` and opencode 1.18.35, 20 graded runs. Most conditions ran one to three times, so the counts show which setups work at all and are too small to rank close ones. Thinking, the profile and `AGENTS.md` changed together in Step 4 and were not tested separately, and the first tuned run still had the `skill` tool on. Default-settings runs had thinking off; all others had it on. The three `attach` runs per model used [`NOAA_SOLAR.v1.md`](https://github.com/xbill9/dev-hacktoberfest/blob/main/bench/docs/NOAA_SOLAR.v1.md), which has no parentheses around the multi-line declination formula; the fourth E4B run and the three `attach2` E2B runs used the parenthesised version linked in Step 5. All three E2B syntax failures came from `NOAA_SOLAR.v1.md`. Gemma 4 12B and Claude Code against the same server were not run.

The strategy for building an offline coding agent with Gemma 4 on a 4 GB laptop GPU was validated with an incremental step by step approach.

---

#### References

* [dev-hacktoberfest | GitHub](https://github.com/xbill9/dev-hacktoberfest)
* [gemma-4-E4B-it-qat-q4_0-exact-gguf | Hugging Face](https://huggingface.co/xbill9/gemma-4-E4B-it-qat-q4_0-exact-gguf)
* [gemma-4-E2B-it-qat-q4_0-exact-gguf | Hugging Face](https://huggingface.co/xbill9/gemma-4-E2B-it-qat-q4_0-exact-gguf)
* [llama.cpp | GitHub](https://github.com/ggml-org/llama.cpp)
* [opencode](https://opencode.ai)
* [General Solar Position Calculations | NOAA Global Monitoring Laboratory](https://gml.noaa.gov/grad/solcalc/solareqns.PDF)
* [astral | PyPI](https://pypi.org/project/astral/)
* [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass | dev.to](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)
