Capa Dynamic Correlation Prototype

Overview

This repository contains a prototype that explores how dynamic analysis results can be used to confirm and strengthen static capability matches in capa.

The prototype combines:
	•	static rule matches (capa-like output)
	•	dynamic sandbox traces (VMRay-style)

to produce a unified view of capabilities with confidence scoring.

---

Motivation

Capa currently produces static and dynamic results separately.
In practice, analysts use runtime behaviour to verify whether a static match represents real behaviour.

This prototype explores a simple correlation layer that bridges this gap.

---

Key Ideas

Semantic Correlation

Instead of relying on virtual addresses (unreliable due to ASLR), the prototype matches:
	•	static: api(CreateFileA)
	•	dynamic: CreateFileA("C:\temp\file.txt")

using feature-level matching.

---

Coverage-Aware Confidence

Capabilities are classified as:
	•	CONFIRMED_RUNTIME → observed during execution
	•	STATIC_ONLY_UNEXECUTED → not observed, but may be unexecuted code
	•	INCONCLUSIVE_LOW_COVERAGE → insufficient runtime coverage

---

Noise Filtering

Sandbox noise (e.g. explorer.exe, system) is filtered to focus on relevant behaviour.

---

Example Output:

<img width="501" height="489" alt="image" src="https://github.com/user-attachments/assets/19dbb2c2-8721-4a78-b4c4-a33127ba2eb8" />




---

Visualization

The prototype generates a simple hierarchical graph:

capability → OR → API features

Saved to:

output/graph.png

<img width="896" height="710" alt="image" src="https://github.com/user-attachments/assets/074f64c0-a978-4dd3-a0b0-3ed610433eeb" />




---

How to Run

pip install -r requirements.txt
python correlate.py


---

Repository Structure

.
├── correlate.py          # main pipeline
├── confidence.py         # confidence model
├── feature_mapper.py     # dynamic feature extraction
├── noise_filter.py       # sandbox noise filtering
├── metrics.py            # evaluation metrics
├── visualize.py          # graph generation
├── data/                 # sample inputs


---

Design Notes
	•	Correlation is implemented as a post-processing step
	•	No modification to Capa’s core engine
	•	Focuses on validating feasibility, not full integration

---

Future Work
	•	Integrate with capa ResultDocument
	•	Extend beyond API-level to rule-level correlation
	•	Explore symbol-based or rebased address mapping
	•	Integrate into Ghidra UI

---

Status

Prototype / Proof of Concept

---

Related

This work is part of a GSoC proposal exploring improvements to Capa’s dynamic analysis.
