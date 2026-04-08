import streamlit as st
import numpy as np
from PIL import Image
import easyocr

# Konfiguracja - musi być na samym początku
st.set_page_config(page_title="Inwentaryzacja", layout="centered")

st.title("📸 Inwentaryzacja Mebli")

# Ładowanie modelu OCR
@st.cache_resource
def get_reader():
    return easyocr.Reader(['pl', 'en'], gpu=False)

try:
    reader = get_reader()
except Exception as e:
    st.error("Błąd ładowania silnika OCR. Sprawdź requirements.txt")
    st.stop()

# Baza danych w pamięci
if 'lista' not in st.session_state:
    st.session_state.lista = []

# APARAT
foto = st.camera_input("Zrób zdjęcie etykiety")

if foto:
    img = Image.open(foto)
    img_array = np.array(img)
    
    with st.spinner('Odczytywanie...'):
        # Pobieramy tekst
        wynik = reader.readtext(img_array, detail=0)
        tekst_ocr = " ".join(wynik)
    
    st.success(f"Wykryto: {tekst_ocr}")

    # Formularz
    with st.form("dodawanie"):
        nr_pokoju = st.text_input("Numer pokoju")
        opis_mebla = st.text_area("Co to jest? (Edytuj jeśli trzeba)", value=tekst_ocr)
        przycisk = st.form_submit_button("ZAPISZ DO LISTY")
        
        if przycisk:
            st.session_state.lista.append({
                "Pokój": nr_pokoju,
                "Opis": opis_mebla
            })
            st.toast("Zapisano!")

# Wyświetlanie tabeli
if st.session_state.lista:
    st.write("### Twoje zapisane meble:")
    st.table(st.session_state.lista)
    
    if st.button("Wyczyść wszystko"):
        st.session_state.lista = []
        st.rerun()
