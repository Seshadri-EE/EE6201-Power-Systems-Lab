# =============================================================================
# SystemData.py
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
# Load Flow Analysis — Global Data Store
# =============================================================================
# DESCRIPTION:
#   This module acts as the single shared database for the entire load flow
#   program. All parsed network elements are stored here as module-level
#   lists, and all other files import directly from this module.
#
#   Because Python caches modules on first import, every file that imports
#   from SystemData shares the SAME objects in memory — not copies.
#   This means data populated in Reading.py is immediately visible to
#   Initialize.py, NetworkModel.py, and any subsequent modules.
#
# USAGE:
#   To access shared data in any file, simply import what you need:
#
#       import SystemData as db
#       db.buses.append(...)        # modify in-place
#       db.slack_node = 3           # update a scalar safely via module ref
#
#   OR for read-only list access:
#
#       from SystemData import buses, lines
#
#   NOTE: Always use 'import SystemData as db' when you need to
#   reassign a scalar (integer, float, string). Importing a scalar with
#   'from SystemData import slack_node' and then reassigning it
#   creates a local copy and will NOT update the shared value.
#
# WORKFLOW:
#   SystemData.py   ←  this file (global database)
#   NetworkClasses.py    ←  class definitions
#   Reading.py           ←  populates this database from the data file
#   Initialize.py        ←  reads this database, sets initial voltages
#   NetworkModel.py      ←  reads this database, builds Y_bus
# =============================================================================


# =============================================================================
# NETWORK ELEMENT LISTS
# =============================================================================
# These lists are populated by Reading.py.
# All subsequent modules read from these lists directly.

buses           = []    # List of Bus objects
transformers    = []    # List of Transformer objects
lines           = []    # List of TransmissionLine objects
shunt_reactors  = []    # List of ShuntReactor objects
loads           = []    # List of Load objects
generators      = []    # List of Generator objects


# =============================================================================
# SYSTEM CONSTANTS
# =============================================================================
# These scalars are used across multiple modules.
# Modify via 'import SystemData as db' then 'db.slack_node = N'.

slack_node  = 1      # Node number of the slack (reference) bus
base_mva    = 100    # System base MVA for per-unit conversion


# =============================================================================
# END OF SystemData.py
# =============================================================================
