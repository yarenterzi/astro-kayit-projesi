import streamlit as st
import pyodbc
import datetime
import os

def connect_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-AVM7HQ8\\YAREN;'
        'DATABASE=deneme1DB;'
        'Trusted_Connection=yes;'
    )
    return conn

def get_zodiac_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 20): return "Koç"
    if (month == 4 and day >= 21) or (month == 5 and day <= 21): return "Boğa"
    if (month == 5 and day >= 22) or (month == 6 and day <= 22): return "İkizler"
    if (month == 6 and day >= 23) or (month == 7 and day <= 22): return "Yengeç"
    if (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Aslan"
    if (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Başak"
    if (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Terazi"
    if (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Akrep"
    if (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Yay"
    if (month == 12 and day >= 22) or (month == 1 and day <= 20): return "Oğlak"
    if (month == 1 and day >= 21) or (month == 2 and day <= 19): return "Kova"
    if (month == 2 and day >= 20) or (month == 3 and day <= 20): return "Balık"

st.title("🔮 Kayıt Sayfası")

name = st.text_input("İsminiz:")
email = st.text_input("E-posta adresiniz:")
birth_date = st.date_input("Doğum Tarihi", datetime.date(2000, 1, 1))
uploaded_file = st.file_uploader("📷 Resim Yükle", type=["jpg", "jpeg", "png"])

if st.button("Kaydet ve Devam Et"):
    if name and email and birth_date and uploaded_file:
        try:
            image_path = f"static/images/{name}_{email}.png"
            os.makedirs("static/images", exist_ok=True)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            zodiac = get_zodiac_sign(birth_date.day, birth_date.month)

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO UserTable1 (UserName, Email, BirthDate, ImagePath) VALUES (?, ?, ?, ?)",
                (name, email, birth_date, image_path)
            )
            conn.commit()

            st.session_state["user_name"] = name
            st.session_state["zodiac"] = zodiac
            st.session_state["image_path"] = image_path

            # Sadece yönlendirme yeterli
            st.switch_page("pages/blog1.py")  # blog.py dosyasının yolu burada önemli

        except Exception as e:
            st.error(f"Hata oluştu: {e}")
    else:
        st.warning("Tüm alanları doldurun.")
