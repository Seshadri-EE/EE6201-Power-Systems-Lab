# =============================================================================
# Reading.py
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
# Short Circuit Analysis — Data File Reader
# =============================================================================
# OBJECTIVE:
#   Read and parse power system network data from the structured data file
#   (Data.d1) and populate the shared global database in SystemData.py.
#
# RECORD CODES:
#   BS  - Bus
#   TR  - Transformer
#   TL  - Transmission Line
#   DZ  - Shunt Reactor
#   DP  - Load
#   GP  - Generator
#   XX  - Non-active record (skipped)
#   #   - Comment line (skipped)
#
# DATA ACKNOWLEDGEMENT:
#   The network data file (Data.d1) was originally received by
#   V. Seshadri Sravan Kumar during his PhD studies at the Indian Institute
#   of Science (IISc), Bangalore, from Prof. D. Thukaram, Department of
#   Electrical Engineering, IISc. Full credit to Prof. Thukaram.
#
# NODE NUMBERING ASSUMPTION:
#   See SC.py for the full list of assumptions.
#
# DEPENDENCIES:
#   SystemData.py     — global database (populated here)
#   NetworkClasses.py — class definitions
# =============================================================================

import SystemData as db
from NetworkClasses import Bus, Transformer, TransmissionLine, ShuntReactor, Load, Generator


# =============================================================================
# FILE INPUT
# =============================================================================

filename = input("Enter the input data filename (e.g., Data/Data.d1): ")


# =============================================================================
# FILE READING AND PARSING
# =============================================================================

try:
    with open(filename, 'r') as f:

        for line in f:

            line = line.strip()
            if not line or line.startswith('#'):
                continue

            tokens = line.split()
            code   = tokens[0]

            # ------------------------------------------------------------------
            if code == 'BS':
                # BUS RECORD
                # Format: BS  <zone>  <description>  <node>  <voltage>
                #
                # YOUR CODE STARTS HERE
                # 1. Extract zone, description, node, voltage from tokens.
                # 2. Create a Bus object.
                # 3. Append to db.buses.
                # HINT: tokens[1]=zone, tokens[2]=description,
                #       tokens[3]=node, tokens[4]=voltage

                pass  # Remove this line once you add your code

                # YOUR CODE ENDS HERE

            # ------------------------------------------------------------------
            elif code == 'TR':
                # TRANSFORMER RECORD
                # Format: TR  <zone>  <desc>  <from>  <to>  <r>  <x>  <tap>  <max_loading>
                #
                # YOUR CODE STARTS HERE

                pass

                # YOUR CODE ENDS HERE

            # ------------------------------------------------------------------
            elif code == 'TL':
                # TRANSMISSION LINE RECORD
                # Format: TL  <zone>  <desc>  <from>  <to>  <r>  <x>  <b_half>  <max_loading>
                #
                # YOUR CODE STARTS HERE

                pass

                # YOUR CODE ENDS HERE

            # ------------------------------------------------------------------
            elif code == 'DZ':
                # SHUNT REACTOR RECORD
                # Format: DZ  <zone>  <desc>  <node>  <r>  <x>
                #
                # YOUR CODE STARTS HERE

                pass

                # YOUR CODE ENDS HERE

            # ------------------------------------------------------------------
            elif code == 'DP':
                # LOAD RECORD
                # Format: DP  <zone>  <desc>  <node>  <P>  <Q>  <compensation>
                #
                # YOUR CODE STARTS HERE

                pass

                # YOUR CODE ENDS HERE

            # ------------------------------------------------------------------
            elif code == 'GP':
                # GENERATOR RECORD
                # Format: GP  <zone>  <desc>  <node>  <P>  <Q_max>  <Q_min>  <V_setpoint>
                #
                # YOUR CODE STARTS HERE

                pass

                # YOUR CODE ENDS HERE

            # ------------------------------------------------------------------
            elif code == 'XX':
                # Non-active record — skip silently
                continue

            else:
                print(f"  [WARNING] Unknown record code '{code}' — skipping line.")

except FileNotFoundError:
    print(f"[ERROR] File '{filename}' not found. Please check the filename and try again.")


# =============================================================================
# SUMMARY OUTPUT
# =============================================================================

print("\n--- Network Data Summary ---")
print(f"  Buses             : {len(db.buses)}")
print(f"  Transformers      : {len(db.transformers)}")
print(f"  Transmission Lines: {len(db.lines)}")
print(f"  Shunt Reactors    : {len(db.shunt_reactors)}")
print(f"  Loads             : {len(db.loads)}")
print(f"  Generators        : {len(db.generators)}")
print("----------------------------\n")

# =============================================================================
# END OF Reading.py
# =============================================================================
