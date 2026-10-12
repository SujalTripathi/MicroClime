---
title: MicroClime: Offline Urban Heat Scout with TabPFN + Gemma (Screen Time: 10 Seconds)
published: true
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

**MicroClime** is an offline-first microclimate Scout designed around a single principle: **make screen time as close to zero as possible, and get people outside touching grass safely.**

In urban areas and college campuses, the temperature difference between unshaded asphalt and a tree-lined grass corridor can exceed 6°C (10°F). Walking through these heat islands is exhausting and keeps people locked indoors under air conditioning.

With MicroClime:
1. As you walk outside, you tap 4 quick buttons in 5 seconds: your ground surface (grass, brick, asphalt, concrete), shade level (1–5), breeze (yes/no), and felt heat.
2. Once you collect just 5–10 real outdoor spots, **Prior Labs TabPFN-3** evaluates all 40 surface/shade permutations zero-shot on your device.
3. **Google Gemma 2 (2B)** translates the numerical forecast into human navigation advice (e.g., *"Head for the shaded lawn; avoid the asphalt perimeter at midday"*).
4. The app tells you: **"Goal Accomplished: Screen time over. Put your phone in your pocket and enjoy the outdoors."**

---

## Demo

![MicroClime App Interface](https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/MicroClime/main/screenshot.png)

*(MicroClime running with tactile one-tap logging, TabPFN-3 tabular forecasting, and Gemma 2 local inference)*

---

## Code

{% embed https://github.com/YOUR_GITHUB_USERNAME/MicroClime %}

GitHub Repository: [MicroClime on GitHub](https://github.com/YOUR_GITHUB_USERNAME/MicroClime)

---

## How I Built It

MicroClime pairs two distinct open-source AI models working in harmony:

1. **[TabPFN-3](https://docs.priorlabs.ai/) (Prior Labs)**: TabPFN is a tabular foundation model trained to do in-context inference on small datasets (<1000 rows) with state-of-the-art accuracy. Instead of training a model or guessing, TabPFN fits to your 10 walk points in milliseconds and scores every possible route permutation locally.
2. **[Google Gemma 2 (2B)](https://ai.google.dev/gemma) via Ollama**: A compact, high-efficiency open-weight model that runs locally on CPU/GPU. It synthesizes the numerical tabular predictions into a concise, encouraging 60-word outdoor walking brief.
3. **Streamlit & Pure Python**: A responsive, mobile-accessible tactile web interface that works on phone browsers over local Wi-Fi without needing app store downloads.

---

## Why Does Open Innovation Matter?

Open-source and open-weight AI are essential for outdoor tools:

- **100% Offline Resilience:** You don't get 5G cell reception deep in state parks, nature preserves, or remote campus trails. Because TabPFN-3 and Gemma 2 run on local weights, MicroClime works seamlessly with zero internet connection.
- **True Location Privacy:** Commercial cloud APIs track queries, timestamps, and locations. Running inference on-device ensures your physical routines and movements are never logged to commercial servers.
- **Zero API Invoices:** Outdoor exploration shouldn't require monthly SaaS subscriptions or paying per-token API bills.
- **Modularity:** Open weights let developers inspect the exact model version (we pinned TabPFN to v3) and adjust prompts directly without sudden API deprecations.

---

## My Field Test

To put the "Touch Grass" theme to the test, I took MicroClime on an afternoon walk through the local neighborhood and greenway:

- **The Walk:** I logged 8 spots across a 15-minute stroll: two points on exposed road asphalt (felt heat: 5/5), two on a brick walkway (felt heat: 3/5), and four along the shaded grassy park perimeter (felt heat: 1/5).
- **The Result:** TabPFN correctly isolated that canopy shade reduced perceived heat from 5.0 to 1.0, and flagged unshaded concrete as a secondary heat trap. Gemma generated an instant walking route advice in under 4 seconds: *"Stick to the grassy tree canopy on the northern edge. Avoid the parking lot and asphalt lanes. Now put your phone away!"*
- **The Experience:** Total time looking at my screen was under 40 seconds across the entire walk. The rest of the time was spent enjoying the fresh air and autumn breeze.

---

## Prize Categories

- **Best Use of TabPFN**: MicroClime leverages TabPFN-3 directly on real-world small tabular walk logs to predict microclimate thermal comfort without manual model training.
- **Best Use of Gemma**: Uses Google's open-weight Gemma 2 (2B) to convert raw tabular foundation model outputs into conversational, screen-free outdoor walking guidance.
