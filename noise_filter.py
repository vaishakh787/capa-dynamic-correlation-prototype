NOISE_PROCESSES = ["explorer.exe", "system", "svchost.exe"]


def filter_noise(trace):

    total = len(trace["calls"])
    filtered = []

    for call in trace["calls"]:
        process = call.get("process")

        if process not in NOISE_PROCESSES:
            filtered.append(call)

    removed = total - len(filtered)

    print("\nSandbox Noise Filtering")
    print("Total events:", total)
    print("Noise removed:", removed)
    print("Relevant events:", len(filtered))

    return filtered