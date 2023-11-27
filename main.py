import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
import os

# Authentication function
def authenticate(username, password, user_info):
    if username in user_info.index and password == user_info.loc[username, "password"]:
        return True
    return False

# Stress detection quiz function
def stress_detection_page():
    st.title("STRESS ME OUT")
    st.write("Pilihlah sesuai dengan kondisi Anda hari ini.")

    # Questions
    questions = [
        "Seberapa sering anda merasa kewalahan dengan pekerjaan Anda?",
        "Apakah Anda sering mengalami kesulitan untuk tidur?",
        "Seberapa sering Anda merasakan gugup sebelum melakukan suatu aktivitas?",
    ]

    # User responses
    user_responses = {}

    # Quiz buttons
    for i, question in enumerate(questions, start=1):
        user_response = st.radio(f"Q{i}: {question}", options=["Tidak pernah", "Jarang", "Sering", "Setiap saat"])
        numerical_response = {"Tidak pernah": 0, "Jarang": 1, "Sering": 2, "Setiap saat": 3}
        user_responses[f"Q{i}"] = numerical_response[user_response]

    # Save responses to CSV
    save_responses(user_responses)

    stress_level = calculate_stress_level(user_responses)

    # Display stress level
    st.subheader("Stress Level:")
    if stress_level == "Rendah":
        st.success(f"😊 Stress level Anda {stress_level}! Menjaga tingkat stres tetap rendah adalah kunci untuk keseja")
    elif stress_level == "Normal":
        st.warning(f"😐 Stress level Anda {stress_level}. Menjaga tingkat stres tetap normal melibatkan sejumlah kegia")
    else:
        st.error(f"😰 Stress level Anda {stress_level}. Menurunkan tingkat stres tinggi melibatkan inisiatif dari diri")

    # Display recommendations based on stress level
    st.subheader("Apa yang harus dilakukan?")
    if stress_level == "Rendah":
        st.success(f"Karena Stress level Anda {stress_level}, Anda dapat meningkatkan ibadah kepada Tuhan Yang Maha Es")
    elif stress_level == "Normal":
        st.warning(f"Karena Stress level Anda {stress_level}, Anda dapat berolahraga dengan teratur, melakukan hobi An")
    else:
        st.error(f"Karena Stress level Anda {stress_level}. Anda dapat membicarakan keluhan Anda kepada seseorang yang")

# Calculate stress level function
def calculate_stress_level(user_responses):
    total_response = sum(user_responses.values())
    
    if total_response <= 3:
        return "Rendah"
    elif total_response <= 6:
        return "Normal"
    else:
        return "Tinggi"

# Save responses to CSV function
def save_responses(user_responses):
    today = datetime.now().date()
    filename = f"weekly_report_{today}.csv"

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date"] + list(user_responses.keys()))

    new_data = pd.DataFrame({"Date": [today], **user_responses})
    df = pd.concat([df, new_data], ignore_index=True)

    df.to_csv(filename, index=False)

# Reset weekly report function
def reset_weekly_report():
    filename = f"weekly_report_{datetime.now().date()}.csv"
    try:
        os.remove(filename)
        st.success("🔄 Weekly Report sudah direset!")
    except FileNotFoundError:
        st.warning("Tidak ada Weekly Report untuk direset.")

# Generate weekly report function
def generate_weekly_report():
    st.title("Laporan Weekly Stress")
    try:
        latest_report = pd.read_csv(f"weekly_report_{datetime.now().date()}.csv")
        st.write("Weekly report terakhir")
        st.table(latest_report)
    except FileNotFoundError:
        st.warning("Tidak ada Weekly Report untuk minggu ini.")

# Sign-up page function
def sign_up():
    st.title("Sign Up")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password", key="new_password")

    if st.button("Sign Up 👉"):
        if new_username.strip() == "":
            st.error("Username tidak boleh kosong.")
        else:
            user_info = pd.DataFrame({"password": [new_password]}, index=[new_username])
            user_info.to_csv("user_info.csv")
            st.success(f"✅ User {new_username} successfully signed up!")

# Psychologist recommendation page function
def recommend_nearest_psychologist_page(user_location):
    psychologist_info = {
        "Bandar Lampung": [
            {"name": "Psikolog Yurni, M.Psi.", "profile_link": "https://www.halodoc.com/tanya-dokter/yurni-m-psi-psikolog", "image_path": r"C:\Users\rynko\Documents\nyobaaaaa\profil pa yurni.png"}
        ],
        "Metro": [
            {"name": "Octa Reni Setiawati, S.Psi, M.Psi, Psikolog", "profile_link": "https://www.praktikpsikologi.com/", "image_path": r"C:\Users\rynko\Documents\nyobaaaaa\bu okta.jpg"}
        ],
        "Jakarta": [
            {"name": "Jennyfer, M.Psi., Psikolog", "profile_link": "https://www.instagram.com/jen.psikolog/", "image_path": r"C:\Users\rynko\Documents\nyobaaaaa\download.jpeg"}
        ],
        "Surabaya": [
            {"name": "Ratna Sari M.Psi.,Psikolog", "profile_link": "https://ertamentari.com/", "image_path": r"C:\Users\rynko\Documents\nyobaaaaa\bu ratna.jpg"}
        ],
        "Yogyakarta": [
            {"name": "Mirza Adi Prabowo, M.Psi., Psikolog", "profile_link": "https://mirzaadi.my.id/", "image_path": r"C:\Users\rynko\Documents\nyobaaaaa\pa mirza.jpeg"}
        ],
        "Medan": [
            {"name": "Dr. Manahap Cerarius Fransiskus Pardosi M.Ked, Sp.KJ", "profile_link": "https://www.halodoc.com/tanya-dokter/dr-manahap-cerarius-fransiskus-pard", "image_path": r"C:\Users\rynko\Documents\nyobaaaaa\pa mana.png"}
        ],
        "Makassar": [
            {"name": "Widia Julianti Siddik, S.Psi., M.Psi., Psikolog", "profile_link": "https://widiapsi.carrd.co/", "image_path": r"C:\Users\rynko\Documents\nyobaaaaa\bu widi.png"}
        ]
    }

    psychologists = psychologist_info.get(selected_city, [])

    for psychologist in psychologists:
        st.success(f"Psikolog terdekat untuk Anda di {selected_city}: {psychologist['name']}")
        st.markdown(f"Link Halodoc: [{psychologist['name']}]({psychologist['profile_link']})")
        image = Image.open(psychologist["image_path"])
        st.image(image, caption=f"Profil Psikolog {psychologist['name']}", use_column_width=True)

# Main function
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Add image
    image = Image.open(r"C:\Users\rynko\Documents\nyobaaaaa\gambar web.jpg")
    st.image(image, caption="STRESS ME OUT", use_column_width=True)

    if not st.session_state.logged_in:
        st.title("Login Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login 👉"):
            user_info = pd.read_csv("user_info.csv", index_col=0)
            if authenticate(username, password, user_info):
                st.session_state.logged_in = True
                st.success("🎉 Berhasil log-in!")
            else:
                st.error("❌ Username atau password tidak valid.")

        st.subheader("Sign up:")
        sign_up()
    else:
        stress_detection_page()

        if st.button("Buat Weekly Report"):
            generate_weekly_report()
        if st.button("Reset Weekly Report"):
            reset_weekly_report()

# Recommendation of the Nearest Psychologist
st.title("Rekomendasi Psikolog Terdekat")
cities = ["Bandar Lampung", "Metro", "Jakarta", "Surabaya", "Yogyakarta", "Medan", "Makassar"]
selected_city = st.selectbox("Pilih kota Anda:", cities, key="selected_city_dropdown")

if st.button("Cari Psikolog Terdekat"):
    try:
        city_coordinates = {
            "Bandar Lampung": (-5.3971, 105.2663),
            "Metro": (-5.1136, 105.3067),
            "Jakarta": (-6.2088, 106.8456),
            "Surabaya": (-7.2575, 112.7521),
            "Yogyakarta": (-7.7971, 110.3688),
            "Medan": (3.5896, 98.6731),
            "Makassar": (-5.1477, 119.4327)
        }
        user_location = city_coordinates.get(selected_city)

        if user_location:
            recommend_nearest_psychologist_page(user_location)
        else:
            st.error("Kota tidak valid. Pilih kota dari dropdown.")
    except KeyError:
        st.error("Terjadi kesalahan dalam memproses. Silakan coba lagi.")

if __name__ == "__main__":
    main()
