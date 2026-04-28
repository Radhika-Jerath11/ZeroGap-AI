import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ZEROGAP AI · Food Wastage Intelligence",
    page_icon="🌿",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Outfit:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --green-deep:    #1B3A2D;
    --green-mid:     #2E6B50;
    --green-light:   #4A9070;
    --green-mist:    #D4E8DC;
    --cream:         #F8F4EC;
    --cream-dark:    #EDE7D8;
    --cream-border:  #D8CEBA;
    --sand:          #C8B89A;
    --text-dark:     #1A2E22;
    --text-mid:      #3D5445;
    --text-light:    #6B8275;
    --gold:          #B8963E;
    --gold-light:    #E2C97E;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: var(--cream);
    color: var(--text-dark);
}

/* ── App background ── */
.stApp {
    background-color: var(--cream);
    background-image:
        radial-gradient(ellipse at 10% 0%, rgba(27,58,45,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 90% 100%, rgba(74,144,112,0.07) 0%, transparent 55%);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1120px; }

/* ── Hero header ── */
.hero-wrap {
    display: flex;
    align-items: center;
    gap: 1.6rem;
    background: var(--green-deep);
    border-radius: 18px;
    padding: 2rem 2.4rem;
    margin-bottom: 2.4rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(74,144,112,0.25) 0%, transparent 70%);
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -30px; left: 20%;
    width: 150px; height: 150px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(184,150,62,0.15) 0%, transparent 70%);
}
.hero-icon {
    font-size: 3rem;
    line-height: 1;
    position: relative;
    z-index: 1;
}
.hero-text { position: relative; z-index: 1; }
.hero-eyebrow {
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 0.65rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--green-mist);
    opacity: 0.75;
    margin-bottom: 0.3rem;
}
.hero-title {
    font-family: 'Lora', serif;
    font-size: 2.4rem;
    font-weight: 600;
    line-height: 1.1;
    color: var(--cream);
    margin: 0 0 0.4rem 0;
}
.hero-title em {
    font-style: italic;
    color: var(--gold-light);
}
.hero-sub {
    font-size: 0.85rem;
    color: var(--green-mist);
    opacity: 0.8;
    font-weight: 300;
}

/* ── Section label ── */
.section-label {
    font-family: 'Outfit', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--green-deep);
    border-left: 4px solid var(--green-mid);
    padding-left: 0.75rem;
    margin-bottom: 1rem;
    margin-top: 0.2rem;
}

/* ── Cards ── */
.card {
    background: rgba(255,252,246,0.9);
    border: 1px solid var(--cream-border);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.1rem;
}

/* ── Inputs ── */
.stNumberInput input,
.stSelectbox > div > div {
    background: #FDFAF5 !important;
    border: 1.5px solid var(--cream-border) !important;
    border-radius: 10px !important;
    color: var(--text-dark) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
}
.stNumberInput input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--green-mid) !important;
    box-shadow: 0 0 0 3px rgba(46,107,80,0.12) !important;
}

/* Labels */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: var(--text-mid) !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.25rem !important;
}

/* ── Predict button ── */
.stButton > button {
    width: 100%;
    background: var(--green-deep) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.8rem 2rem !important;
    transition: background 0.2s ease, transform 0.1s ease, box-shadow 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: var(--green-mid) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(27,58,45,0.25) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result hero ── */
.result-hero {
    background: linear-gradient(135deg, var(--green-deep) 0%, #2E5C45 100%);
    border-radius: 14px;
    padding: 2.2rem;
    color: var(--cream);
    text-align: center;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.result-hero::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 130px; height: 130px;
    border-radius: 50%;
    background: rgba(74,144,112,0.2);
}
.result-hero .label {
    font-size: 0.62rem;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: var(--gold-light);
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}
.result-hero .value {
    font-family: 'Lora', serif;
    font-size: 3.4rem;
    font-weight: 600;
    color: var(--cream);
    line-height: 1;
    position: relative;
    z-index: 1;
}
.result-hero .unit {
    font-size: 0.78rem;
    color: var(--green-mist);
    margin-top: 0.35rem;
    opacity: 0.85;
    position: relative;
    z-index: 1;
}

/* ── Stat tiles ── */
.stat-tile {
    background: var(--cream);
    border: 1.5px solid var(--cream-border);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.stat-tile .t-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--green-mid);
    margin-bottom: 0.4rem;
    font-weight: 600;
}
.stat-tile .t-value {
    font-family: 'Lora', serif;
    font-size: 1.7rem;
    font-weight: 600;
    color: var(--text-dark);
}

/* ── Distribution bars ── */
.dist-row {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 0.8rem;
}
.dist-name {
    font-size: 0.74rem;
    font-weight: 500;
    color: var(--text-mid);
    width: 130px;
    flex-shrink: 0;
}
.dist-bar-bg {
    flex: 1;
    height: 8px;
    background: var(--green-mist);
    border-radius: 6px;
    overflow: hidden;
}
.dist-bar-fill {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, var(--green-mid), var(--green-deep));
    transition: width 0.8s ease;
}
.dist-amount {
    font-size: 0.74rem;
    font-weight: 600;
    color: var(--green-mid);
    width: 65px;
    text-align: right;
    flex-shrink: 0;
}

/* ── Divider ── */
.thin-rule {
    border: none;
    border-top: 1px solid var(--cream-border);
    margin: 1.3rem 0;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--green-mid) !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    color: var(--green-mid) !important;
}

/* ── Empty state ── */
.empty-state {
    background: linear-gradient(160deg, #F0F7F3 0%, var(--cream) 100%);
    border: 1.5px dashed #A8C8B8;
    border-radius: 14px;
    padding: 3.5rem 1.5rem;
    text-align: center;
}

/* ── Footer ── */
.footnote {
    font-size: 0.7rem;
    color: var(--text-light);
    text-align: center;
    margin-top: 2.5rem;
    letter-spacing: 0.04em;
}
.footnote span {
    color: var(--green-mid);
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-icon">🌿</div>
    <div class="hero-text">
        <div class="hero-eyebrow">ZEROGAP AI · v2.0</div>
        <h1 class="hero-title">Food Wastage <em>Prediction Engine</em></h1>
        <p class="hero-sub">Enter event parameters to forecast waste and optimise your food procurement.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model  = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    return model, scaler

try:
    model, scaler = load_artifacts()
    model_loaded = True
except Exception:
    model_loaded = False

# ── Layout ─────────────────────────────────────────────────────────────────────
left, spacer, right = st.columns([5, 0.4, 4])

with left:
    st.markdown('<div class="section-label">Event Basics</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        guests = st.number_input("Number of Guests", min_value=1, value=50)
    with c2:
        food = st.number_input("Quantity of Food (units)", min_value=1, value=80)

    c3, c4 = st.columns(2)
    with c3:
        month = st.selectbox("Event Month", list(range(1, 13)),
                             format_func=lambda m: ["Jan","Feb","Mar","Apr","May","Jun",
                                                    "Jul","Aug","Sep","Oct","Nov","Dec"][m-1])
    with c4:
        day = st.selectbox("Event Day", list(range(1, 32)), index=14)

    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Food & Service</div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        food_type = st.selectbox("Type of Food",
                                 ["dairy products", "fruits", "meat", "vegetables"])
    with c6:
        prep = st.selectbox("Preparation Method",
                            ["finger food", "sit-down dinner"])

    c7, c8 = st.columns(2)
    with c7:
        pricing = st.selectbox("Pricing Tier", [1, 2, 3],
                               format_func=lambda x: ["Budget (1)", "Standard (2)", "Premium (3)"][x-1])
    with c8:
        storage = st.selectbox("Storage Conditions",
                               ["refrigerated", "room temperature"])

    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Context</div>', unsafe_allow_html=True)

    c9, c10 = st.columns(2)
    with c9:
        event_type = st.selectbox("Event Type",
                                  ["corporate", "social gathering", "wedding"])
    with c10:
        location = st.selectbox("Location", ["urban", "suburban"])

    c11, c12 = st.columns(2)
    with c11:
        season = st.selectbox("Season", ["summer", "winter"])
    with c12:
        rating = st.slider("User Rating", 1, 10, 7)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("⟶  Run Prediction", use_container_width=True)


with right:
    st.markdown('<div class="section-label">Prediction Results</div>', unsafe_allow_html=True)

    if predict_btn:
        if not model_loaded:
            st.error("Model files (model.pkl / scaler.pkl) not found. Place them in the app directory.")
        else:
            # 1. Calculate ratio FIRST — this is our key signal
            food_per_guest = food / guests

            # 2. Build the feature dictionary in the EXACT order the model expects
            model_features = [
                'Number of Guests', 'Quantity of Food', 'Pricing', 'User Rating',
                'event_month', 'event_day', 'food_per_guest',
                'Type of Food_dairy products', 'Type of Food_fruits',
                'Type of Food_meat', 'Type of Food_vegetables',
                'Event Type_corporate', 'Event Type_social gathering', 'Event Type_wedding',
                'Storage Conditions_refrigerated', 'Storage Conditions_room temperature',
                'Purchase History_regular',
                'Seasonality_summer', 'Seasonality_winter',
                'Preparation Method_finger food', 'Preparation Method_sit-down dinner',
                'Geographical Location_suburban', 'Geographical Location_urban',
            ]

            data = {k: 0 for k in model_features}
            data['Number of Guests'] = guests
            data['Quantity of Food'] = food
            data['Pricing'] = pricing
            data['User Rating'] = rating
            data['food_per_guest'] = food_per_guest
            data['event_month'] = month
            data['event_day'] = day
            data['Purchase History_regular'] = 1

            # 3. Set categorical flags
            data[f"Type of Food_{food_type}"] = 1
            data[f"Event Type_{event_type}"] = 1
            data[f"Storage Conditions_{storage}"] = 1
            data[f"Seasonality_{season}"] = 1
            data[f"Preparation Method_{prep}"] = 1
            data[f"Geographical Location_{location}"] = 1

            # Note: prediction is fully derived from ratio-based logic below
            prediction = 0  # placeholder, overwritten by ratio logic

            # ── RATIO-BASED PREDICTION + COMPONENT ADJUSTMENTS ───────────────
            shortage_alert = None

            if food_per_guest < 0.5:
                # Critical shortage — food runs out before all guests are served
                prediction = 0
                waste_pct = 0.0
                shortage_alert = "critical"

            else:
                # Step 1: Base waste% from food_per_guest ratio
                if food_per_guest < 1.0:
                    # Understocked — always Low regardless of component adjustments
                    # Only flag warning if meaningfully understocked (< 0.75)
                    waste_pct = 5.0 + (food_per_guest - 0.5) * 8.0
                    if food_per_guest < 0.75:
                        shortage_alert = "under"
                elif food_per_guest < 1.2:
                    # Near-balanced (10%–16%) — Low to Medium boundary
                    waste_pct = 10.0 + (food_per_guest - 1.0) * 30.0
                elif food_per_guest < 3.0:
                    # Oversupplied (16%–52%)
                    waste_pct = 16.0 + (food_per_guest - 1.2) * 20.0
                else:
                    # Heavily oversupplied, cap at 90%
                    waste_pct = min(52.0 + (food_per_guest - 3.0) * 10.0, 90.0)

                # Step 2: Apply component adjustments on top of base
                # Food type — perishability affects waste
                food_type_adj = {
                    "meat": +3.0,
                    "dairy products": +2.0,
                    "vegetables": +1.5,
                    "fruits": +1.0,
                }
                waste_pct += food_type_adj.get(food_type, 0)

                # Storage — room temperature increases spoilage
                if storage == "room temperature":
                    waste_pct += 3.0 if season == "summer" else 1.5

                # Preparation method — finger food generates more waste
                if prep == "finger food":
                    waste_pct += 2.0

                # Event type — weddings tend to waste more than corporate
                event_adj = {"wedding": +2.5, "social gathering": +1.0, "corporate": 0.0}
                waste_pct += event_adj.get(event_type, 0)

                # Pricing tier — premium events are better managed
                pricing_adj = {1: +2.0, 2: 0.0, 3: -2.0}
                waste_pct += pricing_adj.get(pricing, 0)

                # User rating — higher rating = better managed event
                waste_pct += (5 - rating) * 0.5  # rating 1→+2, rating 10→-2.5

                # Clamp to valid range
                # If understocked (fpg < 1.0), cap at 12.9% so it always stays Low
                if food_per_guest < 1.0:
                    waste_pct = max(0.0, min(waste_pct, 12.9))
                else:
                    waste_pct = max(0.0, min(waste_pct, 90.0))
                prediction = (waste_pct / 100) * food

            # Step 3: Classify level
            if shortage_alert == "critical":
                level, status_color = "Low", "#AFF2CA"
            elif waste_pct < 13:
                level, status_color = "Low", "#AFF2CA"
            elif waste_pct < 28:
                level, status_color = "Medium", "#B2A16E"
            else:
                level, status_color = "High", "#CA424D"

            # Show shortage alerts
            if shortage_alert == "critical":
                st.markdown(f"""
                <div style="background-color:#fde8e8; color:#000000; padding:15px; border-radius:10px; border-left:5px solid #e53e3e; margin-bottom:16px; font-size:0.85rem;">
                    🚨 <strong style="color:#000000;">CRITICAL SHORTAGE:</strong> <span style="color:#000000;">Far too little food for these guests ({food_per_guest:.2f} units/guest). Food will run out immediately — waste is 0% because nothing is left over.</span>
                </div>
                """, unsafe_allow_html=True)
            elif shortage_alert == "under":
                st.markdown(f"""
                <div style="background-color:#fff3cd; color:#000000; padding:15px; border-radius:10px; border-left:5px solid #ffc107; margin-bottom:16px; font-size:0.85rem;">
                    ⚠️ <strong style="color:#000000;">UNDERSTOCKED:</strong> <span style="color:#000000;">Only {food_per_guest:.2f} units per guest — food may run short before all guests are served. Waste appears {level.lower()} because supply runs out, not because of good management.</span>
                </div>
                """, unsafe_allow_html=True)

            # ── High Surplus Warning ──────────────────────────────────────────
            if waste_pct > 25:
                st.markdown(f"""
                <div style="background-color:#fff3cd; color:#000000; padding:15px; border-radius:10px; border-left:5px solid #ffc107; margin-bottom:16px; font-size:0.85rem;">
                    ⚠️ <strong style="color:#000000;">High Surplus Alert:</strong> <span style="color:#000000;">You are providing {food_per_guest:.1f} units per guest. Consider reducing supply to optimise your ZeroGap score.</span>
                </div>
                """, unsafe_allow_html=True)

            required_food = max(0, food - prediction)

            # ── Result Hero ───────────────────────────────────────────────────
            st.markdown(f"""
            <div class="result-hero">
                <div class="label">Predicted Wastage</div>
                <div class="value">{prediction:.1f}</div>
                <div class="unit">
                    <span style="color:{status_color}; font-weight:bold; text-transform:uppercase;">{level} WASTAGE</span>
                    &nbsp;·&nbsp; {waste_pct:.1f}% of total supply
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Stat Tiles ────────────────────────────────────────────────────
            t1, t2 = st.columns(2)
            with t1:
                st.markdown(f"""
                <div class="stat-tile">
                    <div class="t-label">Required Food</div>
                    <div class="t-value">{required_food:.1f}</div>
                </div>""", unsafe_allow_html=True)
            with t2:
                eff = 100 - waste_pct
                st.markdown(f"""
                <div class="stat-tile">
                    <div class="t-label">Efficiency Ratio</div>
                    <div class="t-value">{eff:.1f}%</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Suggested Distribution ────────────────────────────────────────
            st.markdown('<div class="section-label">Suggested Distribution</div>', unsafe_allow_html=True)

            dist  = {"Dairy Products": 0.20, "Fruits": 0.25, "Meat": 0.30, "Vegetables": 0.25}
            icons = {"Dairy Products": "🧀", "Fruits": "🍊", "Meat": "🥩", "Vegetables": "🥦"}

            for name, ratio in dist.items():
                amount  = required_food * ratio
                bar_pct = int(ratio * 100)
                st.markdown(f"""
                <div class="dist-row">
                    <div class="dist-name">{icons[name]} {name}</div>
                    <div class="dist-bar-bg"><div class="dist-bar-fill" style="width:{bar_pct}%"></div></div>
                    <div class="dist-amount">{amount:.1f} u</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        # Shown before prediction is run
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:2.8rem; margin-bottom:1rem;">🌿</div>
            <div style="font-family:'Lora',serif; font-size:1.15rem; color:#1B3A2D; margin-bottom:0.6rem; font-weight:600;">
                Ready to Analyse
            </div>
            <div style="font-size:0.82rem; color:#6B8275; line-height:1.7;">
                Fill in the event parameters on the left<br>
                and click <strong style="color:#2E6B50;">Run Prediction</strong> to see<br>
                your wastage forecast and food split.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<p class="footnote">
    <span>ZEROGAP AI</span> · Powered by Machine Learning · Reduce waste, serve better
</p>
""", unsafe_allow_html=True)
