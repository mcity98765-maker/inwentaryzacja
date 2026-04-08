import streamlit as st
import numpy as np
from PIL import Image
import easyocr

# Konfiguracja strony
st.set_page_config(page_title="Inwentaryzator Mebli", page_icon="🗄️")

st.title("📸 Inwentaryzacja Mebli")
st.write("Zrób zdjęcie etykiety, a ja spróbuję odczytać tekst.")

# Inicjalizacja czytnika OCR (wczytuje się raz)
@st.cache_resource
def load_reader():
    # 'pl' dla polskiego, 'en' dla angielskiego
    return easyocr.Reader(['pl', 'en'])

reader = load_reader()

# Inicjalizacja bazy w pamięci sesji
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# Miejsce na zrobienie zdjęcia (wersja file_uploader - działa na każdym telefonie)
img_file = st.file_uploader("Zrób zdjęcie", type=['png', 'jpg', 'jpeg'])

if img_file:
    # Przetwarzanie obrazu
    image = Image.open(img_file)
    img_array = np.array(image)
    
    # Odczyt tekstu
    with st.spinner('Odczytywanie etykiety...'):
        results = reader.readtext(img_array, detail=0)
        detected_text = " ".join(results)

    st.success(f"Wykryty tekst: {detected_text}")

    # Formularz dodawania danych
    with st.form("entry_form"):
        pokoj = st.text_input("Numer pokoju", placeholder="np. 204")
        opis = st.text_area("Edytuj dane z etykiety", value=detected_text)
        submit = st.form_submit_button("Dodaj do listy")

        if submit:
            st.session_state.inventory.append({
                "Pokój": pokoj,
                "Dane z etykiety": opis
            })
            st.toast("Dodano do spisu!")

# Wyświetlanie tabeli z wynikami
if st.session_state.inventory:
    st.divider()
    st.subheader("Twój spis (do skopiowania do Excela)")
    st.table(st.session_state.inventory)
    
    if st.button("Wyczyść listę"):
        st.session_state.inventory = []
        st.rerun()
