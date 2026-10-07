#!/bin/bash
# E2B on the 1650 Ti through opencode: Google's QAT GGUF (baseline) vs the exact Q4_0 repack.
# Same server flags, same task, same grader; arms alternate per trial (ABBA-ish) so drift hits both.
S=$(dirname "$0"); BIN=/home/xbill/llama.cpp/build/bin/llama-server
declare -A G=([gemma-4-e2b-google]=/home/xbill/models/gemma-4-E2B-it-qat-q4_0/gemma-4-E2B_q4_0-it.gguf
              [gemma-4-e2b]=/home/xbill/models/gemma-4-E2B-it-qat-q4_0-exact-v2/gemma-4-E2B-it-q4_0-exact.gguf)
run() { M=$1; T=$2
  $BIN -m ${G[$M]} --host 127.0.0.1 --port 8080 -ngl 99 -c 32768 -ctk f16 -ctv f16 -fa 1 -t 6 -tb 12 --parallel 1 --reasoning off --metrics > $S/agent/server-$M-rvb$T.log 2>&1 &
  P=$!; for i in $(seq 1 120); do curl -fsS localhost:8080/health >/dev/null 2>&1 && break; sleep 1; done
  V=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
  echo "$($S/agent_run.sh $M rvb$T) vram=${V}MiB"
  kill -9 $P; wait $P 2>/dev/null; sleep 2; }
for T in 1 2 3; do
  if [ $((T%2)) = 1 ]; then run gemma-4-e2b-google $T; run gemma-4-e2b $T; else run gemma-4-e2b $T; run gemma-4-e2b-google $T; fi
done
