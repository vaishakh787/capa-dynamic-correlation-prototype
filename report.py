def generate_report(results):

    confirmed = [r for r in results if r["evidence"] == "CONFIRMED_RUNTIME"]

    static_only = [
        r for r in results
        if r["evidence"] in ("STATIC_ONLY_UNEXECUTED", "INCONCLUSIVE_LOW_COVERAGE")
    ]

    print("\nAnalysis Report")

    print("\nConfirmed Capabilities:")
    for r in confirmed:
        print(f"- {r['capability']} ({r['api']})")

    print("\nUnconfirmed / Static-Only Capabilities:")
    for r in static_only:
        print(f"- {r['capability']} ({r['api']})")