# J0 benchmark
HEAD: be2f28bbd65bf7259598bdecf3d1a00373df4e69
Start UTC: 2026-09-30T19:35:55.515851+00:00
End UTC: 2026-09-30T19:37:20.208517+00:00
Command: `python3 -m sim run --deck data/decks/cattiva-azurobe-br.txt --opp data/decks/chillet-relaxaurus-bp.txt --bot heuristic2 --games 400 --seed 5 --no-report --logs 0`
Exit: 0
Elapsed seconds: 84.675
J1 games: 1000

```text
12
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           39 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  12
On-line CPU(s) list:                     0-11
Vendor ID:                               GenuineIntel
Model name:                              Intel(R) Core(TM) i7-8700T CPU @ 2.40GHz
CPU family:                              6
Model:                                   158
Thread(s) per core:                      2
Core(s) per socket:                      6
Socket(s):                               1
Stepping:                                10
CPU(s) scaling MHz:                      59%
CPU max MHz:                             4000.0000
CPU min MHz:                             800.0000
BogoMIPS:                                4800.00
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb pti ssbd ibrs ibpb stibp tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp vnmi md_clear flush_l1d arch_capabilities
Virtualization:                          VT-x
L1d cache:                               192 KiB (6 instances)
L1i cache:                               192 KiB (6 instances)
L2 cache:                                1.5 MiB (6 instances)
L3 cache:                                12 MiB (1 instance)
NUMA node(s):                            1
NUMA node0 CPU(s):                       0-11
Vulnerability Gather data sampling:      Vulnerable
Vulnerability Ghostwrite:                Not affected
Vulnerability Indirect target selection: Not affected
Vulnerability Itlb multihit:             KVM: Mitigation: Split huge pages
Vulnerability L1tf:                      Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vulnerable
Vulnerability Mds:                       Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Meltdown:                  Mitigation; PTI
Vulnerability Mmio stale data:           Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Old microcode:             Not affected
Vulnerability Reg file data sampling:    Not affected
Vulnerability Retbleed:                  Mitigation; IBRS
Vulnerability Spec rstack overflow:      Not affected
Vulnerability Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:                Mitigation; IBRS; IBPB conditional; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                     Mitigation; Microcode
Vulnerability Tsa:                       Not affected
Vulnerability Tsx async abort:           Mitigation; TSX disabled
Vulnerability Vmscape:                   Mitigation; IBPB before exit to userspace
               total        used        free      shared  buff/cache   available
Mem:              15           2           2           0          10          12
Swap:              3           3           0
Python 3.11.15

400 games: cattiva-azurobe-br vs chillet-relaxaurus-bp -> results/20260930-193555_cattiva-azurobe-br_vs_chillet-relaxaurus-bp
  40/400 games
  80/400 games
  120/400 games
  160/400 games
  200/400 games
  240/400 games
  280/400 games
  320/400 games
  360/400 games
  400/400 games
{
  "win_rate": 0.595,
  "ci95": [
    0.5462,
    0.642
  ],
  "going_first": {
    "games": 218,
    "wins": 152,
    "losses": 66,
    "draws": 0,
    "win_rate": 0.6972,
    "ci95": [
      0.6333,
      0.7544
    ]
  },
  "going_second": {
    "games": 182,
    "wins": 86,
    "losses": 96,
    "draws": 0,
    "win_rate": 0.4725,
    "ci95": [
      0.4013,
      0.5449
    ]
  },
  "avg_turns": 12.84
}
wrote results/20260930-193555_cattiva-azurobe-br_vs_chillet-relaxaurus-bp/summary.json, games.jsonl

```
