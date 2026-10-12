# 🌿 MicroClime: Offline Urban Heat Scout

> **Touch Grass, Not Screens.**  
> Built for the **Hacktoberfest Open-Source AI Challenge (Week 1 / 2026)**.  
> Targeting: **Best Use of TabPFN** & **Best Use of Gemma**.

---

## 📖 Overview

**MicroClime** is an open-source, offline-first outdoor companion that helps people escape indoor screens and safely navigate outdoor urban heat islands.

During outdoor strolls, runs, or campus walks, users log a few sensory data points with a single tap (surface ground type, canopy shade, breeze, and perceived heat). 

In under 5 seconds:
1. **Prior Labs TabPFN-3** (tabular foundation model) evaluates all 40 microclimate permutations to forecast the coolest walking corridors and identify dangerous heat traps.
2. **Google Gemma 2 (2B)** (open-weight model running locally via Ollama) translates these tabular predictions into actionable, plain-English walking navigation advice.
3. The interface immediately tells the user to **lock their screen and enjoy the outdoors**.

---

## ⚡ The "Touch Grass" Philosophy

The challenge prompt states: *"The best builds here should make the screen the shortest part of the experience."*

- **Screen time:** ~10 seconds to log spots and view guidance.
- **Outdoor time:** 30–60 minutes walking through shaded, comfortable green spaces.
- **Zero Cloud Leakage:** All inference runs 100% on-device (local weights). It works seamlessly in parks and hiking trails with zero cellular reception.

---

## 🏗️ Architecture

```
[Outdoor Walker on Smartphone / Laptop]
        │
        │ Taps sensory cues (Grass, Canopy, Breeze)
        ▼
[MicroClime Core Engine (engine.py)]
  ├── Prior Labs TabPFN-3 (Tabular Foundation Model)
  │     └── Ingests small real-world walk data (<15 rows)
  │     └── Zero-shot regression across all 40 surface/shade/wind permutations
  │
  └── Google Gemma 2 (2B via Ollama / Open Weights)
        └── Transforms ranked tabular outputs into empathetic, natural navigation tips
        │
        ▼
[Cooling Corridors Revealed → Lock Screen → Touch Grass!]
```

---

## 🚀 Quickstart

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/YOUR_USERNAME/MicroClime.git
cd MicroClime
pip install -r requirements.txt
```

### 2. Configure Prior Labs TabPFN
Get your free API token from [Prior Labs UX](https://ux.priorlabs.ai/account) and accept the TabPFN-3 license.
Create a `.env` file in the root directory:
```env
TABPFN_TOKEN="your_tabpfn_token_here"
```

### 3. Run Google Gemma (Ollama)
```bash
ollama pull gemma2:2b
```

### 4. Launch the Web Interface
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser. (Or access `http://<your-local-ip>:8501` from your mobile phone on the same Wi-Fi network).

---

## 🌟 Why Open Innovation Matters

- **Offline Independence:** Works deep in national parks and rural greenways without 4G/5G signal.
- **Complete Privacy:** Personal movement and location logs never leave your device.
- **Zero Marginal API Costs:** Free from proprietary token pricing or external vendor lock-in.

---

## 📄 License
MIT License. Built with ❤️ for Hacktoberfest 2026.
