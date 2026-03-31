# =============================================================================
# NetworkState.py
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
# Load Flow Analysis — Network State
# =============================================================================
# DESCRIPTION:
#   This module defines the NetworkState class, which represents the complete
#   electrical state of the power system at any point during the solution.
#
#   The "state" of a power system is fully described by the complex voltage
#   at every bus — magnitude |V| and angle delta. From these voltages, all
#   other quantities (P, Q, line flows, losses) can be derived.
#
#   This class is designed to serve two purposes:
#
#       1. LOAD FLOW (current):
#          Compute P and Q at each bus from current voltage estimates.
#          Used inside the Newton-Raphson loop to evaluate mismatches.
#
#       2. STATE ESTIMATION (future):
#          Incorporate measurement data (with noise) and solve the
#          Weighted Least Squares (WLS) problem to estimate the true
#          system state. Residuals, covariance, and observability
#          analysis will all be added here in a future assignment.
#
# DEPENDENCIES:
#   SystemData.py   — shared global database (db.buses, db.ybus)
#   NetworkModel.py — must be run first to populate db.ybus
#
# WORKFLOW:
#   Reading.py  ->  Initialize.py  ->  NetworkModel.py  ->  NetworkState.py
#                                                                 |
#                                                              LF.py (loop)
# =============================================================================

import numpy as np
import SystemData as db


# =============================================================================
# CLASS: NetworkState
# =============================================================================

class NetworkState:
    """
    Represents the complete electrical state of the power system.

    Attributes:
        V  : numpy array of complex bus voltages (N,)
        P  : numpy array of calculated active power at each bus (N,)
        Q  : numpy array of calculated reactive power at each bus (N,)
        N  : number of buses

    Future attributes (State Estimation):
        z        : measurement vector
        h        : calculated measurement vector
        residual : z - h
        W        : weighting matrix (inverse of covariance)
    """

    def __init__(self):
        """
        Initializes the NetworkState from the current bus voltages in db.
        Extracts the voltage vector and sets up P and Q arrays.
        """

        self.N = len(db.buses)

        # ---------------------------------------------------------------------
        # VOLTAGE STATE VECTOR
        # ---------------------------------------------------------------------
        # Extract complex voltages from all buses into a single numpy array.
        # Index order matches db.ybus.node_index for consistency.

        self.V = np.array([bus.V for bus in db.buses], dtype=complex)

        # ---------------------------------------------------------------------
        # POWER ARRAYS
        # ---------------------------------------------------------------------
        # Initialized to zero — populated by compute_power()

        self.P = np.zeros(self.N)
        self.Q = np.zeros(self.N)

    # =========================================================================
    # REFRESH VOLTAGE VECTOR
    # =========================================================================

    def update_voltages(self):
        """
        Refreshes self.V from the current bus voltages in db.buses.
        Called at the start of each Newton-Raphson iteration after
        voltages have been updated.
        """
        self.V = np.array([bus.V for bus in db.buses], dtype=complex)

    # =========================================================================
    # COMPUTE POWER AT ALL BUSES
    # =========================================================================

    def compute_power(self):
        """
        Computes the net injected active power P and reactive power Q
        at every bus using the current voltage state.

        Power Flow Equations:
        ---------------------
        For bus i, the net injected power is:

            P_i = sum_{j=1}^{N} |V_i||V_j| [ G_ij cos(di - dj)
                                             + B_ij sin(di - dj) ]

            Q_i = sum_{j=1}^{N} |V_i||V_j| [ G_ij sin(di - dj)
                                             - B_ij cos(di - dj) ]

        where:
            |V_i|, |V_j| : voltage magnitudes at buses i and j
            di,   dj     : voltage angles at buses i and j
            G_ij         : real part      of Y_bus[i, j]  (conductance)
            B_ij         : imaginary part of Y_bus[i, j]  (susceptance)

        -----------------------------------------------------------------
        COMPACT FORM (recommended):
        -----------------------------------------------------------------
        The double summation above can be written compactly using
        complex arithmetic. For all buses simultaneously:

            S = V * conj(Y_bus @ V)

        where:
            S      : complex power vector (N,),  S = P + jQ
            V      : complex voltage vector (N,)
            Y_bus  : complex admittance matrix (N x N)
            conj() : element-wise complex conjugate
            @      : matrix-vector multiplication

        This single expression replaces the entire double summation
        and is fully vectorized. Try to implement this form first.

        -----------------------------------------------------------------
        EFFICIENCY HINT:
        -----------------------------------------------------------------
        In numpy this becomes just three lines:

            Y    = db.ybus.Y_bus           # (N x N) complex matrix
            S    = self.V * np.conj(Y @ self.V)   # (N,) complex power

            self.P = S.real                # active power (pu)
            self.Q = S.imag                # reactive power (pu)

        If you are not yet comfortable with the compact form, you may
        implement the explicit double summation using the trigonometric
        expressions above — both approaches are correct. Think about
        which is cleaner, and why they are equivalent.
        -----------------------------------------------------------------

        Output:
        -------
            Updates self.P and self.Q in-place.
            Values are in per unit on the system base (db.base_mva).
        """

        # YOUR CODE STARTS HERE
        # Compute P and Q at all buses from the current voltage vector
        # and the Y_bus matrix. Update self.P and self.Q.
        #
        # Recommended:
        #   Y      = db.ybus.Y_bus
        #   S      = self.V * np.conj(Y @ self.V)
        #   self.P = S.real
        #   self.Q = S.imag

        pass  # Remove this line once you add your code

        # YOUR CODE ENDS HERE

    # =========================================================================
    # DISPLAY
    # =========================================================================

    def print_power(self):
        """
        Prints the calculated P and Q at each bus in a formatted table.
        """
        print("\n--- Calculated Bus Power ---")
        print(f"  {'Node':<6} {'Name':<12} {'Type':<6} {'P (pu)':<12} {'Q (pu)':<12}")
        print("  " + "-" * 56)

        for idx, bus in enumerate(db.buses):
            print(f"  {bus.node:<6} {bus.description:<12} {bus.bus_type:<6} "
                  f"{self.P[idx]:<12.6f} {self.Q[idx]:<12.6f}")

        print("  " + "-" * 56 + "\n")


# =============================================================================
# INSTANTIATE AND STORE IN GLOBAL DATABASE
# =============================================================================
# The NetworkState object is stored in db so LF.py and future modules
# (including State Estimation) can access the current system state via
# db.state.

db.state = NetworkState()

# =============================================================================
# END OF NetworkState.py
# =============================================================================
