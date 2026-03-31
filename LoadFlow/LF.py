# =============================================================================
# LF.py
# =============================================================================
#
# Course    : EE6201 - Power Systems Lab
# Institute : Indian Institute of Technology Hyderabad (IIT Hyderabad)
# Semester  : Spring 2026
# Assignment: Assignment 10
# Instructor: V. Seshadri Sravan Kumar, Dept. of Electrical Engineering
#
# Note      : The concepts, structure, and pedagogical ideas in this assignment
#             are original. The assignment template was developed with partial
#             assistance from an AI language model (Claude, Anthropic) for
#             formatting and scaffolding purposes.
#
# =============================================================================
# Load Flow Analysis — Main Driver
# =============================================================================
# DESCRIPTION:
#   Top-level script that drives the entire Newton-Raphson load flow solution.
#   Runs each stage in sequence and contains the main iterative loop.
#
# NEWTON-RAPHSON OVERVIEW:
#   Starting from an initial voltage guess, the method refines the solution
#   at each iteration until power mismatches fall below a tolerance:
#
#       1. Compute power at all buses           (NetworkState)
#       2. Check PV-PQ bus switching            (PVPQSwitch)
#       3. Compute power mismatch [ΔP; ΔQ]     (Mismatch)
#       4. Check convergence
#       5. Form Jacobian matrix J               (Jacobian)
#       6. Solve  J * Δx = mismatch            (Update)
#       7. Update bus voltages                  (Update)
#
# EXECUTION STAGES:
#   Stage 1 — Reading.py      : Parse data file
#   Stage 2 — Initialize.py   : Set initial voltages and bus types
#   Stage 3 — NetworkModel.py : Build Y-Bus matrix
#   Stage 4 — Main loop       : Newton-Raphson iterations
#   Stage 5 — Results.py      : Print converged solution
#
# =============================================================================

import SystemData as db


# =============================================================================
# IMPORTANT ASSUMPTIONS
# =============================================================================
# The following assumptions are made in this implementation. Violating any
# of them without appropriate code modifications will produce incorrect
# results.
#
# 1. NODE NUMBERING:
#    Buses are numbered sequentially from 1 to N with no missing numbers,
#    and bus 1 is always taken as the slack bus.
#    Array index = node number - 1  (bus 1 → index 0, bus N → index N-1).
#    Production codes must include a node renumbering module to handle
#    arbitrary and non-contiguous bus numbering. This should be inserted
#    as a pre-processing step before Stage 1.
#
# 2. LOAD MODEL — CONSTANT PQ:
#    All loads are modeled as constant PQ loads — active and reactive power
#    consumption is assumed fixed and independent of bus voltage magnitude.
#    As a consequence, P_spec is computed only ONCE before the loop and
#    never changes. Q_spec is also computed once but MAY be modified during
#    iterations if PV-PQ switching occurs (see Assumption 7).
#    If voltage-dependent load models are used, form_specified_values()
#    must be moved inside the iterative loop.
#
# 3. SINGLE SLACK BUS:
#    Exactly one slack bus is assumed, fixed at node 1. The slack bus
#    provides the voltage reference (|V| = 1.0 pu, δ = 0°) and absorbs
#    all active and reactive power mismatches in the network.
#
# 4. FLAT START INITIALISATION:
#    All PQ bus voltages are initialised to 1∠0° (flat start).
#    PV bus voltage magnitudes are set from generator data with angle 0°.
#    Poorly conditioned or heavily loaded systems may require a better
#    initial guess to ensure convergence.
#
# 5. TRANSFORMER MODEL:
#    Transformers are modeled using an ideal transformer with an off-nominal
#    tap ratio. Tap changers are assumed fixed and not adjusted during the
#    load flow solution.
#
# 6. LINE CHARGING:
#    Transmission lines are modeled using the standard pi-equivalent circuit.
#    The half line charging susceptance (b/2) at each end is included in
#    the Y-bus formation.
#
# 7. PV-PQ SWITCHING:
#    Generator buses (PV buses) are checked against reactive power limits
#    [Q_min, Q_max] at every iteration. A bus exceeding its limits is
#    switched to PQ with Q_spec fixed at the violated limit and the voltage
#    magnitude constraint is released. A switched bus is restored to PV if
#    Q_calc recovers within limits in a subsequent iteration.
#    Switching changes Npq and consequently the size of the mismatch vector
#    and the Jacobian — both are rebuilt after every switch.
# =============================================================================


# =============================================================================
# STAGE 1 — READ NETWORK DATA
# =============================================================================

print("=" * 60)
print("  EE6201 Power Systems Lab — Load Flow Analysis")
print("=" * 60)

print("\n[Stage 1] Reading network data...")
import Reading
print("[Stage 1] Complete.")


# =============================================================================
# STAGE 2 — INITIALIZE VOLTAGES
# =============================================================================

print("\n[Stage 2] Initializing bus voltages...")
import Initialize
print("[Stage 2] Complete.")


# =============================================================================
# STAGE 3 — BUILD Y-BUS MATRIX
# =============================================================================

print("\n[Stage 3] Building Y-Bus matrix...")
import NetworkModel
print("[Stage 3] Complete.")


# =============================================================================
# STAGE 4 — NEWTON-RAPHSON ITERATIVE LOOP
# =============================================================================

from Mismatch   import form_specified_values, compute_mismatch
from PVPQSwitch import check_pv_pq_switch
from Jacobian   import form_jacobian
from Update     import solve_linear_system, update_voltages
import NetworkState

# -----------------------------------------------------------------------------
# PRE-LOOP SETUP
# -----------------------------------------------------------------------------
# Form specified power vector ONCE — valid for constant PQ load model only.
# P_spec never changes. Q_spec may be modified by PV-PQ switching.

P_spec, Q_spec = form_specified_values()

MAX_ITER  = 50       # Maximum number of iterations allowed
TOLERANCE = 1e-6     # Convergence tolerance (per unit)
converged = False
iteration = 0

# -----------------------------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------------------------

print("\n[Stage 4] Starting Newton-Raphson iterations...")
print("-" * 60)
print(f"  {'Iter':<8} {'Max |ΔP| (pu)':<20} {'Max |ΔQ| (pu)':<20} {'Status'}")
print("-" * 60)

while iteration < MAX_ITER:

    iteration += 1

    # ------------------------------------------------------------------
    # STEP 1 — COMPUTE POWER AT ALL BUSES
    # ------------------------------------------------------------------
    db.state.compute_power()

    # ------------------------------------------------------------------
    # STEP 2 — CHECK PV-PQ SWITCHING
    # ------------------------------------------------------------------
    # Q_spec updated in-place for any switched bus.
    # Recompute power if any switch occurred.

    Q_spec, switched = check_pv_pq_switch(Q_spec)
    if switched:
        db.state.compute_power()

    # ------------------------------------------------------------------
    # STEP 3 — COMPUTE MISMATCH
    # ------------------------------------------------------------------
    # Vector length depends on current Npq (may have changed after switching).

    dP, dQ, mismatch_vector, max_dP, max_dQ = compute_mismatch(P_spec, Q_spec)

    # ------------------------------------------------------------------
    # STEP 4 — CHECK CONVERGENCE
    # ------------------------------------------------------------------

    status = "Converged" if (max_dP < TOLERANCE and max_dQ < TOLERANCE) else "Running..."
    print(f"  {iteration:<8} {max_dP:<20.6f} {max_dQ:<20.6f} {status}")

    if max_dP < TOLERANCE and max_dQ < TOLERANCE:
        converged = True
        break

    # ------------------------------------------------------------------
    # STEP 5 — FORM JACOBIAN
    # ------------------------------------------------------------------
    # Rebuilt every iteration — size reflects current Npq after switching.

    J = form_jacobian()

    # ------------------------------------------------------------------
    # STEP 6 — SOLVE  J * Δx = mismatch
    # ------------------------------------------------------------------

    dx = solve_linear_system(J, mismatch_vector)

    # ------------------------------------------------------------------
    # STEP 7 — UPDATE BUS VOLTAGES
    # ------------------------------------------------------------------
    # Angles updated for all non-slack buses.
    # Magnitudes updated for PQ buses only.
    # Slack bus never updated.

    update_voltages(dx)


# -----------------------------------------------------------------------------
# POST-LOOP REPORT
# -----------------------------------------------------------------------------

print("-" * 60)
if converged:
    print(f"\n  Solution converged in {iteration} iteration(s).")
else:
    print(f"\n  [WARNING] Solution did NOT converge after {MAX_ITER} iterations.")
    print(f"  Check network data or increase MAX_ITER.")


# =============================================================================
# STAGE 5 — RESULTS
# =============================================================================

from Results import print_bus_results, print_line_flows, print_summary

print("\n[Stage 5] Load Flow Results:")

db.state.compute_power()    # final power update at converged voltages

print_bus_results()
print_line_flows()
print_summary()

print("  Load flow analysis complete.")
print("=" * 60 + "\n")

# =============================================================================
# END OF LF.py
# =============================================================================
