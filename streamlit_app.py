import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Inicjalizacja połączenia
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

st.title("Zarządzanie Kategoriami")

# --- SEKCJA DODAWANIA ---
st.header("Dodaj nową kategorię")
with st.form("category_form", clear_on_submit=True):
    nazwa_kat = st.text_input("Nazwa kategorii")
    opis_kat = st.text_area("Opis")
    submitted = st.form_submit_button("Zapisz")

    success = False
    if submitted:
        if nazwa_kat:
            try:
                # Wykonanie zapisu
                supabase.table("kategorie").insert({
                    "kategorie": nazwa_kat, 
                    "opis": opis_kat
                }).execute()
                success = True
            except Exception as e:
                st.error(f"Błąd bazy danych: {e}")
        else:
            st.warning("Nazwa jest wymagana.")

# Kluczowa zmiana: st.rerun() musi być POZA blokiem try/except formularza
if success:
    st.success(f"Dodano: {nazwa_kat}")
    st.rerun()

---

# --- SEKCJA LISTA I USUWANIE ---
st.header("Lista kategorii")

try:
    # Pobieranie danych
    response = supabase.table("kategorie").select("*").execute()
    items = response.data

    if items:
        df = pd.DataFrame(items)
        st.dataframe(df[["id", "kategorie", "opis"]], use_container_width=True)

        st.subheader("Usuń kategorię")
        to_delete = st.selectbox(
            "Wybierz do usunięcia", 
            options=items, 
            key="delete_box",
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        delete_clicked = st.button("Usuń", type="primary")
        
        delete_success = False
        if delete_clicked:
            try:
                supabase.table("kategorie").delete().eq("id", to_delete['id']).execute()
                delete_success = True
            except Exception as e:
                st.error(f"Nie można usunąć (prawdopodobnie kategoria ma produkty): {e}")
        
        # Odświeżenie po usunięciu (również poza try/except)
        if delete_success:
            st.rerun()
            
    else:
        st.info("Brak danych.")
except Exception as e:
    st.error(f"Błąd ładowania danych: {e}")
