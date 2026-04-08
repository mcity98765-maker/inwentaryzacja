import streamlit as st
import numpy as np
from PIL import Image
import easyocr

# Konfiguracja strony
st.set_page_config(page_title="Inwentaryzacja")

st.title("📸 Inwentaryzacja Mebli")

# Funkcja ładująca model (z zabezpieczeniem)
@st.cache_resource
def load_model():
    return easyocr.Reader(['pl', 'en'], gpu=False)

# Próba załadowania modelu
try:
    reader = load_model()
except Exception as e:
    st.error(f"Problem z ładowaniem modelu: {e}")
    st.stop()

# Baza w pamięci
if 'lista' not in st.session_state:
    st.session_state.lista = []

# APARAT
st.write("Kliknij poniżej, aby zrobić zdjęcie:")
foto = st.camera_input("Zrób zdjęcie etykiety")

if foto:
    img = Image.open(foto)
    img_array = np.array(img)
    
    with st.spinner('Odczytywanie...'):
        wynik = reader.readtext(img_array, detail=0)
        tekst_ocr = " ".join(wynik)
    
    st.success(f"Odczytano: {tekst_ocr}")

    with st.form("formularz"):
        pokoj = st.text_input("Numer pokoju")
        opis = st.text_area("Opis (z etykiety)", value=tekst_ocr)
        zapisz = st.form_submit_button("ZAPISZ DO LISTY")
        
        if zapisz:
            st.session_state.lista.append({"Pokój": pokoj, "Opis": opis})
            st.toast("Dodano!")

# Wyświetlanie tabeli
if st.session_state.lista:
    st.divider()
    st.write("### Spis mebli:")
    st.table(st.session_state.lista)
    
    if st.button("Wyczyść listę"):
        st.session_state.lista = []
        st.rerun()
