#!/bin/bash
# usage: ctx_sweep.sh <label> <gguf> <ctx...>
LABEL=$1; GGUF=$2; shift 2
BIN=/home/xbill/llama.cpp/build/bin/llama-server; PORT=8081
OUT=$(dirname "$0")/sweep; mkdir -p $OUT
for C in "$@"; do
  LOG=$OUT/$LABEL-$C.log
  $BIN -m $GGUF --host 127.0.0.1 --port $PORT -ngl 99 -c $C -ctk f16 -ctv f16 -fa 1 -t 6 -tb 12 --parallel 1 --reasoning off >$LOG 2>&1 &
  PID=$!; ok=0
  for i in $(seq 1 120); do
    kill -0 $PID 2>/dev/null || break
    curl -fsS localhost:$PORT/health >/dev/null 2>&1 && { ok=1; break; }; sleep 1
  done
  if [ $ok = 0 ]; then echo "$LABEL ctx=$C LOAD_FAIL $(grep -iE 'out of memory|failed|error' $LOG | head -2 | tr '\n' ' ')"; kill $PID 2>/dev/null; wait $PID 2>/dev/null; continue; fi
  VRAM=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
  # fill ~90% of context: "word " is ~1 token
  N=$((C*9/10 - 200))
  python3 -c "import json;print(json.dumps({'messages':[{'role':'user','content':('apple '*$N)+'\nHow many words above? Reply with one short sentence.'}],'max_tokens':32}))" > $OUT/req.json
  R=$(curl -sS -m 900 localhost:$PORT/v1/chat/completions -H 'content-type: application/json' -d @$OUT/req.json)
  VRAM2=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
  echo "$R" | python3 -c "
import json,sys
try:
  r=json.load(sys.stdin); t=r['timings']
  print('$LABEL ctx=$C vram_idle=${VRAM}MiB vram_after=${VRAM2}MiB prompt_tok=%d prefill=%.0f t/s (%.1fs) decode=%.1f t/s reply=%r'%(t['prompt_n'],t['prompt_per_second'],t['prompt_ms']/1000,t['predicted_per_second'],r['choices'][0]['message']['content'][:60]))
except Exception as e: print('$LABEL ctx=$C vram=${VRAM}MiB REQ_FAIL', sys.stdin.read()[:200], e)"
  kill $PID; wait $PID 2>/dev/null; sleep 2
done
