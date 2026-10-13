# Bounded J20–J22 queue stopped

{
  "job": "J22",
  "line": 1,
  "command": "python3 -m sim optimize --deck results/runs/cattiva_dragons.txt --rounds 1 --max-tries 6 --seed 231 --screen-games 400 --screen-outs 14",
  "argv": [
    "python3",
    "-m",
    "sim",
    "optimize",
    "--deck",
    "results/runs/cattiva_dragons.txt",
    "--rounds",
    "1",
    "--max-tries",
    "6",
    "--seed",
    "231",
    "--screen-games",
    "400",
    "--screen-outs",
    "14"
  ],
  "head": "034a132b08d16023f6fe63a5a2b7ce0be06b5866",
  "start": "2026-10-12T13:52:54.748771+00:00",
  "log": "/home/gator/palworld-run-artifacts/J20-J22-reordered/J22-1.stdout",
  "phase": "FAILED",
  "pid": 2770443,
  "checked": "2026-10-13T02:22:54.791564+00:00",
  "log_bytes": 999,
  "end": "2026-10-13T02:24:58.135229+00:00",
  "exit": 0,
  "error": "Traceback (most recent call last):\n  File \"/home/gator/palworld-run-artifacts/J20-J22-reordered/queue.py\", line 151, in <module>\n    try:run()\n        ^^^^^\n  File \"/home/gator/palworld-run-artifacts/J20-J22-reordered/queue.py\", line 112, in run\n    assert not git('diff',m['base'],'--',*m['inputs'])\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n",
  "time": "2026-10-13T02:24:58.153517+00:00"
}
