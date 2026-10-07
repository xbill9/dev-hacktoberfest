#!/bin/bash
# usage: cc_run.sh <model-label> <stock|lean> <trial>   (llama-server on :8080 serving the GGUF)
# Permissions: file edits accepted; Bash only for python3/pytest; nothing else is pre-approved,
# and in -p mode anything unapproved is refused rather than prompted.
M=$1; V=$2; T=$3; S=$(dirname "$0"); N=cc-$V-$M-$T; D=$S/agent/$N; rm -rf $D; mkdir -p $D
TOOLS=(); [ $V = lean ] && TOOLS=(--tools "Bash,Read,Write,Edit")
export PATH=/home/xbill/devto-hackoberfest/bench/.agentenv/bin:$PATH
start=$(date +%s)
( cd $D && ANTHROPIC_BASE_URL=http://127.0.0.1:8080 ANTHROPIC_API_KEY=local \
  ANTHROPIC_MODEL=$M ANTHROPIC_DEFAULT_HAIKU_MODEL=$M ANTHROPIC_DEFAULT_SONNET_MODEL=$M ANTHROPIC_DEFAULT_OPUS_MODEL=$M \
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 DISABLE_TELEMETRY=1 DISABLE_AUTOUPDATER=1 \
  timeout 900 claude -p --bare --strict-mcp-config --permission-mode acceptEdits \
    --allowedTools "Bash(python3:*)" "Bash(pytest:*)" "${TOOLS[@]}" \
    --output-format stream-json --verbose "$(cat $S/agent_task.txt)" < /dev/null > $S/agent/$N.jsonl 2> $S/agent/$N.err )
rc=$?; end=$(date +%s)
tools=$(grep -o '"type":"tool_use"' $S/agent/$N.jsonl | wc -l)
ver=$(cd $D && timeout 60 python3 -m pytest -q 2>&1 | tail -1)
grade=$(cd $D && timeout 60 /home/xbill/.pyenv/shims/python3 -I $S/grade.py 2>&1 | tail -1)
echo "$N rc=$rc wall=$((end-start))s tool_uses=$tools files=$(ls $D | tr '\n' ' ') own_tests='$ver' grader='$grade'"
