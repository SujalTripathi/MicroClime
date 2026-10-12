---
title: MicroClime: Offline Urban Heat Scout with TabPFN + Gemma (Screen Time: 10 Seconds)
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

**MicroClime** helps you find the most comfortable path for an outdoor walk, with the screen as the shortest part of the experience.

As you walk, you tap a few buttons in about 5 seconds per spot: ground surface (grass, brick, concrete, asphalt), shade (1-5), breeze (yes/no) and how hot it felt (1-5). After 5 or more spots:

1. **TabPFN-3** (Prior Labs) predicts perceived heat for all 40 surface/shade/breeze combinations.
2. **Gemma 2 (2B)**, running locally through Ollama, turns the ranking into a short walking tip.
3. The app tells you to put the phone away and go outside.

**Who it's for:** students crossing a campus, run clubs picking a route, and anyone walking in a hot city.

## Demo

<!-- TODO: drag in 1-2 screenshots (results page + a photo from your walk), or a short screen recording -->

## Code

{% embed https://github.com/YOUR_GITHUB_USERNAME/MicroClime %}

## How I Built It

- **[TabPFN-3](https://docs.priorlabs.ai/)**: a tabular foundation model that needs no training run. It predicts from about 10 logged rows. Weights run locally.
- **[Gemma 2 (2B)](https://ai.google.dev/gemma) via Ollama**: local, open-weight text generation for the walking tip.
- **Streamlit + pandas** for the tap-to-log UI.
- The engine falls back to a RandomForest and a plain template if TabPFN or Ollama is unavailable. The app always shows which model actually answered.
- I pinned TabPFN to v3 after hitting a license-version mismatch: I had accepted v3, but the library defaulted to a newer version.

## Why Does Open Innovation Matter?

- **Runs on a laptop, no cloud calls for inference.** Both models run on local weights, so predictions and advice need no server.
- **Walking data stays on the device.** Where and when you walk is personal.
- **No per-request cost.**
- **I can pin and swap models.** I pinned TabPFN's version and can change Gemma's size or prompt freely.
- **Honest limits:** weights need a one-time download and license acceptance, and the TabPFN token is needed for that step. A 2B model gives generic advice, and the tabular model is only as good as the few spots you log.

## My Field Test

<!-- TODO: write this ONLY from your real walk. Include: where you went, how many spots you logged, what the app recommended, whether it matched what you felt, and what went wrong. Add a photo. Delete this section if you did not walk. -->

## My Agent Session

<!-- Optional: link the session if you saved one -->

## Prize Categories

- Best Use of TabPFN
- Best Use of Gemma
