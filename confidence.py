def compute_confidence(static_present, dynamic_present, dynamic_coverage=0.0):
    """
    Improved confidence model addressing coverage gap.

    static_present: static rule matched
    dynamic_present: runtime confirmation exists
    dynamic_coverage: how much of static space was exercised
    """

    # strong confirmation
    if static_present and dynamic_present:
        return 0.9

    # static only → depends on coverage
    if static_present and not dynamic_present:
        if dynamic_coverage < 0.3:
            return 0.6  # low coverage → inconclusive
        else:
            return 0.3  # high coverage → likely unexecuted

    return 0.0