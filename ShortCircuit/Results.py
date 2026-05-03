# =============================================================================
# Results.py
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
# Short Circuit Analysis — Results Output
# =============================================================================

import cmath
import numpy as np
import SystemData as db


def print_fault_currents():
    """
    Prints the sequence and phase fault currents at the faulted bus
    in both rectangular and polar form.
    """

    r = db.fault_results

    print("\n" + "=" * 65)
    print(f"  FAULT RESULTS — {r['fault_type']} fault at Bus {r['fault_node']}")
    print("=" * 65)

    print("\n  Sequence Fault Currents:")
    print(f"  {'':>6} {'Real (pu)':<16} {'Imag (pu)':<16} {'|I| (pu)':<12} {'Angle (deg)'}")
    print("  " + "-" * 60)

    for label, I in [('Ia0', r['Ia0']), ('Ia1', r['Ia1']), ('Ia2', r['Ia2'])]:
        if I is not None:
            mag   = abs(I)
            angle = cmath.phase(I) * 180 / cmath.pi
            print(f"  {label:<6} {I.real:<16.6f} {I.imag:<16.6f} {mag:<12.6f} {angle:.4f}")

    print("\n  Phase Fault Currents:")
    print(f"  {'':>6} {'Real (pu)':<16} {'Imag (pu)':<16} {'|I| (pu)':<12} {'Angle (deg)'}")
    print("  " + "-" * 60)

    for label, I in [('Ia', r['Ia']), ('Ib', r['Ib']), ('Ic', r['Ic'])]:
        if I is not None:
            mag   = abs(I)
            angle = cmath.phase(I) * 180 / cmath.pi
            print(f"  {label:<6} {I.real:<16.6f} {I.imag:<16.6f} {mag:<12.6f} {angle:.4f}")

    print("  " + "-" * 60)


def print_postfault_voltages():
    """
    Prints post-fault sequence and phase voltages at all buses.
    """

    r = db.fault_results

    print("\n  Post-Fault Bus Voltages:")
    print(f"  {'Node':<6} {'Name':<12} "
          f"{'|Va| (pu)':<12} {'∠Va (deg)':<12} "
          f"{'|Vb| (pu)':<12} {'|Vc| (pu)'}")
    print("  " + "-" * 70)

    # YOUR CODE STARTS HERE
    # Loop over db.buses and print post-fault voltages.
    # Use r['Va'], r['Vb'], r['Vc'] arrays indexed by bus position.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    print("  " + "-" * 70 + "\n")


# =============================================================================
# END OF Results.py
# =============================================================================
