#!/bin/bash
# The workable recipe, measured 2026-10-07 (bench/RESULTS.md): Gemma 4 E4B exact Q4_0 GGUF on the
# GTX 1650 Ti at 32k with thinking ON, opencode with the task subagent and skills off.
#   ./touchgrass-agent.sh serve        # start llama-server on :8080 (stops nothing else; free the port first)
#   ./touchgrass-agent.sh run "task" docs/REF.md [more refs...]   # one-shot, reference docs attached
#   ./touchgrass-agent.sh tui          # interactive opencode in the current directory
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
GGUF=/home/xbill/models/gemma-4-E4B-it-qat-q4_0-exact/gemma-4-E4B-it-q4_0-exact.gguf
export OPENCODE_CONFIG=$HERE/bench/tuned.opencode.json
case "$1" in
  serve) exec /home/xbill/llama.cpp/build/bin/llama-server -m "$GGUF" --host 127.0.0.1 --port 8080 \
           -ngl 99 -c 32768 -ctk f16 -ctv f16 -fa 1 -t 6 -tb 12 --parallel 1 --reasoning on --metrics ;;
  run)   shift; MSG=$1; shift; ARGS=(); for f in "$@"; do ARGS+=(-f "$f"); done
         exec opencode run -m llamacpp/gemma-4-e4b "$MSG" "${ARGS[@]}" < /dev/null ;;
  tui)   exec opencode -m llamacpp/gemma-4-e4b ;;
  *)     sed -n 2,7p "$0"; exit 1 ;;
esac
