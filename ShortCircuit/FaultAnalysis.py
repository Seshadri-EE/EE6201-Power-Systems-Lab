# =============================================================================
# FaultAnalysis.py
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
# Short Circuit Analysis — Fault Current Calculation
# =============================================================================
# DESCRIPTION:
#   This module computes fault currents and post-fault bus voltages for
#   four types of shunt faults at a specified bus using sequence network
#   theory (method of symmetrical components).
#
#   Fault types supported:
#       LLLG — Three-phase to ground (balanced fault)
#       SLG  — Single line to ground
#       LL   — Line to line
#       DLG  — Double line to ground
#
# THEORY — SYMMETRICAL COMPONENTS:
#   Let k  = faulted bus index (= fault_node - 1)
#   Let Zf = fault impedance (pu)
#   Let V0_k = pre-fault voltage at bus k (from db.V0[k])
#
#   Key Z-bus elements at faulted bus k:
#       Z1_kk = db.zbus_pos[k, k]    (positive sequence Thevenin impedance)
#       Z2_kk = db.zbus_neg[k, k]    (negative sequence Thevenin impedance)
#       Z0_kk = db.zbus_zero[k, k]   (zero sequence Thevenin impedance)
#
# -----------------------------------------------------------------------
# FAULT TYPE FORMULAS:
# -----------------------------------------------------------------------
#
#   1. THREE-PHASE (LLLG) — Balanced fault, only positive sequence:
#
#       Ia1 = V0_k / (Z1_kk + Zf)
#       Ia2 = 0
#       Ia0 = 0
#
#       Fault current (phase a):
#           Ia = Ia1  (in pu)
#
# -----------------------------------------------------------------------
#   2. SINGLE LINE TO GROUND (SLG) — Phase a to ground:
#
#       Ia1 = Ia2 = Ia0 = V0_k / (Z1_kk + Z2_kk + Z0_kk + 3*Zf)
#
#       Fault current (phase a):
#           Ia = 3 * Ia1
#       Ib = Ic = 0
#
# -----------------------------------------------------------------------
#   3. LINE TO LINE (LL) — Phase b to phase c (no ground):
#
#       Ia1 = V0_k / (Z1_kk + Z2_kk + Zf)
#       Ia2 = -Ia1
#       Ia0 = 0
#
#       Let a = e^(j*2π/3)  (symmetrical component operator)
#
#       Phase currents:
#           Ia = 0
#           Ib = (a^2 - a) * Ia1
#           Ic = (a - a^2) * Ia1
#
# -----------------------------------------------------------------------
#   4. DOUBLE LINE TO GROUND (DLG) — Phase b and c to ground:
#
#       Ia1 = V0_k / (Z1_kk + Z2_kk*(Z0_kk + 3*Zf) / (Z2_kk + Z0_kk + 3*Zf))
#       Ia2 = -Ia1 * (Z0_kk + 3*Zf) / (Z2_kk + Z0_kk + 3*Zf)
#       Ia0 = -Ia1 * Z2_kk           / (Z2_kk + Z0_kk + 3*Zf)
#
#       Phase currents via symmetrical components:
#           Ia = Ia0 + Ia1 + Ia2  = 0
#           Ib = Ia0 + a^2*Ia1 + a*Ia2
#           Ic = Ia0 + a*Ia1   + a^2*Ia2
#
# -----------------------------------------------------------------------
# POST-FAULT BUS VOLTAGES (all buses):
# -----------------------------------------------------------------------
#   After finding sequence fault currents, post-fault voltages at all
#   buses i can be computed using the Z-bus:
#
#       V1_i = V0_i  -  Z1_ik * Ia1      (positive sequence)
#       V2_i =        - Z2_ik * Ia2      (negative sequence)
#       V0_i =        - Z0_ik * Ia0      (zero sequence)
#
#   where Z1_ik = db.zbus_pos[i, k], etc.
#
#   Phase voltages:
#       Va_i = V0_i + V1_i + V2_i
#       Vb_i = V0_i + a^2*V1_i + a*V2_i
#       Vc_i = V0_i + a*V1_i   + a^2*V2_i
#
# DEPENDENCIES:
#   SystemData.py  — db.zbus_pos, db.zbus_neg, db.zbus_zero, db.V0
#   ZBus.py        — must be run first
# =============================================================================

import numpy as np
import cmath
import SystemData as db

# Symmetrical component operator a = e^(j*2π/3)
a = cmath.exp(1j * 2 * cmath.pi / 3)


# =============================================================================
# FUNCTION: compute_fault
# =============================================================================

def compute_fault():
    """
    Computes fault currents and post-fault bus voltages for the fault
    specified in db.fault_node, db.fault_type, and db.fault_zf.

    Returns:
        results : dict containing:
            'fault_node'    : faulted bus node number
            'fault_type'    : fault type string
            'Ia0', 'Ia1', 'Ia2' : sequence fault currents (pu)
            'Ia', 'Ib', 'Ic'    : phase fault currents (pu)
            'V_seq'             : dict of sequence voltages at all buses
            'V_phase'           : dict of phase voltages at all buses
    """

    k  = db.fault_node - 1              # faulted bus array index
    Zf = db.fault_zf                    # fault impedance (pu)
    V0 = db.V0[k]                       # pre-fault voltage at faulted bus

    Z1kk = db.zbus_pos[k, k]
    Z2kk = db.zbus_neg[k, k]
    Z0kk = db.zbus_zero[k, k]

    # ------------------------------------------------------------------
    fault_type = db.fault_type.upper()
    # ------------------------------------------------------------------

    if fault_type == 'LLLG':
        Ia0, Ia1, Ia2 = compute_LLLG(V0, Z1kk, Zf)

    elif fault_type == 'SLG':
        Ia0, Ia1, Ia2 = compute_SLG(V0, Z1kk, Z2kk, Z0kk, Zf)

    elif fault_type == 'LL':
        Ia0, Ia1, Ia2 = compute_LL(V0, Z1kk, Z2kk, Zf)

    elif fault_type == 'DLG':
        Ia0, Ia1, Ia2 = compute_DLG(V0, Z1kk, Z2kk, Z0kk, Zf)

    else:
        raise ValueError(f"Unknown fault type '{db.fault_type}'. "
                         f"Choose from: LLLG, SLG, LL, DLG")

    # ------------------------------------------------------------------
    # PHASE FAULT CURRENTS
    # ------------------------------------------------------------------

    # YOUR CODE STARTS HERE
    # Compute phase currents Ia, Ib, Ic from sequence currents Ia0, Ia1, Ia2.
    # Use the symmetrical component transformation:
    #     Ia = Ia0 + Ia1 + Ia2
    #     Ib = Ia0 + a^2 * Ia1 + a * Ia2
    #     Ic = Ia0 + a   * Ia1 + a^2 * Ia2

    Ia = None  # Replace with your computation
    Ib = None
    Ic = None

    # YOUR CODE ENDS HERE

    # ------------------------------------------------------------------
    # POST-FAULT BUS VOLTAGES
    # ------------------------------------------------------------------

    V1_buses, V2_buses, V0_buses = compute_postfault_voltages(k, Ia0, Ia1, Ia2)

    # ------------------------------------------------------------------
    # PHASE VOLTAGES AT ALL BUSES
    # ------------------------------------------------------------------

    # YOUR CODE STARTS HERE
    # Compute Va, Vb, Vc at each bus from sequence voltages.
    # Store as numpy arrays.
    #
    # HINT:
    #     Va = V0_buses + V1_buses + V2_buses
    #     Vb = V0_buses + (a**2)*V1_buses + a*V2_buses
    #     Vc = V0_buses + a*V1_buses + (a**2)*V2_buses

    Va = None  # Replace with your computation
    Vb = None
    Vc = None

    # YOUR CODE ENDS HERE

    # ------------------------------------------------------------------
    # PACKAGE RESULTS
    # ------------------------------------------------------------------

    db.fault_results = {
        'fault_node' : db.fault_node,
        'fault_type' : db.fault_type,
        'Ia0'        : Ia0,
        'Ia1'        : Ia1,
        'Ia2'        : Ia2,
        'Ia'         : Ia,
        'Ib'         : Ib,
        'Ic'         : Ic,
        'V1_buses'   : V1_buses,
        'V2_buses'   : V2_buses,
        'V0_buses'   : V0_buses,
        'Va'         : Va,
        'Vb'         : Vb,
        'Vc'         : Vc,
    }

    return db.fault_results


# =============================================================================
# FAULT TYPE FUNCTIONS
# =============================================================================

def compute_LLLG(V0, Z1kk, Zf):
    """
    Three-phase to ground fault (balanced).
    Only positive sequence current flows.

        Ia1 = V0 / (Z1kk + Zf)
        Ia2 = 0
        Ia0 = 0
    """

    # YOUR CODE STARTS HERE
    # Compute Ia1, Ia2, Ia0 using the formula above.
    # Return Ia0, Ia1, Ia2.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE


def compute_SLG(V0, Z1kk, Z2kk, Z0kk, Zf):
    """
    Single line to ground fault (phase a to ground).
    All three sequence currents are equal.

        Ia1 = Ia2 = Ia0 = V0 / (Z1kk + Z2kk + Z0kk + 3*Zf)
    """

    # YOUR CODE STARTS HERE

    pass

    # YOUR CODE ENDS HERE


def compute_LL(V0, Z1kk, Z2kk, Zf):
    """
    Line to line fault (phase b to phase c, no ground).

        Ia1 =  V0 / (Z1kk + Z2kk + Zf)
        Ia2 = -Ia1
        Ia0 =  0
    """

    # YOUR CODE STARTS HERE

    pass

    # YOUR CODE ENDS HERE


def compute_DLG(V0, Z1kk, Z2kk, Z0kk, Zf):
    """
    Double line to ground fault (phase b and c to ground).

        Ia1 = V0 / (Z1kk + Z2kk*(Z0kk + 3*Zf) / (Z2kk + Z0kk + 3*Zf))
        Ia2 = -Ia1 * (Z0kk + 3*Zf) / (Z2kk + Z0kk + 3*Zf)
        Ia0 = -Ia1 * Z2kk           / (Z2kk + Z0kk + 3*Zf)
    """

    # YOUR CODE STARTS HERE

    pass

    # YOUR CODE ENDS HERE


# =============================================================================
# POST-FAULT VOLTAGE FUNCTION
# =============================================================================

def compute_postfault_voltages(k, Ia0, Ia1, Ia2):
    """
    Computes post-fault sequence voltages at all buses.

    For each bus i:
        V1_i = V0_i  -  Z1_ik * Ia1
        V2_i =        - Z2_ik * Ia2
        V0_i =        - Z0_ik * Ia0

    Parameters:
        k    : faulted bus index (integer)
        Ia0, Ia1, Ia2 : sequence fault currents (complex)

    Returns:
        V1_buses, V2_buses, V0_buses : numpy arrays of size N
    """

    # YOUR CODE STARTS HERE
    # Use db.zbus_pos[:, k], db.zbus_neg[:, k], db.zbus_zero[:, k]
    # to compute post-fault sequence voltages at all buses.
    #
    # HINT — vectorized form:
    #     V1_buses = db.V0 - db.zbus_pos[:, k] * Ia1
    #     V2_buses =       - db.zbus_neg[:, k] * Ia2
    #     V0_buses =       - db.zbus_zero[:, k] * Ia0

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE


# =============================================================================
# END OF FaultAnalysis.py
# =============================================================================
