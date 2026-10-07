"""Derive every computed figure the article quotes from the raw run logs.

Usage: python3 derive_facts.py > runs/derived.txt   (run from bench/)
"""
import collections, glob, json, os, re

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")

print("# Derived from runs/ by derive_facts.py")
print("\n## Tool calls per agent run (tool, status): count")
edit_tot = collections.Counter()
for f in sorted(glob.glob(f"{R}/agent-*/*.jsonl")):
    c = collections.Counter()
    for line in open(f):
        try:
            p = json.loads(line).get("part") or {}
        except ValueError:
            continue
        if p.get("type") == "tool":
            c[(p["tool"], p["state"]["status"])] += 1
    name = os.path.relpath(f, R)
    ok, err = c[("edit", "completed")], c[("edit", "error")]
    print(f"{name}: {dict(c)}  edits {ok + err}, failed {err}")

print("\n## Decode speed per run, from llama-server 'eval time' lines (all requests in the run)")
arms = collections.defaultdict(list)
for f in sorted(glob.glob(f"{R}/agent-rvb/server-gemma-4-e2b*-rvb*.log")):
    s = open(f).read()
    ev = [(int(n), float(ms)) for ms, n in re.findall(r"\s eval time =\s+([\d.]+) ms /\s+(\d+) tokens", s)]
    tps = sum(n for n, _ in ev) / sum(ms for _, ms in ev) * 1000
    arm = "google" if "google" in f else "repack"
    arms[arm].append(tps)
    print(f"{os.path.basename(f)}: {tps:.1f} tok/s over {len(ev)} requests")
for arm, v in arms.items():
    print(f"E2B {arm}: mean of {len(v)} runs = {sum(v) / len(v):.1f} tok/s")

print("\n## opencode prompt size, cold server, request 'Reply with exactly: pong' (prompt-size-server.log)")
s = open(f"{R}/prompt-size-server.log").read()
for task, label in (("4", "default profile, Claude skills imported"), ("29", "tuned profile, skill and task tools off")):
    m = re.search(rf"task {task} \| prompt eval time =\s+([\d.]+) ms /\s+(\d+) tokens", s)
    print(f"{label}: {m.group(2)} tokens, cold prefill {float(m.group(1)) / 1000:.1f} s on E2B")

print("\n## Grader, re-run now on every saved agent output (grade.py: London, New York, Sydney within 10 min)")
import subprocess, sys
for d in sorted(glob.glob(f"{R}/agent-*/gemma-4-*")):
    if not os.path.isdir(d):
        continue
    out = subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(R), "grade.py")], cwd=d,
                         capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    print(f"{os.path.relpath(d, R)}: {out[-1] if out else 'no output'}")

print("\n## Counts quoted in the article, computed from the re-grade and tool-call data above")
def graded(pattern):
    res = []
    for d in sorted(glob.glob(f"{R}/{pattern}")):
        if os.path.isdir(d):
            out = subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(R), "grade.py")], cwd=d,
                                 capture_output=True, text=True, timeout=60).stdout.strip()
            res.append(out.endswith("GRADER 3/3"))
    return res
def edits(pattern):
    ok = err = 0
    for f in glob.glob(f"{R}/{pattern}"):
        for line in open(f):
            p = (json.loads(line).get("part") or {}) if line.strip() else {}
            if p.get("type") == "tool" and p["tool"] == "edit":
                ok += p["state"]["status"] == "completed"; err += p["state"]["status"] == "error"
    return ok, err
conds = {
    "E4B, thinking + tuned profile + doc attached": ["agent-attach/gemma-4-e4b-*", "agent-attach2/gemma-4-e4b-*"],
    "E4B, thinking + tuned profile + doc in the repo": ["agent-docs/gemma-4-e4b-*"],
    "E4B, thinking + tuned profile": ["agent-tuned/gemma-4-e4b-*"],
    "E4B, default settings": ["agent-rvb/gemma-4-e4b-1"],
    "E2B, thinking + tuned profile + doc attached": ["agent-attach/gemma-4-e2b-*", "agent-attach2/gemma-4-e2b-*"],
    "E2B, default settings, both GGUFs": ["agent-rvb/gemma-4-e2b-*"],
}
fails = total_fail = 0
for name, pats in conds.items():
    r = [x for p in pats for x in graded(p)]
    print(f"{name}: {sum(r)} of {len(r)} passed")
    if not name.startswith("E4B, thinking + tuned profile + doc attached"):
        total_fail += len(r) - sum(r); fails += len(r)
print(f"every other combination: {fails - total_fail} of {fails} passed")
ok, err = edits("agent-rvb/gemma-4-e4b-1.jsonl"); print(f"E4B default settings edits: {err} of {ok + err} failed")
ok, err = edits("agent-rvb/gemma-4-e2b-rvb3.jsonl"); print(f"E2B repack default run 3 edits: {err} of {ok + err} failed")
ok, err = edits("agent-tuned/gemma-4-e4b-tuned-1.jsonl"); print(f"E4B tuned run 1 edits: {ok} of {ok + err} landed")
ok, err = edits("agent-attach*/gemma-4-e2b-*.jsonl"); print(f"E2B doc-attached runs edits: {ok} of {ok + err} landed")
v = [float(x) for x in re.findall(r"vram=(\d+)MiB", open(f"{R}/rvb.txt").read())]
print(f"E2B VRAM at 32k: google {max(v):.0f} MiB, repack {min(v):.0f} MiB, difference {max(v) - min(v):.0f} MiB")
