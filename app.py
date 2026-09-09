import streamlit as st
import os
from utils.storage import load_user_profile, save_user_profile, load_chat_history, save_chat_history, clear_chat_history
from utils.health_calc import calculate_bmi, calculate_bmr, calculate_tdee, calculate_targets, calculate_water_intake
from agents.coordinator_agent import CoordinatorAgent

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Health Coach | Multi-Agent System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Glassmorphism & Modern Aesthetic ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Custom Header Card */
    .header-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(59, 130, 246, 0.15));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }

    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #10B981, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .header-subtitle {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-top: 0.3rem;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }

    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }

    .metric-lbl {
        font-size: 0.85rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Agent Badge */
    .agent-tag {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.4);
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-top: 0.3rem;
    }

    .agent-tag-nut {
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border-color: rgba(52, 211, 153, 0.4);
    }

    .agent-tag-fit {
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border-color: rgba(251, 191, 36, 0.4);
    }

    .agent-tag-life {
        background: rgba(168, 85, 247, 0.2);
        color: #C084FC;
        border-color: rgba(192, 132, 252, 0.4);
    }

    /* Disclaimer Card */
    .disclaimer-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        font-size: 0.85rem;
        color: #FCA5A5;
        margin-top: 1.5rem;
    }

    /* Chat bubble styling tweaks */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Data & State ---
if "profile" not in st.session_state:
    st.session_state.profile = load_user_profile()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

if "coordinator" not in st.session_state:
    st.session_state.coordinator = CoordinatorAgent()

profile = st.session_state.profile

# --- Sidebar: User Profile & Configuration ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/health-calendar.png", width=64)
    st.title("User Profile & Onboarding")
    st.caption("Personalize your multi-agent health coach memory.")

    with st.form("user_profile_form"):
        name = st.text_input("Name", value=profile.get("name", "Alex"))
        
        col_a, col_b = st.columns(2)
        with col_a:
            age = st.number_input("Age", min_value=12, max_value=100, value=int(profile.get("age", 22)))
            height = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=float(profile.get("height_cm", 175.0)), step=1.0)
        with col_b:
            gender = st.selectbox("Gender", options=["Male", "Female"], index=0 if profile.get("gender") == "Male" else 1)
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=float(profile.get("weight_kg", 70.0)), step=0.5)

        goal = st.selectbox(
            "Primary Goal",
            options=["Lose Weight / Fat Loss", "Gain Muscle / Hypertrophy", "Stay Fit / Maintenance"],
            index=1 if "muscle" in profile.get("goal", "").lower() else (0 if "lose" in profile.get("goal", "").lower() else 2)
        )

        diet_pref = st.selectbox(
            "Diet Preference",
            options=["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Eggetarian"],
            index=0
        )

        activity_level = st.selectbox(
            "Activity Level",
            options=[
                "Sedentary (Little/no exercise)",
                "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)",
                "Very Active (6-7 days/week)"
            ],
            index=2
        )

        st.markdown("---")
        st.subheader("🔑 LLM Configuration")
        api_key = st.text_input("Gemini or Groq API Key (Optional)", value=profile.get("api_key", ""), type="password", help="Leave blank to use smart offline rules engine.")

        submitted = st.form_submit_button("💾 Save Profile & Update Memory", use_container_width=True)

        if submitted:
            updated = {
                "name": name,
                "age": int(age),
                "gender": gender,
                "height_cm": float(height),
                "weight_kg": float(weight),
                "goal": goal,
                "diet_pref": diet_pref,
                "activity_level": activity_level,
                "api_key": api_key.strip()
            }
            st.session_state.profile = updated
            save_user_profile(updated)
            st.success("Profile saved successfully!")

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        clear_chat_history()
        st.session_state.chat_history = []
        st.rerun()

    # System Status Indicator
    active_key = profile.get("api_key") or os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY")
    if active_key:
        st.caption("🟢 **AI Provider**: LLM API Connected")
    else:
        st.caption("⚡ **AI Provider**: Smart Offline Rules Engine Active")

# --- Main App Body ---

# Header Section
st.markdown("""
<div class="header-card">
    <div class="header-title">🤖 Multi-Agent AI Health Coach</div>
    <div class="header-subtitle">Collaborative AI Agents working together to deliver personalized Nutrition, Fitness & Lifestyle advice.</div>
    <div style="margin-top: 1rem;">
        <span class="agent-tag">🤖 Coordinator Agent</span>
        <span class="agent-tag agent-tag-nut">🥗 Nutrition Agent</span>
        <span class="agent-tag agent-tag-fit">🏋️ Fitness Agent</span>
        <span class="agent-tag agent-tag-life">🌿 Lifestyle Agent</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Calculate Health Metrics
bmi_res = calculate_bmi(profile.get("weight_kg", 70.0), profile.get("height_cm", 175.0))
bmr = calculate_bmr(profile.get("weight_kg", 70.0), profile.get("height_cm", 175.0), profile.get("age", 22), profile.get("gender", "Male"))
tdee = calculate_tdee(bmr, profile.get("activity_level", "Moderately Active"))
targets = calculate_targets(tdee, profile.get("goal", "Gain muscle"))
water_liters = calculate_water_intake(profile.get("weight_kg", 70.0), profile.get("activity_level", "Moderately Active"))

# Render Health Dashboard Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Body Mass Index (BMI)</div>
        <div class="metric-val" style="color: {bmi_res['color']};">{bmi_res['bmi']}</div>
        <div style="font-size: 0.8rem; font-weight: 600; color: {bmi_res['color']}; margin-top: 0.2rem;">{bmi_res['category']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Estimated BMR / TDEE</div>
        <div class="metric-val" style="color: #60A5FA;">{int(tdee)} <span style="font-size: 0.9rem;">kcal/day</span></div>
        <div style="font-size: 0.8rem; color: #9CA3AF; margin-top: 0.2rem;">BMR Baseline: {int(bmr)} kcal</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Target Caloric Intake</div>
        <div class="metric-val" style="color: #34D399;">{targets['target_calories']} <span style="font-size: 0.9rem;">kcal</span></div>
        <div style="font-size: 0.8rem; color: #34D399; margin-top: 0.2rem;">{targets['goal_type']}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Hydration Target</div>
        <div class="metric-val" style="color: #38BDF8;">{water_liters} <span style="font-size: 0.9rem;">Liters</span></div>
        <div style="font-size: 0.8rem; color: #9CA3AF; margin-top: 0.2rem;">~{int(water_liters * 4)} glasses / day</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Quick Prompt Suggestions ---
st.subheader("💡 Ask Your AI Coaching Team")
suggestion_cols = st.columns(4)

selected_prompt = None
with suggestion_cols[0]:
    if st.button("🍱 1-Day Meal Plan", use_container_width=True):
        selected_prompt = "Give me a detailed 1-day personalized meal plan matching my diet preference and calories."
with suggestion_cols[1]:
    if st.button("🏋️ 30-Min Workout", use_container_width=True):
        selected_prompt = "Suggest a 30-minute home/gym workout routine tailored for my goal."
with suggestion_cols[2]:
    if st.button("😴 Sleep & Recovery", use_container_width=True):
        selected_prompt = "How can I improve my sleep quality, energy levels, and daily habits?"
with suggestion_cols[3]:
    if st.button("📊 Full Daily Plan", use_container_width=True):
        selected_prompt = "Give me a complete daily health plan covering my meals, workout, and hydration."

# --- Render Chat Memory ---
for message in st.session_state.chat_history:
    role = message.get("role")
    content = message.get("content")
    agents_used = message.get("agents", [])
    
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        if agents_used:
            tags_html = " ".join([f"<span class='agent-tag'>{ag}</span>" for ag in agents_used])
            st.markdown(f"<div>{tags_html}</div><br>", unsafe_allow_html=True)
        st.markdown(content)

# Chat Input Box
user_input = st.chat_input("Ask your agents anything about nutrition, workouts, sleep, or habits...")

# Combine button click or direct typed query
query_to_process = selected_prompt or user_input

if query_to_process:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": query_to_process})
    with st.chat_message("user", avatar="👤"):
        st.markdown(query_to_process)

    # Process query through Coordinator & Sub-Agents
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 Coordinator Agent is analyzing intent & consulting specialist agents..."):
            effective_key = profile.get("api_key") or os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY") or ""
            response_text, contributing_agents = st.session_state.coordinator.process_query(
                prompt=query_to_process,
                user_profile=profile,
                api_key=effective_key
            )
            
            # Display contributing agents
            if contributing_agents:
                tags_html = " ".join([f"<span class='agent-tag'>{ag}</span>" for ag in contributing_agents])
                st.markdown(f"<div>{tags_html}</div><br>", unsafe_allow_html=True)

            st.markdown(response_text)

    # Save to history memory
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response_text,
        "agents": contributing_agents
    })
    save_chat_history(st.session_state.chat_history)
    
    if selected_prompt:
        st.rerun()

# --- Safety Disclaimer Footer ---
st.markdown("""
<div class="disclaimer-box">
    ⚠️ <strong>Medical Disclaimer</strong>: This AI Agent system is built for college demonstration & educational fitness guidance. 
    It does not provide medical diagnoses or treatment. Always consult a qualified medical professional for health concerns.
</div>
""", unsafe_allow_html=True)
