import streamlit as st
import numpy as np
from PIL import Image
import easyocr

# 1. Konfiguracja strony
st.set_page_config(page_title="Inwentaryzacja", page_icon="🗄️")

st.title("📸 Inwentaryzacja Mebli")

# 2. Inicjalizacja czytnika OCR (wczytywanie raz)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['pl', 'en'])

reader = load_reader()

# 3. Baza danych w sesji
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# 4. Aparat fotograficzny
img_file = st.camera_input("Zrób zdjęcie etykiety")

if img_file:
    image = Image.open(img_file)
    img_array = np.array(image)
    
    with st.spinner('Odczytywanie danych...'):
        # OCR wyciąga tekst
        results = reader.readtext(img_array, detail=0)
        detected_text = " ".join(results)

    st.success(f"Wykryto: {detected_text}")

    # Formularz wpisywania danych
    with st.form("entry_form"):
        pokoj = st.text_input("Numer pokoju")
        opis = st.text_area("Dane z etykiety (możesz edytować)", value=detected_text)
        submit = st.form_submit_button("Zapisz mebel")

        if submit:
            st.session_state.inventory.append({"Pokój": pokoj, "Opis": opis})
            st.success("Dodano do listy!")

# 5. Wyświetlanie tabeli
if st.session_state.inventory:
    st.divider()
    st.subheader("Lista zainwentaryzowanych mebli")
    st.table(st.session_state.inventory)
    
    if st.button("Wyczyść wszystko"):
        st.session_state.inventory = []
        st.rerun()
