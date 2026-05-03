# =============================================================================
# SystemData.py
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
# Short Circuit Analysis — Global Data Store
# =============================================================================
# DESCRIPTION:
#   This module acts as the single shared database for the entire short
#   circuit analysis program. All parsed network elements, sequence network
#   matrices, and fault results are stored here as module-level variables.
#
#   All other files import from this module using:
#       import SystemData as db
#
#   Because Python caches modules on first import, every file that imports
#   from SystemData shares the SAME objects in memory — not copies.
#
# WORKFLOW:
#   SystemData.py   ←  this file (global database)
#   NetworkClasses.py  ←  class definitions
#   Reading.py         ←  populates network element lists
#   Initialize.py      ←  sets initial bus voltages
#   NetworkModel.py    ←  builds sequence Y-bus matrices
#   ZBus.py            ←  inverts Y-bus to get Z-bus matrices
#   FaultAnalysis.py   ←  computes fault currents
#   SC.py              ←  main driver
# =============================================================================


# =============================================================================
# NETWORK ELEMENT LISTS
# =============================================================================
# Populated by Reading.py.

buses           = []    # List of Bus objects
transformers    = []    # List of Transformer objects
lines           = []    # List of TransmissionLine objects
shunt_reactors  = []    # List of ShuntReactor objects
loads           = []    # List of Load objects
generators      = []    # List of Generator objects


# =============================================================================
# SYSTEM CONSTANTS
# =============================================================================

slack_node  = 1         # Node number of the slack (reference) bus
base_mva    = 100       # System base MVA for per-unit conversion


# =============================================================================
# SEQUENCE Y-BUS MATRICES
# =============================================================================
# Populated by NetworkModel.py.
# Each is an instance of the YBus class for the respective sequence network.
#
# For this assignment:
#   Positive sequence = Negative sequence = Zero sequence
#   (same impedance data used for all three — see assumptions in SC.py)
#
# In a full implementation, each sequence would use different impedance data:
#   ybus_pos  — standard positive sequence network
#   ybus_neg  — negative sequence (same as positive for passive elements)
#   ybus_zero — zero sequence (depends on transformer winding connections
#               and line zero-sequence impedances — typically ~3x positive)

ybus_pos  = None    # Positive sequence Y-bus  (YBus object)
ybus_neg  = None    # Negative sequence Y-bus  (YBus object)
ybus_zero = None    # Zero sequence Y-bus      (YBus object)


# =============================================================================
# SEQUENCE Z-BUS MATRICES
# =============================================================================
# Populated by ZBus.py.
# Obtained by inverting the corresponding Y-bus matrices.
#
# NOTE: Direct inversion is used here for simplicity. In production codes,
# the Z-bus building algorithm (Kron reduction) is preferred for large
# networks as it is computationally more efficient.

zbus_pos  = None    # Positive sequence Z-bus  (numpy complex matrix)
zbus_neg  = None    # Negative sequence Z-bus  (numpy complex matrix)
zbus_zero = None    # Zero sequence Z-bus      (numpy complex matrix)


# =============================================================================
# INITIAL VOLTAGES
# =============================================================================
# Set by Initialize.py.
# Pre-fault voltage at each bus used as the Thevenin source in fault analysis.
#
# For this assignment: flat start (1∠0° at all buses).
# Ideal approach: run load flow first (Assignment 10) and use converged
# voltages as pre-fault conditions. See Initialize.py for details.

V0 = None       # numpy array of pre-fault complex voltages (size N)


# =============================================================================
# FAULT SPECIFICATION
# =============================================================================
# Set by user input in SC.py before FaultAnalysis.py is called.

fault_node  = None  # Integer — bus node number where fault is applied
fault_type  = None  # String  — 'LLLG', 'SLG', 'LL', or 'DLG'
fault_zf    = 0.0   # Fault impedance in per unit (default: bolted fault = 0)


# =============================================================================
# FAULT RESULTS
# =============================================================================
# Populated by FaultAnalysis.py after the fault is computed.

fault_results = None    # dict — fault currents and voltages (see FaultAnalysis.py)


# =============================================================================
# END OF SystemData.py
# =============================================================================
