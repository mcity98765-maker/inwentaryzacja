import streamlit as st
import numpy as np
from PIL import Image
import easyocr

st.set_page_config(page_title="Inwentaryzacja", layout="centered")

# Funkcja OCR
@st.cache_resource
def load_reader():
    return easyocr.Reader(['pl', 'en'], gpu=False)

reader = load_reader()

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

st.title("📸 Inwentaryzacja na żywo")

# WYMUSZENIE KAMERY
# Dodajemy unikalny klucz, aby Streamlit za każdym razem odświeżał moduł
foto = st.camera_input("Skieruj aparat na etykietę", key="active_camera_v3")

if foto:
    img = Image.open(foto)
    img_array = np.array(img)
    
    with st.spinner('Odczytywanie...'):
        results = reader.readtext(img_array, detail=0)
        tekst = " ".join(results)
    
    st.success(f"Wykryto: {tekst}")

    with st.form("add_form"):
        pokoj = st.text_input("Numer pokoju")
        opis = st.text_area("Edytuj dane", value=tekst)
        if st.form_submit_button("ZAPISZ"):
            st.session_state.inventory.append({"Pokój": pokoj, "Opis": opis})
            st.rerun()

if st.session_state.inventory:
    st.divider()
    st.table(st.session_state.inventory)
    if st.button("Wyczyść listę"):
        st.session_state.inventory = []
        st.rerun()
