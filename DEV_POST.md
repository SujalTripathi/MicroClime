---
title: MicroClime: Find the Coolest Path on Your Walk with TabPFN + Gemma (Screen Time: 10 Seconds)
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

**MicroClime** helps you pick the most comfortable outdoor path, using nothing but a few quick taps while you walk.

Every few minutes you log a spot: ground type (asphalt, concrete, brick, grass), shade (1-5), breeze (yes/no), and how hot it felt (1-5). After about 5 spots, a tabular foundation model predicts how every surface/shade/breeze combination will feel, and a local LLM turns that into a short, plain-English tip like *"head for the shaded grass, avoid the sunny asphalt."*

The screen is the shortest part of the experience: ~5 seconds per log, ~10 seconds for the answer. Then you put the phone away and walk.

**Who it's for:** anyone who walks, runs or studies outside in the heat: students crossing a campus, run clubs picking a route, people in cities with heat-island streets.

## Demo

<!-- TODO: add screenshot/GIF of the app at http://localhost:8501 and a photo from your real walk -->

## Code

<!-- TODO: embed your GitHub repo: {% embed https://github.com/YOUR_USER/YOUR_REPO %} -->

## How I Built It

- **[TabPFN-3](https://docs.priorlabs.ai/)** (Prior Labs): a tabular foundation model. It needs no training run; I give it ~10 logged rows and it predicts perceived heat for all 40 surface/shade/breeze combinations. Weights run **locally** on my laptop.
- **Gemma 2 (2B) via Ollama**: runs fully local and turns the ranked table into a short walking tip.
- **Streamlit** for the tap-to-log UI; **pandas** for data.
- The engine ([engine.py](engine.py)) falls back to a RandomForest and a plain template if TabPFN or Ollama is unavailable, and the app always shows which model actually answered.

## Why Does Open Innovation Matter?

- **Works with no signal.** Parks and trails often have none. Both models run on-device, so the whole pipeline works offline once downloaded.
- **Your walking data stays with you.** Where you walk and when is personal. Nothing leaves the laptop.
- **Zero per-request cost.** No API bill for a hobby tool.
- **I can swap and steer models.** I pinned TabPFN to v3 and could change Gemma size or prompt freely; a closed API wouldn't let me do that.
- **Honest friction:** TabPFN weights need a one-time license acceptance, and I hit a version mismatch (I had accepted v3 but the library defaulted to a newer version). Pinning the version fixed it.

## My Field Test

<!-- TODO (write this from your REAL walk): where you went, what you logged, what the app recommended, whether it was right, what surprised you, what failed. Add 1-2 photos. -->

## Prize Categories

- Best Use of TabPFN
- Best Use of Gemma
