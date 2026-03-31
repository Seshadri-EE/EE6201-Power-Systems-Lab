# Newton-Raphson Load Flow Solver
### EE6201 — Power Systems Lab, IIT Hyderabad

---

## Overview

This repository contains the assignment template for **Assignment 10** of the
Power Systems Lab course (EE6201) offered at the **Indian Institute of Technology
Hyderabad (IIT Hyderabad)**, Spring 2026.

The assignment implements a **Newton-Raphson Load Flow solver** for a power
system network in Python. The code is structured as a set of modular files,
each responsible for a specific stage of the solution pipeline.

> **The code is intentionally incomplete.**
> Students are expected to fill in the marked sections (`# YOUR CODE STARTS HERE`)
> as part of the assignment. The template provides the architecture, data
> structures, detailed comments, and hints — the core logic is left for the
> student to implement.

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
├── SystemData.py       # Global database — shared lists and constants
├── NetworkClasses.py   # Class definitions for all network elements
├── Reading.py          # Parses network data file into SystemData
├── Initialize.py       # Sets initial complex voltages at all buses
├── NetworkModel.py     # Builds the Y-Bus admittance matrix (YBus class)
├── NetworkState.py     # Computes power injections at all buses
├── Mismatch.py         # Computes the power mismatch vector
├── PVPQSwitch.py       # Handles PV-PQ bus type switching
├── Jacobian.py         # Forms the Jacobian matrix
├── Update.py           # Solves J*Δx = mismatch and updates voltages
├── Results.py          # Prints converged voltage profile and line flows
├── LF.py               # Main driver — runs the full solution pipeline
└── README.md
```

---

## How to Run

```bash
python LF.py
```

When prompted, enter the name of the network data file (e.g. `network.txt`).
The data file will be made available separately on this repository.

---

## Data File Format

The network data file uses fixed record codes to identify element types.
Each line begins with a two-character code followed by the element data:

| Code | Element           | Format |
|------|-------------------|--------|
| `BS` | Bus               | `BS  <zone>  <name>  <node>  <voltage_kV>` |
| `TR` | Transformer       | `TR  <zone>  <name>  <from>  <to>  <r>  <x>  <tap>  <max_MVA>` |
| `TL` | Transmission Line | `TL  <zone>  <name>  <from>  <to>  <r>  <x>  <b/2>  <max_MVA>` |
| `DZ` | Shunt Reactor     | `DZ  <zone>  <name>  <node>  <r>  <x>` |
| `DP` | Load              | `DP  <zone>  <name>  <node>  <P_MW>  <Q_MVAR>  <comp_MVAR>` |
| `GP` | Generator         | `GP  <zone>  <name>  <node>  <P_MW>  <Q_max>  <Q_min>  <V_pu>` |

All impedance and admittance values are in **per unit** on the system base.
All power values are in **MW / MVAR**.

---

## Important Assumptions

The following assumptions are made in this implementation. Users extending
the code for production use should address these limitations:

1. **Node Numbering** — Buses are numbered sequentially from 1 to N with
   no missing numbers. Bus 1 is always the slack bus. A node renumbering
   module would be needed for arbitrary bus numbering.

2. **Constant PQ Load Model** — All loads are modeled as constant PQ.
   The specified power vector is formed once before the iterative loop.
   Voltage-dependent load models (ZIP, constant current) are not supported.

3. **Single Slack Bus** — Exactly one slack bus, fixed at node 1 with
   |V| = 1.0 pu and δ = 0°.

4. **Flat Start Initialisation** — PQ buses initialised to 1∠0° pu.
   PV bus magnitudes set from generator data with angle 0°.

5. **Fixed Tap Transformers** — Tap changers are fixed at the specified
   value and not adjusted during the load flow solution.

6. **Pi-Equivalent Line Model** — Transmission lines use the standard
   π-equivalent circuit with half-line charging susceptance b/2 at each end.

7. **PV-PQ Switching** — Generator buses are checked against reactive power
   limits [Q_min, Q_max] at every iteration. Buses violating limits are
   switched to PQ. Switching changes the size of the mismatch vector and
   Jacobian, both rebuilt after every switch.

---

## Solution Pipeline

```
LF.py
 │
 ├── [Stage 1]  Reading.py          Parse data file → populate SystemData
 ├── [Stage 2]  Initialize.py       Set initial voltages and bus types
 ├── [Stage 3]  NetworkModel.py     Build Y-Bus matrix
 │
 └── [Stage 4]  Newton-Raphson Loop
      │
      ├── NetworkState.compute_power()       Calculate P, Q at all buses
      ├── PVPQSwitch.check_pv_pq_switch()   Check and switch PV/PQ buses
      ├── Mismatch.compute_mismatch()        Form [ΔP; ΔQ] vector
      ├── convergence check
      ├── Jacobian.form_jacobian()           Build J matrix
      ├── Update.solve_linear_system()       Solve J*Δx = mismatch
      └── Update.update_voltages()           Apply corrections to voltages
 │
 └── [Stage 5]  Results.py          Print converged solution
```

---

## Dependencies

- Python 3.8+
- NumPy

```bash
pip install numpy
```

---

## Acknowledgements

**Network Data:**
The network data file (`Data.d1`) is a South Indian power system equivalent
network. It was originally shared with V. Seshadri Sravan Kumar during his
PhD studies at the **Indian Institute of Science (IISc), Bangalore**, by
**Prof. D. Thukaram**, Department of Electrical Engineering, IISc.
Full credit and gratitude to Prof. Thukaram for sharing this data.
The data is used here solely for educational purposes.

**Assignment Template:**
The concepts, structure, and pedagogical ideas in this assignment are original.
The assignment template was developed with partial assistance from an AI
language model (Claude, Anthropic) for formatting and scaffolding purposes.

---

## License

This code is shared for educational purposes.
You are free to use, adapt, and extend it with appropriate attribution.