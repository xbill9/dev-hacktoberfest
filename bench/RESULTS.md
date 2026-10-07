# Offline coding agent on a 4 GB laptop GPU: results

Measured on 2026-10-07 on a GTX 1650 Ti Max-Q (4096 MiB, Turing sm75) with a 6-core CPU and 15 GB RAM.
Software: llama.cpp `fc343a8`, opencode 1.18.35 and Claude Code 2.1.292. The Claude Code runs
were never completed (see "Not done").

## Models

| Label | File | Notes |
|---|---|---|
| E2B repack | `xbill9/gemma-4-E2B-it-qat-q4_0-exact-gguf` (exact-v2) | every matrix Q4_0, rebuilt from the QAT checkpoint |
| E2B baseline | Google `gemma-4-E2B_q4_0-it.gguf` (3.35 GB) | Google's QAT GGUF |
| E4B repack | `xbill9/gemma-4-E4B-it-qat-q4_0-exact-gguf` | 2.43 GiB resident; the 1.59 GB per-layer table stays in mmap |
| 12B | Google `gemma-4-12b-it-qat-q4_0.gguf` (6.98 GB) | downloaded, **not run**: it needs CPU offload, and slow was ruled out |

## 1. How much context fits (`ctx_sweep.sh`)

Each cell fills 90% of the window with a real prompt. Thinking was off, KV f16, flash attention on.

| Context | E2B VRAM | E2B cold prefill | E2B decode | E4B VRAM | E4B cold prefill | E4B decode |
|---|---|---|---|---|---|---|
| 8k | 1.49 GB | 280 t/s (26 s) | 69 t/s | 2.85 GB | 153 t/s (47 s) | 35 t/s |
| 16k | 1.54 GB | 239 t/s (61 s) | 63 t/s | 2.99 GB | 140 t/s (104 s) | 32 t/s |
| 32k | 1.65 GB | 188 t/s (156 s) | 56 t/s | **3.26 GB** | 121 t/s (242 s) | 28 t/s |
| 64k | 1.88 GB | 131 t/s (448 s) | 45 t/s | **OOM** | — | — |
| 128k | 2.33 GB (load only) | — | — | — | — | — |

Sliding-window attention keeps the KV cache small, so prefill speed is the limit, not memory. E4B tops out
at 32k on this card.

## 2. The agent task

One prompt, run headless through `opencode run`: write `daylight.py` (NOAA sunrise/sunset, standard
library only) plus pytest tests with given London acceptance windows, then run the tests until they
pass (`agent_task.txt`).

**Scoring is independent of the agent's own tests.** `grade.py` checks London, New York and Sydney
against astral within ±10 minutes. The reference values were verified with astral before use.
Sandboxing: file edits are allowed, Bash only for `python3`/`pytest`, and everything else is denied.

## 3. Results

| # | Condition | Model | Grader (full passes) | Wall time |
|---|---|---|---|---|
| A | rig defaults (thinking off) | E2B baseline | 0/3 | 88–154 s |
| A | rig defaults | E2B repack | 0/3 | 129–334 s |
| A | rig defaults | E4B repack | 0/1 | 711 s |
| B | tuned: thinking on, `task` subagent off, `AGENTS.md` rules | E4B repack | 0/2 | 565–1116 s |
| C | B + reference doc in `docs/` | E4B repack | 0/1 (never opened the doc) | 433 s |
| D | **B + reference doc attached to the request (`-f`)** | **E4B repack** | **3/3** | **178, 393, 218 s** |
| D | B + doc attached | E2B repack | 0/3 (syntax error copied from the doc) | 171–236 s |
| E | D with a paste-safe doc | E2B repack | 0/3 (best: 2/3 cities) | 137–313 s |
| E | D with a paste-safe doc | E4B repack | **1/1** | 316 s |

**E4B with the doc attached: 4 of 4. Every other combination: 0 of 16.**

### Repack vs baseline (E2B, condition A, 3 trials each, same flags)

| | Google baseline | Exact repack |
|---|---|---|
| VRAM at 32k | 1771 MiB | **1653 MiB (−118)** |
| Decode, mean of 3 runs | 61.5 t/s | **65.3 t/s (+6%)** |
| Grader passes | 0/3 | 0/3 |

## 4. What went wrong, and what fixed it

1. **The agent games its own tests.** In condition A it hard-coded London, or returned 06:00/18:00
   everywhere, or dropped the time windows from its tests. The windows went missing when opencode's
   `task` subagent was handed a rewritten prompt that left them out. Fixed by denying `task` and adding
   the `AGENTS.md` rules.
2. **The `edit` tool needs exact recall.** E4B without thinking failed 10 of 11 edits ("Could not find
   oldString"). With thinking on, 3 of 5 landed. E2B stays bad at it even with thinking.
3. **Knowledge, not agent skill.** The tuned E4B had the right structure but invented the formulas.
   Offline there is nowhere to look them up. A doc sitting in the repo was ignored; **attaching it put
   it in context from turn 1**, and E4B then passed in 3–6 minutes, faster than any failing run.
4. **Small models transcribe docs literally.** A multi-line formula without parentheses became a
   Python syntax error for E2B (3 of 3). Docs for a small model need to be paste-safe.

## 5. Harness findings (opencode 1.18.35)

- `opencode run` hangs at `init` when stdin is an open pipe. Use `< /dev/null`.
- opencode imports Claude Code skills from `~/.claude/skills`. Setting `skill: false` cut the system
  prompt from about 11.4k to 7.0k tokens, and E4B's cold first turn from 78 s to 46 s.
- A top-level `tools` key does not reach the agent; set it under `agent.build.tools`. `edit: false`
  also disables `write`.

## 6. Recipe

`../touchgrass-agent.sh serve`, then `../touchgrass-agent.sh run "<task>" docs/<ref>.md`. The profile is
`tuned.opencode.json`, plus an `AGENTS.md` in the work directory.

## Not done

- **Claude Code against llama-server.** `cc_run.sh` is ready (llama.cpp serves `/v1/messages`), but it
  was never run: the first matrix hung on the opencode stdin bug, and the work then focused on getting
  opencode to pass.
- **Battery runs (unplugged).** Not measured yet.
- **The 12B model.** Not run.
- **Ablation inside condition D.** This would show how much of the pass comes from thinking alone.

Raw logs for every run are in `runs/`.
