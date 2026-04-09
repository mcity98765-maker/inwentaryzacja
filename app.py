
import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import easyocr

# =============================
# KONFIGURACJA STRONY
# =============================
st.set_page_config(
    page_title="Inwentaryzacja",
    page_icon="📸",
    layout="centered"
)

st.title("📸 Inwentaryzacja na żywo")

# =============================
# OCR – cache
# =============================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['pl', 'en'], gpu=False)

reader = load_reader()

# =============================
# SESSION STATE
# =============================
if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "last_room" not in st.session_state:
    st.session_state.last_room = ""

# =============================
# PREPROCESSING OBRAZU
# =============================
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    return gray

# =============================
# DUPLIKATY
# =============================
def is_duplicate(room, desc):
    for item in st.session_state.inventory:
        if item["Pokój"] == room and item["Opis"] == desc:
            return True
    return False

# =============================
# KAMERA
# =============================
foto = st.camera_input(
    "Skieruj aparat na etykietę",
    key="active_camera"
)

show_debug = st.checkbox("🔍 Pokaż szczegóły OCR", value=False)

if foto:
    image = Image.open(foto)
    img_array = np.array(image)

    processed = preprocess_image(img_array)

    with st.spinner("Odczytywanie etykiety..."):
        ocr_result = reader.readtext(processed)
        detected_text = " ".join([r[1] for r in ocr_result])

    st.success("✅ Tekst wykryty")
    st.write(detected_text)

    if show_debug:
        st.subheader("Szczegóły OCR")
        st.json(ocr_result)

    # =============================
    # FORMULARZ ZAPISU
    # =============================
    with st.form("save_form"):
        room = st.text_input(
            "Numer pokoju",
            value=st.session_state.last_room
        )
        description = st.text_area(
            "Opis",
            value=detected_text,
            height=100
        )

        save = st.form_submit_button("💾 ZAPISZ")

        if save:
            if room.strip() == "":
                st.warning("⚠️ Podaj numer pokoju")
            elif is_duplicate(room, description):
                st.warning("⚠️ Ten wpis już istnieje")
            else:
                st.session_state.inventory.append({
                    "Pokój": room,
                    "Opis": description
                })
                st.session_state.last_room = room
                st.success("✅ Zapisano")
                st.rerun()

# =============================
# TABELA WYNIKÓW
# =============================
if st.session_state.inventory:
    st.divider()
    st.subheader("📋 Zebrane elementy")

    df = pd.DataFrame(st.session_state.inventory)
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Pobierz CSV",
            csv,
            "inwentaryzacja.csv",
            "text/csv",
            use_container_width=True
        )

    with col2:
        if st.button("🗑️ Wyczyść listę", use_container_width=True):
            st.session_state.inventory = []
            st.rerun()
``

