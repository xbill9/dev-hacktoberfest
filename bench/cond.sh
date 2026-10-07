#!/bin/bash
# usage: tuned.sh <trials> <model-id...>   thinking ON, otherwise the rig's flags at 32k.
S=$(dirname "$0"); BIN=/home/xbill/llama.cpp/build/bin/llama-server; N=$1; shift
declare -A G=([gemma-4-e4b]=/home/xbill/models/gemma-4-E4B-it-qat-q4_0-exact/gemma-4-E4B-it-q4_0-exact.gguf
              [gemma-4-e2b]=/home/xbill/models/gemma-4-E2B-it-qat-q4_0-exact-v2/gemma-4-E2B-it-q4_0-exact.gguf
              [gemma-4-e2b-google]=/home/xbill/models/gemma-4-E2B-it-qat-q4_0/gemma-4-E2B_q4_0-it.gguf)
mkdir -p $S/runs/${OUTDIR:-agent-tuned}
for M in "$@"; do
  $BIN -m ${G[$M]} --host 127.0.0.1 --port 8080 -ngl 99 -c 32768 -ctk f16 -ctv f16 -fa 1 -t 6 -tb 12 --parallel 1 --reasoning on --metrics > $S/runs/${OUTDIR:-agent-tuned}/server-$M.log 2>&1 &
  P=$!; for i in $(seq 1 120); do curl -fsS localhost:8080/health >/dev/null 2>&1 && break; sleep 1; done
  for T in $(seq ${START:-1} $N); do $S/${RUNNER:-agent_run_tuned.sh} $M $T; done
  kill -9 $P; wait $P 2>/dev/null; sleep 2
done
