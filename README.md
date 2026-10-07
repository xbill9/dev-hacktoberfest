# dev-hacktoberfest: an offline coding agent on a 4 GB laptop GPU

Entry for the [Hacktoberfest Open-Source AI Challenge, Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05).

**Article:** [Touch Grass, Pack Your Docs: An Offline Coding Agent on a 4 GB Laptop GPU](https://dev.to/xbill/touch-grass-pack-your-docs-an-offline-coding-agent-on-a-4-gb-laptop-gpu-4lf1)

**Touch grass, but pack your docs.** This repo takes a coding agent outdoors, away from the desk and
off the network. Everything runs on a laptop: Gemma 4 E4B on a GTX 1650 Ti (4 GB), served by
llama.cpp and driven by opencode. No API key, no network, and nothing leaves the machine.

## What works

Across 20 headless agent runs on one task (write NOAA sunrise/sunset code plus tests, then make the tests
pass), with every result checked by an independent grader:

| Setup | Full passes |
|---|---|
| **E4B exact Q4_0 + thinking on + tuned opencode + reference doc attached to the request** | **4 of 4** (3–6.5 min each) |
| Every other combination (E2B, thinking off, no doc, doc left in the repo) | 0 of 16 |

The small model has the structure right, but offline it cannot look anything up, so without the
equations it invents them. Attach the reference and it writes correct code in a few minutes. The full
tables, failure analysis and harness findings are in [`bench/RESULTS.md`](bench/RESULTS.md).

## Run it

You need [llama.cpp](https://github.com/ggml-org/llama.cpp) built with CUDA, [opencode](https://opencode.ai),
and the model:
[`xbill9/gemma-4-E4B-it-qat-q4_0-exact-gguf`](https://huggingface.co/xbill9/gemma-4-E4B-it-qat-q4_0-exact-gguf)
(an exact Q4_0 rebuild of Google's QAT checkpoint, Apache 2.0).

Edit the paths at the top of [`touchgrass-agent.sh`](touchgrass-agent.sh), then:

```bash
./touchgrass-agent.sh serve                                        # llama-server on :8080, 32k, thinking on
./touchgrass-agent.sh run "your task" docs/reference.md            # one-shot, reference docs attached
./touchgrass-agent.sh tui                                          # interactive
```

opencode also needs a `llamacpp` provider pointing at `http://127.0.0.1:8080/v1`; see
[`bench/opencode.json`](bench/opencode.json). The agent profile is
[`bench/tuned.opencode.json`](bench/tuned.opencode.json) (the `task` subagent and skills off), plus an
[`AGENTS.md`](bench/AGENTS.md) in the work directory. Run opencode once while you are still online,
because it downloads its provider package on first use.

## Repo layout

| Path | What |
|---|---|
| `touchgrass-agent.sh` | The working setup: serve, run, tui |
| `bench/RESULTS.md` | All measurements and what they mean |
| `bench/*.sh`, `bench/grade.py`, `bench/agent_task.txt` | The harness: context sweep, agent runners, independent grader |
| `bench/docs/NOAA_SOLAR.md` | The reference sheet the agent is given (`.v1` is the version that broke E2B) |
| `bench/runs/` | Raw logs and agent output for every run |
| `RULES-week1.md`, `TEMPLATE-week1.md` | Challenge rules and submission template, saved for offline use |

## Challenge notes

Project started 2026-10-07, inside the challenge window. Any commit made after the deadline
(2026-10-11 23:59 PDT) will be listed here, as the rules require.

## License

Apache 2.0. Gemma models are subject to Google's Gemma terms.
