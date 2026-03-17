import json

from report import generate_report
from noise_filter import filter_noise
from feature_mapper import extract_dynamic_features
from confidence import compute_confidence
from metrics import print_metrics
from visualize import visualize


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}


def extract_static_features(static_data):

    features = []

    rules = static_data.get("rules", {})

    for rule, data in rules.items():

        matches = data.get("matches", [])

        for match in matches:

            for feature in match.get("features", []):

                if feature.get("type") == "api":

                    features.append({
                        "capability": rule,
                        "api": feature.get("value")
                    })

    return features


def correlate(static_features, dynamic_features):
    """
    Correlation Layer (Post-Processing Stage)

    This operates on:
    - Static capa output (ResultDocument-like JSON)
    - Dynamic sandbox trace

    Uses semantic feature matching instead of address mapping.
    """

    results = []

    # --- semantic API matching ---
    dynamic_apis = {
        (f["value"], tuple(f.get("arguments", [])))
        for f in dynamic_features
    }

    # --- coverage estimation ---
    total_static = len(static_features)
    total_dynamic = len(dynamic_features)

    dynamic_coverage = total_dynamic / max(total_static, 1)

    for item in static_features:

        api = item["api"]
        capability = item["capability"]

        # semantic match (ignore args for now, but structure supports it)
        dynamic_present = any(api == dyn_api for dyn_api, _ in dynamic_apis)

        confidence = compute_confidence(
            static_present=True,
            dynamic_present=dynamic_present,
            dynamic_coverage=dynamic_coverage
        )

        # --- improved evidence classification ---
        if dynamic_present:
            evidence = "CONFIRMED_RUNTIME"
        else:
            if dynamic_coverage < 0.3:
                evidence = "INCONCLUSIVE_LOW_COVERAGE"
            else:
                evidence = "STATIC_ONLY_UNEXECUTED"

        results.append({
            "capability": capability,
            "api": api,
            "confidence": confidence,
            "evidence": evidence,

            # --- maintainer feedback: explicit correlation strategy ---
            "correlation_type": "semantic_api_match",

            # placeholder for future address mapping
            "address_mapping": "semantic_only"
        })

    return results


def main():

    print("Starting Static–Dynamic Correlation Prototype\n")

    static_data = load_json("data/static_output.json")
    trace = load_json("data/vmray_trace.json")

    if not static_data or not trace:
        print("Input data missing. Check JSON files.")
        return

    filtered_calls = filter_noise(trace)

    dynamic_features = extract_dynamic_features(filtered_calls)

    static_features = extract_static_features(static_data)

    print(f"\nStatic features extracted: {len(static_features)}")
    print(f"Dynamic features extracted: {len(dynamic_features)}")

    results = correlate(static_features, dynamic_features)

    if not results:
        print("\nNo correlated capabilities found.")
        return

    print("\nCorrelated Capability Analysis\n")

    for r in results:

        print(f"Capability: {r['capability']}")
        print(f"API: {r['api']}")
        print(f"Evidence: {r['evidence']}")
        print(f"Confidence: {r['confidence']}")
        print()

    print_metrics(results)

    try:
        visualize(results)
    except Exception as e:
        print("Visualization skipped:", e)


if __name__ == "__main__":
    main()