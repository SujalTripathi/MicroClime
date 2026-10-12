import pandas as pd
import streamlit as st

from engine import SURFACES, gemma_advice, predict_zones

st.set_page_config(
    page_title="MicroClime • Offline Urban Heat Scout",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom modern CSS styling: tactile mobile feel, glassmorphism, nature gradients
st.markdown(
    """
    <style>
    /* Global styling */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1f18 0%, #080d0b 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header card */
    .hero-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(6, 78, 59, 0.25));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #34d399, #10b981, #a7f3d0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    /* Tactile Spot Logger Card */
    .action-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(51, 65, 85, 0.7);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Result Cards */
    .zone-card-cool {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.05));
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .zone-card-hot {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(185, 28, 28, 0.05));
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .advice-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(21, 128, 61, 0.1));
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 18px;
        color: #f1f5f9;
        font-size: 1.05rem;
        line-height: 1.5;
        margin-top: 16px;
    }
    
    /* Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Hero
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🌿 MicroClime</div>
        <div class="hero-sub">
            The screen-free urban heat scout. Tap what you feel on the trail, uncover cooling corridors with <b>TabPFN</b>, and let <b>Gemma</b> guide your walk.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

COLS = ["surface_type", "shade_level", "breeze_felt", "perceived_heat"]
if "log" not in st.session_state:
    st.session_state.log = pd.DataFrame(columns=COLS)

# Surface mapping
SURFACE_OPTIONS = {
    "🌱 Grass / Lawn": "grass",
    "🧱 Brick Walkway": "brick",
    "🪨 Concrete Pavement": "concrete",
    "🛣️ Asphalt Road": "asphalt",
}

SHADE_OPTIONS = {
    "☀️ Harsh Sun": 1,
    "🌤️ Light Shade": 2,
    "⛅ Dappled Shade": 3,
    "🌳 Tree Canopy": 4,
    "🌲 Deep Dense Shade": 5,
}

BREEZE_OPTIONS = {
    "🍃 Yes, Cool Breeze": 1,
    "🛑 No Wind / Stagnant": 0,
}

HEAT_OPTIONS = {
    "❄️ 1 - Very Cool": 1,
    "😊 2 - Pleasant": 2,
    "🌤️ 3 - Warm": 3,
    "🥵 4 - Sweltering": 4,
    "🔥 5 - Scorching": 5,
}

# --- SECTION 1: TACTILE LOGGER ---
st.markdown("### 📍 Step 1: Log Current Spot")

col_a, col_b = st.columns(2)
with col_a:
    sel_surface = st.radio("What are you standing on?", list(SURFACE_OPTIONS.keys()), index=0)
    sel_breeze = st.radio("Feel any breeze?", list(BREEZE_OPTIONS.keys()), index=0)

with col_b:
    sel_shade = st.select_slider("Sunlight & Shade:", options=list(SHADE_OPTIONS.keys()), value="⛅ Dappled Shade")
    sel_heat = st.select_slider("How hot does it feel right now?", options=list(HEAT_OPTIONS.keys()), value="🌤️ 3 - Warm")

btn_col1, btn_col2, btn_col3 = st.columns([1.5, 1.2, 0.8])

with btn_col1:
    if st.button("➕ Tap to Log Spot", type="primary", use_container_width=True):
        new_row = pd.DataFrame(
            [[
                SURFACE_OPTIONS[sel_surface],
                SHADE_OPTIONS[sel_shade],
                BREEZE_OPTIONS[sel_breeze],
                HEAT_OPTIONS[sel_heat],
            ]],
            columns=COLS,
        )
        st.session_state.log = pd.concat([st.session_state.log, new_row], ignore_index=True)
        st.toast("✅ Spot logged in 2 seconds!", icon="📍")

with btn_col2:
    if st.button("⚡ Quick Demo Walk", use_container_width=True):
        st.session_state.log = pd.read_csv("sample_walk.csv")[COLS]
        st.toast("Loaded 10 outdoor field points!", icon="🚀")

with btn_col3:
    if st.button("🗑️ Reset", use_container_width=True):
        st.session_state.log = pd.DataFrame(columns=COLS)

# Progress indicator
logged_count = len(st.session_state.log)
min_required = 5
pct = min(1.0, logged_count / min_required)

st.progress(pct, text=f"Progress: {logged_count} / {min_required} spots collected {'(Ready to analyze!)' if logged_count >= min_required else '(Collect at least 5)'}")

# Live spots list
if logged_count > 0:
    with st.expander(f"📋 Review Logged Walk Data ({logged_count} spots)", expanded=False):
        st.dataframe(st.session_state.log, use_container_width=True, hide_index=True)

# --- SECTION 2: AI PREDICTION ---
st.markdown("---")
st.markdown("### 🔮 Step 2: Scout Microclimates")

place_name = st.text_input("Current Location / Park Name:", value="Central Campus & Greenway", placeholder="e.g. City Central Park")

can_predict = logged_count >= min_required
if st.button("🧭 Uncover Cool Corridors & Put Screen Away", type="primary", disabled=not can_predict, use_container_width=True):
    try:
        with st.spinner("🤖 Prior Labs TabPFN-3 is forecasting all 40 microclimate permutations..."):
            zones, model_name = predict_zones(st.session_state.log)

        st.success(f"⚡ Foundation Model: {model_name}")

        # Top 3 Coolest vs Top 3 Hottest
        col_c, col_h = st.columns(2)
        
        with col_c:
            st.markdown("#### ❄️ Top 3 Cooling Corridors")
            for idx, r in zones.head(3).iterrows():
                breeze_str = "🍃 Breezy" if r.breeze_felt == 1 else "🛑 Still"
                st.markdown(
                    f"""
                    <div class="zone-card-cool">
                        <div>
                            <b>{r.surface_type.capitalize()}</b> • Shade {int(r.shade_level)}/5<br>
                            <small style="color:#6ee7b7">{breeze_str}</small>
                        </div>
                        <div style="font-size:1.3rem; font-weight:800; color:#34d399">
                            {r.predicted_heat:.1f} <span style="font-size:0.8rem">/ 5</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col_h:
            st.markdown("#### 🔥 Top 3 Heat Traps to Avoid")
            for idx, r in zones.tail(3).iloc[::-1].iterrows():
                breeze_str = "🍃 Breezy" if r.breeze_felt == 1 else "🛑 Still"
                st.markdown(
                    f"""
                    <div class="zone-card-hot">
                        <div>
                            <b>{r.surface_type.capitalize()}</b> • Shade {int(r.shade_level)}/5<br>
                            <small style="color:#fca5a5">{breeze_str}</small>
                        </div>
                        <div style="font-size:1.3rem; font-weight:800; color:#f87171">
                            {r.predicted_heat:.1f} <span style="font-size:0.8rem">/ 5</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with st.spinner("🧠 Gemma is synthesizing your personalized outdoor guide..."):
            advice_text, source_engine = gemma_advice(zones, place_name)

        st.markdown(
            f"""
            <div class="advice-box">
                <div style="font-weight:700; color:#4ade80; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
                    <span>🧭</span> Gemma Walk Navigation Advice
                </div>
                <div style="font-size:1.05rem;">{advice_text}</div>
                <div style="font-size:0.8rem; color:#94a3b8; margin-top:8px;">Source: {source_engine}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.balloons()
        st.info("🎒 **Goal Accomplished:** You now know the coolest path. Lock your phone, step away from the keyboard, and go touch grass!")

    except Exception as err:
        st.error(f"Error during prediction: {err}")

# Optional collapsed tools for judges/devs
with st.expander("🛠️ Advanced: CSV Import / Export for Judges"):
    up = st.file_uploader("Upload pre-recorded CSV", type="csv")
    if up:
        st.session_state.log = pd.read_csv(up)
        st.rerun()
    if len(st.session_state.log) > 0:
        csv_data = st.session_state.log.to_csv(index=False)
        st.download_button("📥 Export Walk Log as CSV", data=csv_data, file_name="my_walk_log.csv", mime="text/csv")
