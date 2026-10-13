"""Independent recompute behind adversarial_review.md (Gate 3, INJ-09-2026-W3-AECN).
Inputs are values read this session from the ticket images, BOLs, Ops Notes,
Certify component windows, the August guidance and W2's Certify data pull.
Each line prints the figure exactly as the review writes it."""
import math

K = 0.453592  # Ops 'AECN Rail'!O4
out = []
def p(tag, text, val, fmt):
    s = format(val, fmt)
    out.append(f"{tag} | {text} = {s}")

# 2.3 TILX200231 offload 2 with published KL720 standard empty (August guidance: 29,645 lb)
std = (72640 - 29645) * K
p("R1", "TILX200231 o2 net with KL720 standard, (72,640 - 29,645) x 0.453592 (kg)", std, ",.5f")
d = 19504.456 - std
p("R2", "credited 19,504.456 minus R1 (kg)", d, ".5f")
p("R2r", "R2 rounded (kg)", d, ".2f")
g = d * (1 - 0.0129) * (1 - 0.00196) * 0.397 * 3.667 / 1000
p("R3", "R2 after sparging and filtration, x 0.397 x 3.667 (tCO2e)", g, ".4f")

# 2.5 SHPX215046 balance
w3 = [21055.74064, 20992.23776]; w2 = [20810.80096, 14841.53024]
tot = sum(w3) + sum(w2)
p("R4", "sum of the four SHPX215046 offloads (kg)", tot, ",.4f")
p("R5", "R4 minus loaded 77,680 (kg)", tot - 77680, ".4f")
p("R6", "two corrections of R5 (kg)", 2 * (tot - 77680), ".4f")
prior = w2[0] + w2[1] + w3[0]
p("R7a", "sum of W2 o3, W2 o4 and W3 o1 (kg)", prior, ",.5f")
p("R7", "W3 offload 2 back-calculated, 77,680 minus R7a (kg)", 77680 - prior, ",.5f")
p("R8", "gross effect of 20.3096 kg at 39.7 % (tCO2e)", (tot - 77680) * (1 - 0.0129) * (1 - 0.00196) * 0.397 * 3.667 / 1000, ".6f")

# 3.3 guidance basis
G = 20130.41296 + 18951.07376 + 20402.56816 + 18334.18864
T = 20048.7664 + 19504.456 + 19876.40144 + 18025.74608
S = sum(w3)
gl = (21675 + 21666 + 21658) * 1.22
tl = (21660 + 21643 + 21476) * 1.22
p("R9", "GPRX5102 guidance loaded mass, 64,999 L x 1.22 (kg)", gl, ",.2f")
p("R10", "TILX200231 guidance loaded mass, 64,779 L x 1.22 (kg)", tl, ",.2f")
p("R11", "GPRX5102 loss on guidance basis, R9 minus 77,818.24352 (kg)", gl - G, ",.2f")
p("R12", "TILX200231 loss on guidance basis, R10 minus 77,455.36992 (kg)", tl - T, ",.2f")
a_w = (G / 77940 + T / 77520 + S / 77680) * 3 * 107.5
a_g = (G / gl + T / tl + S / 77680) * 3 * 107.5
p("R13", "AECN-SOPOR allocated, weigh-ticket basis, 107.5 mi (mi)", a_w, ".2f")
p("R14", "AECN-SOPOR allocated, guidance basis, 107.5 mi (mi)", a_g, ".2f")
p("R15", "embodied difference, (R13 - R14) x 0.0002375605888 (tCO2e)", (a_w - a_g) * 0.0002375605888, ".4f")
p("R16", "AECN-SOPOR allocated, weigh-ticket basis, 107.49722 mi (mi)", (G / 77940 + T / 77520 + S / 77680) * 3 * 107.49722, ".2f")
p("R17", "AECN-SOPOR allocated, COBB 77,950 basis, 107.5 mi (mi)", (G / 77950 + T / 77520 + S / 77680) * 3 * 107.5, ".2f")
p("R18", "AECN-SOPOR allocated, COBB 77,950 basis, 107.49722 mi (mi)", (G / 77950 + T / 77520 + S / 77680) * 3 * 107.49722, ".2f")
p("R19", "GPRX5102 BOL metric-tons figures summed, 25.99 + 25.99 + 25.97 (t)", 25.99 + 25.99 + 25.97, ".2f")
p("R20", "SHPX215046 BOL metric-tons figures summed, 25.94 + 25.90 + 25.84 (t)", 25.94 + 25.90 + 25.84, ".2f")

# 9.6 BCU
proc = 2.424477007002991 + 11.242612670783098 + 0.9675604969172999
p("R21", "transport process sum of the three Certify components (t)", proc, ".6f")
p("R22", "BCU 14.635 minus R21 (kg)", (14.635 - proc) * 1000, ".2f")
p("R23", "exact BCU entry equal to R21 (kgCO2e)", proc * 1000, ",.3f")

# 7.3 / 7a.3 / 9.8 discount
seq = 194.39438206 * 0.397 * 3.667
rel = math.sqrt((0.7257 / 194.39438206) ** 2 + (0.15883 / 39.7) ** 2)
massacts = 27.0567364208 + 4.1753248444 + 2.424477007002991 + 11.242612670783098 + 0.9675604969172999
sd_s = seq * rel; sd_a = massacts * 0.7257 / 197.32159
p("R24", "sequestration standard deviation (t)", sd_s, ".6f")
p("R25", "mass-driven activities standard deviation (t)", sd_a, ".6f")
p("R26", "combined, square root of R24^2 + R25^2 (t)", math.sqrt(sd_s ** 2 + sd_a ** 2), ".10f")
m2 = 193.4919399
seq2 = m2 * 0.397 * 3.667
rel2 = math.sqrt((0.7257 / m2) ** 2 + (0.15883 / 39.7) ** 2)
disc2 = math.sqrt((seq2 * rel2) ** 2 + sd_a ** 2)
p("R27", "discount with corrected Mass of Injectant 193,491.9399 kg (t)", disc2, ".6f")
acts = massacts + 0.1944880415364 + 0.1739640903 + 0.20382648
p("R28", "activities total (t)", acts, ".6f")
p("R29", "corrected gross 193.4919399 x 0.397 x 3.667 (t)", seq2, ".6f")
p("R30", "corrected net, R29 + R21 - R28 - R27 (t)", seq2 + proc - acts - disc2, ".6f")
p("R31", "Certify gross 194.39438206 x 0.397 x 3.667 (t)", seq, ".6f")
p("R32", "gross overstatement, R31 - R29 (t)", seq - seq2, ".6f")

# 7a.2 carbon uncertainty
p("R33", "booked 0.15883 minus 0.004 x 39.7 (%)", 0.15883 - 0.004 * 39.7, ".5f")

# Observation 2: losses without upstream burden
loss = (77940 - G) + (77520 - T)
p("R34", "GPRX5102 + TILX200231 losses (kg)", loss, ".5f")
p("R35", "pyrolysis on losses, x (0.13712 + 0.02116) (tCO2e)", loss / 1000 * (0.13712 + 0.02116), ".5f")
p("R36", "AECN-SOPOR fuel on losses, x 107.49722 x 0.0001143 (tCO2e)", loss / 1000 * 107.49722 * 0.0001143, ".5f")
p("R37", "rail fuel on losses, x 2,199 x 0.00002591 (tCO2e)", loss / 1000 * 2199 * 2.591e-05, ".5f")
tb = loss / 1000 * (0.13712 + 0.02116) + loss / 1000 * 107.49722 * 0.0001143 + loss / 1000 * 2199 * 2.591e-05
p("R38", "sum of R35, R36 and R37 (tCO2e)", tb, ".4f")

# 9.2 SHPX215046 W3 rail share
p("R39", "SHPX215046 W3 rail share, 2,199 x 42,047.9784 / 77,680 (mi)", 2199 * S / 77680, ",.2f")
p("R40", "2,199 + 2,199 + R39 (mi)", 4398 + 2199 * S / 77680, ",.2f")

# Row-level checks cited in the confirmed table
p("R41", "sum of the 10 W3 offload nets (kg)", G + T + S, ",.5f")
p("R42", "C46 197,321.5918 x 0.0129 (kg)", 197321.5918 * 0.0129, ",.6f")
p("R43", "(C46 - D46) x 0.00196 (kg)", (197321.5918 - 2545.448535) * 0.00196, ".5f")
p("R44", "sum of K28:K37, per-row MOBI (kg)", 19831.784 + 18669.93996 + 20099.90186 + 18062.20616 + 20743.38471 + 20680.82387 + 19751.34864 + 19215.11293 + 19581.54067 + 17758.33926, ",.5f")
p("R45", "K46, 200 gal x 3.785411784 L/gal x 1.192 kg/L (kg)", 200 * 3.785411784 * 1.192, ".7f")

print("\n".join(out))
