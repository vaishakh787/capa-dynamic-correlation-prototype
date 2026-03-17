def print_metrics(results):

    confirmed = sum(1 for r in results if r["evidence"] == "CONFIRMED_RUNTIME")

    static_only = sum(
        1 for r in results
        if r["evidence"] in ("STATIC_ONLY_UNEXECUTED", "INCONCLUSIVE_LOW_COVERAGE")
    )

    total = len(results)

    print("\nCorrelation Summary")

    print(f"Capabilities confirmed by runtime: {confirmed}")
    print(f"Static-only or unexecuted capabilities: {static_only}")

    if total > 0:
        coverage = confirmed / total
        print(f"Runtime coverage: {coverage:.2f}")
        print("Note: static-only capabilities may correspond to unexecuted code paths.")