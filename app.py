import streamlit as st
import numpy as np
from PIL import Image
import easyocr

# Konfiguracja strony
st.set_page_config(page_title="Inwentaryzator Mebli", page_icon="🗄️")

st.title("📸 Inwentaryzacja Mebli")

# WAŻNE: To wymusza na przeglądarce odświeżenie sterownika
if 'camera_key' not in st.session_state:
    st.session_state.camera_key = "camera_1"

# Inicjalizacja czytnika OCR
@st.cache_resource
def load_reader():
    return easyocr.Reader(['pl', 'en'])

reader = load_reader()

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# Powrót do st.camera_input - robienie zdjęcia "na żywo"
img_file = st.camera_input("Skieruj aparat na etykietę", key=st.session_state.camera_key)

if img_file:
    image = Image.open(img_file)
    img_array = np.array(image)
    
    with st.spinner('Odczytywanie...'):
        results = reader.readtext(img_array, detail=0)
        detected_text = " ".join(results)

    st.success(f"Wykryto: {detected_text}")

    with st.form("entry_form"):
        pokoj = st.text_input("Numer pokoju")
        opis = st.text_area("Dane z etykiety", value=detected_text)
        submit = st.form_submit_button("Dodaj do listy")

        if submit:
            st.session_state.inventory.append({"Pokój": pokoj, "Opis": opis})
            # Zmieniamy klucz aparatu, żeby go "zresetować" po zrobieniu zdjęcia
            st.session_state.camera_key = f"camera_{np.random.randint(1000)}"
            st.rerun()

if st.session_state.inventory:
    st.divider()
    st.table(st.session_state.inventory)
    if st.button("Wyczyść listę"):
        st.session_state.inventory = []
        st.rerun()
