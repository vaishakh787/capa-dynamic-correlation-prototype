def extract_dynamic_features(calls):

    features = []

    for call in calls:

        api = call.get("api")

        feature = {
            "type": "api",
            "value": api
        }

        # include runtime arguments if available
        if "arguments" in call:
            feature["arguments"] = call["arguments"]

        features.append(feature)

    return features