#!/bin/bash
# usage: agent_run_tuned.sh <model-id> <trial>   (server on :8080 started with --reasoning on)
# Tuned profile: AGENTS.md in the work dir, task subagent denied (OPENCODE_CONFIG merges over global).
M=$1; T=$2; S=$(dirname "$0"); N=$M-tuned-$T; D=$S/runs/agent-tuned/$N; rm -rf $D; mkdir -p $D
cp $S/AGENTS.md $D/
export PATH=/home/xbill/devto-hackoberfest/bench/.agentenv/bin:$PATH
start=$(date +%s)
( cd $D && OPENCODE_CONFIG=$S/tuned.opencode.json timeout 1500 opencode run -m llamacpp/$M --format json "$(cat $S/agent_task.txt)" < /dev/null > $D.jsonl 2> $D.err )
rc=$?; end=$(date +%s)
tools=$(python3 -c "import json,sys,collections;c=collections.Counter(json.loads(l).get('part',{}).get('tool') for l in open(sys.argv[1]) if '\"tool_use\"' in l);print(dict(c))" $D.jsonl 2>/dev/null)
ver=$(cd $D && timeout 60 python3 -m pytest -q 2>&1 | tail -1)
grade=$(cd $D && timeout 60 /home/xbill/.pyenv/shims/python3 -I $S/grade.py 2>&1 | tail -1)
echo "$N rc=$rc wall=$((end-start))s tools=$tools own_tests='$ver' grader='$grade'"
