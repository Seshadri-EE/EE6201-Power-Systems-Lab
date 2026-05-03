# Short Circuit Analysis using Symmetrical Components
### EE6201 — Power Systems Lab, IIT Hyderabad

---

## Overview

This repository contains the assignment template for **Assignment 11** of the
Power Systems Lab course (EE6201) offered at the **Indian Institute of Technology
Hyderabad (IIT Hyderabad)**, Spring 2026.

The assignment implements a **Short Circuit Analysis solver** for a power system
network using the **method of symmetrical components** and the **bus impedance
matrix (Z-bus)**. Four fault types are supported: three-phase (LLLG), single
line to ground (SLG), line to line (LL), and double line to ground (DLG).

> **The code is intentionally incomplete.**
> Students are expected to fill in the marked sections (`# YOUR CODE STARTS HERE`)
> as part of the assignment. The template provides the architecture, data
> structures, detailed comments, formulas, and hints — the core logic is left
> for the student to implement.

Interested users outside the course are welcome to adopt and extend the code
for their own purposes.

---

## Author

**V. Seshadri Sravan Kumar**
Department of Electrical Engineering
Indian Institute of Technology Hyderabad (IIT Hyderabad)

---

## File Structure

```
├── SystemData.py       # Global database — shared lists, sequence matrices, fault spec
├── NetworkClasses.py   # Class definitions for all network elements
├── Reading.py          # Parses network data file into SystemData
├── Initialize.py       # Sets pre-fault bus voltages (flat start)
├── NetworkModel.py     # Builds sequence Y-bus matrices (Y1, Y2, Y0)
├── ZBus.py             # Inverts Y-bus to get Z-bus matrices (Z1, Z2, Z0)
├── FaultAnalysis.py    # Computes fault currents and post-fault voltages
├── Results.py          # Prints fault currents and post-fault bus voltages
├── SC.py               # Main driver — runs the full solution pipeline
├── Data/
│   └── Data.d1         # Network data file (South Indian power system)
└── README.md
```

---

## How to Run

```bash
python SC.py
```

When prompted:
```
Enter the input data filename: Data/Data.d1
Enter faulted bus node number (1 to N): 5
Fault types: LLLG | SLG | LL | DLG
Enter fault type: SLG
Enter fault impedance Zf in pu [default 0.0]:
```

---

## Solution Pipeline

```
SC.py
 │
 ├── [Stage 1]  Reading.py        Parse data file → populate SystemData
 ├── [Stage 2]  Initialize.py     Set pre-fault voltages (flat start: 1∠0° pu)
 ├── [Stage 3]  NetworkModel.py   Build Y1, Y2, Y0 (sequence Y-bus matrices)
 ├── [Stage 4]  ZBus.py           Invert Y1, Y2, Y0 → Z1, Z2, Z0
 ├── [Stage 5]  User input        Fault bus, fault type, fault impedance
 ├── [Stage 6]  FaultAnalysis.py  Compute sequence & phase fault currents
 │                                Compute post-fault sequence & phase voltages
 └── [Stage 7]  Results.py        Print fault currents and bus voltages
```

---

## Fault Analysis Theory

The fault current at bus $k$ is computed using the Thevenin equivalent
of the sequence networks as seen from the faulted bus.

Let $Z_{kk}^{(1)}$, $Z_{kk}^{(2)}$, $Z_{kk}^{(0)}$ be the diagonal elements
of the positive, negative, and zero sequence Z-bus at bus $k$, and
$V_k^0 = 1\angle 0°$ pu (pre-fault voltage). Then:

| Fault Type | Sequence Currents |
|------------|------------------|
| **LLLG** | $I_{a1} = V_k^0 / (Z_{kk}^{(1)} + Z_f)$,  $I_{a2} = I_{a0} = 0$ |
| **SLG**  | $I_{a1} = I_{a2} = I_{a0} = V_k^0 / (Z_{kk}^{(1)} + Z_{kk}^{(2)} + Z_{kk}^{(0)} + 3Z_f)$ |
| **LL**   | $I_{a1} = V_k^0 / (Z_{kk}^{(1)} + Z_{kk}^{(2)} + Z_f)$,  $I_{a2} = -I_{a1}$,  $I_{a0} = 0$ |
| **DLG**  | See `FaultAnalysis.py` for full expression |

Phase currents are recovered via the symmetrical component transformation
($a = e^{j2\pi/3}$):

$$\begin{bmatrix} I_a \\ I_b \\ I_c \end{bmatrix} = \begin{bmatrix} 1 & 1 & 1 \\ 1 & a^2 & a \\ 1 & a & a^2 \end{bmatrix} \begin{bmatrix} I_{a0} \\ I_{a1} \\ I_{a2} \end{bmatrix}$$

Post-fault voltages at all buses $i$ are computed using the off-diagonal
Z-bus elements:

$$V_i^{(1)} = V_i^0 - Z_{ik}^{(1)} I_{a1}, \quad V_i^{(2)} = -Z_{ik}^{(2)} I_{a2}, \quad V_i^{(0)} = -Z_{ik}^{(0)} I_{a0}$$

---

## Important Assumptions

1. **Node Numbering** — Buses numbered sequentially 1 to N, no gaps.
   Bus 1 is the reference. Array index = node number - 1.

2. **Sequence Impedance Equality** — Positive = Negative = Zero sequence
   impedances (same branch data used for all three networks). In reality:
   - Zero sequence line impedance ≈ 2–3.5× positive sequence
   - Transformer zero sequence model depends on winding connections
   
   Students may extend by adding `r0`/`x0` fields to the data file.

3. **Pre-Fault Voltages — Flat Start** — All buses initialised to 1∠0° pu.
   For accuracy, run the load flow (Assignment 10) first and use converged
   voltages as pre-fault conditions.

4. **Bolted Fault** — $Z_f = 0$ by default. User may specify otherwise.

5. **Generator Modeling** — Generators not modeled as shunt elements
   (subtransient reactance $X_d''$ not in data file). May be extended.

6. **Loads Not Modeled** — Loads read from file but not used in sequence networks.

7. **Z-Bus by Inversion** — Direct matrix inversion used for simplicity.
   For large networks, the Z-bus building algorithm or sparse LU
   factorisation is more efficient. See `ZBus.py` for details.

---

## Relationship to Assignment 10

This assignment is **independent** of Assignment 10 (Load Flow). All files
are self-contained and use their own copies of the shared classes and data.
The same network data file (`Data.d1`) is used for both assignments.

For a more accurate short circuit analysis, the pre-fault voltages from
the load flow solution (Assignment 10) may be used in place of the flat
start. This extension is noted in `Initialize.py`.

---

## Data Acknowledgement

The network data file (`Data.d1`) represents a South Indian power system
equivalent network. It was originally shared with V. Seshadri Sravan Kumar
during his PhD studies at the **Indian Institute of Science (IISc), Bangalore**,
by **Prof. D. Thukaram**, Department of Electrical Engineering, IISc.
Full credit and gratitude to Prof. Thukaram for sharing this data.
The data is used here solely for educational purposes.

---

## Acknowledgement

The concepts, structure, and pedagogical ideas in this assignment are original.
The assignment template was developed with partial assistance from an AI
language model (Claude, Anthropic) for formatting and scaffolding purposes.

---

## Dependencies

- Python 3.8+
- NumPy

```bash
pip install numpy
```

---

## License

This code is shared for educational purposes.
You are free to use, adapt, and extend it with appropriate attribution.
