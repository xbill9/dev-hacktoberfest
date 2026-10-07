#!/bin/bash
# usage: agent_run.sh <model-id> <trial>   (server must already be on :8080 with the right GGUF)
M=$1; T=$2; S=$(dirname "$0"); D=$S/agent/$M-$T; rm -rf $D; mkdir -p $D
export PATH=/home/xbill/devto-hackoberfest/bench/.agentenv/bin:$PATH
start=$(date +%s)
( cd $D && timeout 900 opencode run -m llamacpp/$M --format json "$(cat $S/agent_task.txt)" < /dev/null > $S/agent/$M-$T.jsonl 2> $S/agent/$M-$T.err )
rc=$?; end=$(date +%s)
tools=$(grep -c '"type":"tool_use"' $S/agent/$M-$T.jsonl)
ver=$(cd $D && timeout 60 python3 -m pytest -q 2>&1 | tail -1)
# independent check against a grader test, so a model can't pass by weakening its own tests
grade=$(cd $D && timeout 60 /home/xbill/.pyenv/shims/python3 -I $S/grade.py 2>&1 | tail -1)
echo "$M trial=$T rc=$rc wall=$((end-start))s tool_events=$tools files=$(ls $D | tr '\n' ' ') own_tests='$ver' grader='$grade'"
