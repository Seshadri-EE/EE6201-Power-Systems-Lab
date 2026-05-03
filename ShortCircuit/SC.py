# =============================================================================
# SC.py
# =============================================================================
#
# Course    : EE6201 - Power Systems Lab
# Institute : Indian Institute of Technology Hyderabad (IIT Hyderabad)
# Semester  : Spring 2026
# Assignment: Assignment 11
# Instructor: V. Seshadri Sravan Kumar, Dept. of Electrical Engineering
#
# Note      : The concepts, structure, and pedagogical ideas in this assignment
#             are original. The assignment template was developed with partial
#             assistance from an AI language model (Claude, Anthropic) for
#             formatting and scaffolding purposes.
#
# =============================================================================
# Short Circuit Analysis — Main Driver
# =============================================================================
# DESCRIPTION:
#   Top-level script for the short circuit analysis program.
#   Executes all stages in sequence and prompts the user for fault input.
#
# EXECUTION STAGES:
#   Stage 1 — Reading.py      : Parse data file
#   Stage 2 — Initialize.py   : Set pre-fault bus voltages (flat start)
#   Stage 3 — NetworkModel.py : Build sequence Y-bus matrices (Y1, Y2, Y0)
#   Stage 4 — ZBus.py         : Invert Y-bus to get Z-bus matrices (Z1, Z2, Z0)
#   Stage 5 — Fault input     : User specifies fault bus and type
#   Stage 6 — FaultAnalysis.py: Compute fault currents and post-fault voltages
#   Stage 7 — Results.py      : Display results
#
# =============================================================================

import SystemData as db


# =============================================================================
# IMPORTANT ASSUMPTIONS
# =============================================================================
# The following assumptions are made in this implementation.
#
# 1. NODE NUMBERING:
#    Buses are numbered sequentially from 1 to N with no missing numbers.
#    Bus 1 is the reference bus. Array index = node number - 1.
#    A node renumbering module would be needed for arbitrary numbering.
#
# 2. SEQUENCE IMPEDANCE EQUALITY:
#    Positive, negative, and zero sequence impedances are assumed equal
#    and taken from the standard branch data in the data file.
#    In a full implementation:
#       - Negative sequence impedances are the same as positive for
#         passive elements (lines, transformers).
#       - Zero sequence impedances of lines are typically 2–3.5 times
#         the positive sequence values.
#       - Zero sequence transformer models depend on winding connections
#         (Yg-Yg, Yg-Delta, Delta-Yg, etc.) and must be specified
#         separately in the data file.
#    Students may extend this by adding r0/x0 fields to the data file
#    and reading them in Reading.py.
#
# 3. PRE-FAULT VOLTAGES — FLAT START:
#    All bus voltages are initialised to 1∠0° pu before the fault.
#    For more accurate results, run the load flow (LF.py, Assignment 10)
#    first and use converged voltages as pre-fault conditions.
#
# 4. FAULT IMPEDANCE:
#    A bolted fault (Zf = 0) is assumed by default. The user may modify
#    db.fault_zf in Stage 5 to specify a non-zero fault impedance.
#
# 5. GENERATOR MODELING:
#    Generators are not explicitly modeled as shunt elements in the
#    sequence networks (subtransient reactance Xd'' not available in
#    the data file). In a full implementation, each generator would
#    contribute a shunt admittance of 1/jXd'' at its terminal bus
#    in the positive sequence network.
#
# 6. LOADS:
#    Loads are not modeled in the sequence networks. They are read from
#    the data file for completeness but not used in the fault analysis.
#    In a full implementation, loads may be converted to constant
#    impedance shunts and included in the sequence networks.
#
# 7. Z-BUS METHOD:
#    Z-bus is obtained by direct inversion of Y-bus. For large networks,
#    the Z-bus building algorithm or sparse LU factorisation is preferred.
#    See ZBus.py for details.
# =============================================================================


# =============================================================================
# STAGE 1 — READ NETWORK DATA
# =============================================================================

print("=" * 65)
print("  EE6201 Power Systems Lab — Short Circuit Analysis")
print("=" * 65)

print("\n[Stage 1] Reading network data...")
import Reading
print("[Stage 1] Complete.")


# =============================================================================
# STAGE 2 — INITIALISE PRE-FAULT VOLTAGES
# =============================================================================

print("\n[Stage 2] Initialising pre-fault bus voltages (flat start)...")
import Initialize
print("[Stage 2] Complete.")


# =============================================================================
# STAGE 3 — BUILD SEQUENCE Y-BUS MATRICES
# =============================================================================

print("\n[Stage 3] Building sequence Y-Bus matrices...")
import NetworkModel
print("[Stage 3] Complete.")


# =============================================================================
# STAGE 4 — COMPUTE SEQUENCE Z-BUS MATRICES
# =============================================================================

print("\n[Stage 4] Computing sequence Z-Bus matrices (by inversion)...")
import ZBus
print("[Stage 4] Complete.")


# =============================================================================
# STAGE 5 — FAULT SPECIFICATION
# =============================================================================

print("\n[Stage 5] Fault Specification")
print("-" * 65)

# Fault bus
fault_node_input = int(input("  Enter faulted bus node number (1 to N): "))
db.fault_node    = fault_node_input

# Fault type
print("  Fault types: LLLG | SLG | LL | DLG")
db.fault_type = input("  Enter fault type: ").strip().upper()

# Fault impedance (optional)
zf_input   = input("  Enter fault impedance Zf in pu [default 0.0]: ").strip()
db.fault_zf = float(zf_input) if zf_input else 0.0

print(f"\n  Fault: {db.fault_type} at bus {db.fault_node}, Zf = {db.fault_zf} pu")
print("-" * 65)


# =============================================================================
# STAGE 6 — FAULT ANALYSIS
# =============================================================================

print("\n[Stage 6] Computing fault currents...")
from FaultAnalysis import compute_fault
compute_fault()
print("[Stage 6] Complete.")


# =============================================================================
# STAGE 7 — RESULTS
# =============================================================================

print("\n[Stage 7] Results:")
from Results import print_fault_currents, print_postfault_voltages
print_fault_currents()
print_postfault_voltages()

print("  Short circuit analysis complete.")
print("=" * 65 + "\n")

# =============================================================================
# END OF SC.py
# =============================================================================
