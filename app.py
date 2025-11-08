import streamlit as st
import requests
import json

# ---------------------------------------------------------
# App Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="🏦 Financial Alert Agent", layout="centered")

st.markdown("""
    <h1 style='text-align:center; margin-bottom:0;'>🏦 News-to-Action Financial Alert Agent</h1>
    <p style='text-align:center; color:gray; margin-top:0;'>
        Powered by Gemini 2.5 + spaCy — transforming financial news into actionable insights.
    </p>
    <hr style='margin-top:15px; margin-bottom:25px;'>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/analyze"

# ---------------------------------------------------------
# Input Section
# ---------------------------------------------------------
st.markdown("### 📰 Paste a Financial News Article")
article_text = st.text_area(
    "Article Text",
    placeholder="e.g., RBI fined HDFC Bank ₹10 crore for non-compliance with liquidity coverage ratio norms...",
    height=200
)

# ---------------------------------------------------------
# Analyze Button
# ---------------------------------------------------------
if st.button("🔍 Analyze Article", use_container_width=True):
    if not article_text.strip():
        st.warning("⚠️ Please enter some article text before analyzing.")
    else:
        with st.spinner("Analyzing article using Gemini 2.5..."):
            try:
                response = requests.post(
                    API_URL, json={"article_text": article_text})
                if response.status_code != 200:
                    st.error(
                        f"Backend Error: {response.status_code} - {response.text}")
                else:
                    data = response.json()

                    # --- Section Spacing Function ---
                    def section(title, emoji=""):
                        st.markdown(
                            f"<h3 style='margin-top:35px; margin-bottom:10px;'>{emoji} {title}</h3>",
                            unsafe_allow_html=True
                        )

                    # ---------------------------------------------------------
                    # 🧾 Summary
                    # ---------------------------------------------------------
                    section("Summary", "🧾")
                    st.markdown(
                        f"<div style='background-color:#f9f9f9; padding:10px 15px; border-radius:8px;'>{data.get('summary', 'N/A')}</div>",
                        unsafe_allow_html=True
                    )

                    # ---------------------------------------------------------
                    # 📈 Sentiment
                    # ---------------------------------------------------------
                    section("Sentiment", "📈")
                    sentiment = data.get("sentiment", "N/A").capitalize()
                    if sentiment == "Bullish":
                        color, emoji = "green", "🟩"
                    elif sentiment == "Bearish":
                        color, emoji = "red", "🟥"
                    else:
                        color, emoji = "gray", "⬜"
                    st.markdown(
                        f"<div style='text-align:center; color:{color}; font-weight:600; margin-top:5px;'>{emoji} {sentiment}</div>",
                        unsafe_allow_html=True
                    )

                    # ---------------------------------------------------------
                    # ⚠️ Primary Risk Type
                    # ---------------------------------------------------------
                    section("Primary Risk Type", "⚠️")
                    risk_type = data.get("risk_type", "N/A")
                    color_map = {
                        "regulatory": "orange", "credit": "red", "market": "gold",
                        "operational": "purple", "liquidity": "blue"
                    }
                    color = color_map.get(risk_type.lower(), "gray")
                    emoji = "🟠" if risk_type.lower() == "regulatory" else "⚪"
                    st.markdown(
                        f"<div style='text-align:center; color:{color}; font-weight:600; margin-top:5px;'>{emoji} {risk_type}</div>",
                        unsafe_allow_html=True
                    )

                    # ---------------------------------------------------------
                    # 🧠 Risk Rationale
                    # ---------------------------------------------------------
                    section("Risk Rationale", "🧠")
                    st.markdown(
                        f"<div style='background-color:#f9f9f9; padding:10px 15px; border-radius:8px;'>{data.get('risk_rationale', 'N/A')}</div>",
                        unsafe_allow_html=True
                    )

                    # ---------------------------------------------------------
                    # ⭐ Risk Score
                    # ---------------------------------------------------------
                    section("Risk Score (1–5)", "⭐")
                    score_raw = data.get("risk_score", 0)
                    try:
                        score = int(score_raw)
                    except:
                        try:
                            score = int(float(score_raw))
                        except:
                            score = 0
                    score = max(0, min(score, 5))
                    st.progress(min(score / 5, 1.0))

                    if score <= 2:
                        level = "🟢 Low Risk"
                        color = "green"
                    elif score == 3:
                        level = "🟡 Moderate Risk"
                        color = "orange"
                    else:
                        level = "🔴 High Risk"
                        color = "red"

                    st.markdown(
                        f"<div style='text-align:center; color:{color}; font-weight:600; margin-top:10px;'>"
                        f"{score} / 5 — {level}</div>",
                        unsafe_allow_html=True
                    )
                    st.caption("🟢 1–2 = Low | 🟡 3 = Moderate | 🔴 4–5 = High")

                    # ---------------------------------------------------------
                    # 📋 Key Points
                    # ---------------------------------------------------------
                    section("Key Points", "📋")
                    key_points = data.get("key_points", [])
                    if key_points:
                        for p in key_points:
                            st.markdown(f"• {p}")
                    else:
                        st.info("No key points provided.")

                    # ---------------------------------------------------------
                    # 🏢 Extracted Entities
                    # ---------------------------------------------------------
                    section("Extracted Entities", "🏢")
                    entities = json.dumps(data.get("entities", {}), indent=2)
                    st.code(entities, language="json")

                    st.markdown("<hr style='margin-top:40px;'>",
                                unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
