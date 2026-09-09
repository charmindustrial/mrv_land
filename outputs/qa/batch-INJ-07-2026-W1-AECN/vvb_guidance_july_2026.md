# VVB Guidance July 1 - July 31 — sections bearing on INJ-07-2026-W1
Source: https://docs.google.com/document/d/1IQS3Aeqg3MISVjXqzRtYcYmCvEfRo7LNxQgilqdlF0U/edit
Owner garrett.lutz@charmindustrial.com; modified 2026-07-22; read 2026-08-06.

## Trailer Standard Empty Weight (AECN Rail Offloads)

For AECN rail offloads, net bio-oil mass injected is the Full scale weight minus the Empty scale weight of the same tractor + trailer. When an offload's empty scale ticket is missing, or its trailer/tractor does not match the Full ticket (a rig mismatch), the recorded empty weight cannot be used directly. In these cases a conservative per-trailer standard empty weight is substituted.

For each trailer, empty (tare) weights were compiled from all available CAT Scale empty tickets across the April-July 2026 rail offloads (n = 48 valid weighings). The conservative standard empty weight is defined as the per-trailer mean plus one standard deviation. Because a heavier empty weight yields a lower net injected mass, mean + 1 sigma ensures the substitution is conservative (under-crediting) - consistent with the treatment of WODO standard mass loss.

Standard empty weights (as of July 2026): KL192 n=22 mean 29,321 sigma 189 -> 29,510 lb; KL188 n=14 mean 28,997 sigma 309 -> 29,307 lb; KL720 n=8 mean 29,515 sigma 130 -> 29,645 lb; KL510 n=4 mean 28,985 sigma 493 -> 29,478 lb.

For a given offload, substitute the standard empty weight for the trailer recorded on the Full ticket when either (a) the empty scale ticket is missing, or (b) the empty ticket's tractor and/or trailer do not match the Full ticket. Substituted values are annotated in the ops-notes Empty Scale Ticket cell.

### Application - July 1-31 RP (Week 1, INJ-07-2026-W1)
- GRPX5188 offload 1 - full/empty tractor mismatch (CH1 vs CH2; trailer KL192 both). KL192 standard 29,510 lb applied.
- GRPX5188 offload 3 - trailer mismatch (loaded on KL192; empty ticket was KL720). KL192 standard 29,510 lb applied.
- GPRX5107 offload 3 - full/empty tractor mismatch (CH2 vs CH1; trailer KL192 both). KL192 standard 29,510 lb applied.
- GPRX5107 offload 1 - empty ticket was initially missing; the correct KL188 empty ticket (CAT #1312226184338, 28,720 lb, CH2/KL188) was subsequently located and used directly - net 19,876 kg. No standard-empty substitution needed.

## Scale Tickets - Tractor/Trailer Nomenclature Mismatch

This is an operational artifact of a drop-trailer delivery arrangement and does not indicate a mismatched load or an erroneous weighing... The make and model of the trailer - the unit that physically holds and transports the bio-oil - is the same across both the full and empty weighings, and is the basis on which the two tickets are matched for that offload.
