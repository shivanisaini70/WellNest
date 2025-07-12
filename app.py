import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="WellNest", layout="centered", page_icon="🌱")

# --- Load custom CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🌿 WellNest")
page = st.sidebar.selectbox("Go to", ["🏠 Welcome", "📝 Daily Entry", "📊 Dashboard"])

# --- File Path ---
file_path = "data/wellness_log.csv"

# --- Page 1: Welcome ---
if page == "🏠 Welcome":
    st.title("🌿 Welcome to WellNest")
    st.markdown("""
    **WellNest** is your personalized wellness tracker that helps you:
    
    - 📝 Log daily habits (sleep, water, mood, steps)
    - 📊 Visualize your progress
    - 💡 Get smart wellness tips

    Start today and grow a healthier lifestyle, one habit at a time! 🌱  
    Use the sidebar to navigate ➡️
    """)

# --- Page 2: Daily Entry ---
elif page == "📝 Daily Entry":
    st.title("📝 Daily Wellness Entry")

    with st.form("wellness_form"):
        name = st.text_input("👤 Your Name")
        sleep = st.slider("😴 Hours of Sleep", 0, 12, 7)
        water = st.slider("💧 Glasses of Water", 0, 20, 8)
        meals = st.selectbox("🍽️ Meals Today", ["1", "2", "3", "4+"])
        steps = st.number_input("🚶 Steps Walked", min_value=0, step=100)
        mood = st.selectbox("😊 Mood", ["Happy", "Tired", "Anxious", "Sad", "Energetic", "Calm"])
        submit = st.form_submit_button("Submit Entry")

    if submit:
        if name.strip() == "":
            st.error("Please enter your name.")
        else:
            today = datetime.date.today().strftime("%Y-%m-%d")
            new_data = pd.DataFrame({
                "Date": [today],
                "Name": [name],
                "Sleep Hours": [sleep],
                "Water Intake": [water],
                "Meals": [meals],
                "Steps": [steps],
                "Mood": [mood]
            })

            if os.path.exists(file_path):
                new_data.to_csv(file_path, mode='a', header=False, index=False)
            else:
                new_data.to_csv(file_path, mode='w', header=True, index=False)

            st.success("✅ Entry saved successfully!")
            st.balloons()

# --- Page 3: Dashboard ---
elif page == "📊 Dashboard":
    st.title("📊 Your Wellness Dashboard")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        if df.empty:
            st.info("No entries yet. Submit some data first.")
        else:
            last_7 = df.tail(7)

            # --- Mood Chart ---
            mood_count = last_7["Mood"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(mood_count, labels=mood_count.index, autopct="%1.1f%%", startangle=90)
            ax1.axis("equal")
            st.markdown("#### 😊 Mood Distribution")
            st.pyplot(fig1)

            # --- Sleep & Water Chart ---
            st.markdown("#### 😴 Sleep & 💧 Water Intake Trends")
            fig2, ax2 = plt.subplots()
            last_7.plot(kind="bar", x="Date", y=["Sleep Hours", "Water Intake"], ax=ax2)
            plt.xticks(rotation=45)
            st.pyplot(fig2)

            # --- Steps Line Chart ---
            st.markdown("#### 🚶 Steps Over Time")
            fig3, ax3 = plt.subplots()
            ax3.plot(last_7["Date"], last_7["Steps"], marker="o", color="green")
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Steps")
            ax3.set_title("Steps Walked")
            plt.xticks(rotation=45)
            st.pyplot(fig3)

            # --- Smart Tips ---
            st.markdown("### 💡 Personalized Tips")

            try:
                avg_sleep = round(last_7["Sleep Hours"].mean(), 1)
                avg_water = round(last_7["Water Intake"].mean(), 1)
                avg_steps = int(last_7["Steps"].mean())
                common_mood = last_7["Mood"].mode()[0]

                if avg_sleep < 6:
                    st.warning(f"😴 You're sleeping only {avg_sleep} hrs on average. Try to sleep 7–8 hrs.")
                else:
                    st.success(f"✅ Great! You're averaging {avg_sleep} hrs of sleep.")

                if avg_water < 6:
                    st.warning(f"💧 Water intake is low ({avg_water} glasses avg). Try for 8+.")
                else:
                    st.success(f"✅ Good job on hydration! Avg: {avg_water} glasses.")

                if avg_steps < 5000:
                    st.warning(f"🚶 Only {avg_steps} steps avg. Try to move more daily!")
                else:
                    st.success(f"✅ Active! {avg_steps} steps/day.")

                st.info(f"🧠 Most frequent mood: **{common_mood}**")
            except Exception as e:
                st.error("⚠️ Not enough data for tips yet.")
    else:
        st.warning("No data file found. Submit at least one entry.")

    # --- Reset Data Option ---
    st.markdown("---")
    st.subheader("⚠️ Reset All Data")

    with st.expander("🧹 Click to Reset Wellness Data"):
        st.warning("⚠️ This will permanently delete all saved data. Are you sure?")
        confirm_reset = st.checkbox("Yes, I'm sure. Delete everything.")
        if confirm_reset:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    st.success("✅ All data has been deleted. Please refresh to see changes.")
                except Exception as e:
                    st.error(f"Error deleting file: {e}")
            else:
                st.info("📁 No data file found to delete.")
