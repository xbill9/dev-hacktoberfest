#!/bin/bash
P=$(dirname "$0")
while pgrep -f 'agent_run_attach.sh' >/dev/null || pgrep -x llama-server >/dev/null; do sleep 5; done
RUNNER=agent_run_attach2.sh OUTDIR=agent-attach2 $P/cond.sh 3 gemma-4-e2b
RUNNER=agent_run_attach2.sh OUTDIR=agent-attach2 $P/cond.sh 1 gemma-4-e4b
