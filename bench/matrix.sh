#!/bin/bash
S=$(dirname "$0"); BIN=/home/xbill/llama.cpp/build/bin/llama-server
declare -A G=([gemma-4-e4b]=/home/xbill/models/gemma-4-E4B-it-qat-q4_0-exact/gemma-4-E4B-it-q4_0-exact.gguf
              [gemma-4-e2b]=/home/xbill/models/gemma-4-E2B-it-qat-q4_0-exact-v2/gemma-4-E2B-it-q4_0-exact.gguf)
for M in gemma-4-e4b gemma-4-e2b; do
  $BIN -m ${G[$M]} --host 127.0.0.1 --port 8080 -ngl 99 -c 32768 -ctk f16 -ctv f16 -fa 1 -t 6 -tb 12 --parallel 1 --reasoning off --metrics > $S/agent/server-$M.log 2>&1 &
  P=$!; for i in $(seq 1 120); do curl -fsS localhost:8080/health >/dev/null 2>&1 && break; sleep 1; done
  for T in 1; do
    $S/agent_run.sh $M $T
    $S/cc_run.sh $M lean $T
    $S/cc_run.sh $M stock $T
  done
  kill -9 $P; wait $P 2>/dev/null; sleep 2
done
