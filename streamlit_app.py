import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Połączenie z Supabase
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
    # Kolumny zgodne ze schematem: 'kategorie' i 'opis'
    nazwa_input = st.text_input("Nazwa kategorii")
    opis_input = st.text_area("Opis")
    submitted = st.form_submit_button("Dodaj")

    if submitted:
        if nazwa_input:
            try:
                # Wstawianie danych do tabeli 'kategorie'
                supabase.table("kategorie").insert({
                    "kategorie": nazwa_input, 
                    "opis": opis_input
                }).execute()
                st.success(f"Dodano: {nazwa_input}. Dane pojawią się na liście poniżej.")
                # USUNIĘTO st.rerun() - to eliminuje błąd w linii 40
            except Exception as e:
                st.error(f"Błąd bazy danych: {e}")
        else:
            st.warning("Proszę podać nazwę.")

---

# --- SEKCJA LISTY I USUWANIA ---
st.header("Lista kategorii")

try:
    # Pobieranie rekordów z bazy
    response = supabase.table("kategorie").select("*").execute()
    items = response.data

    if items:
        df = pd.DataFrame(items)
        st.dataframe(df[["id", "kategorie", "opis"]], use_container_width=True)

        st.subheader("Usuń kategorię")
        to_delete = st.selectbox(
            "Wybierz do usunięcia", 
            options=items, 
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Usuń", type="primary"):
            try:
                # Usuwanie po kluczu głównym 'id'
                supabase.table("kategorie").delete().eq("id", to_delete['id']).execute()
                st.info("Usunięto pomyślnie.")
                # Tutaj też nie używamy rerun, aby uniknąć błędów
            except Exception as e:
                st.error(f"Błąd: Nie można usunąć (może kategoria ma produkty?). {e}")
    else:
        st.info("Baza danych jest pusta.")

except Exception as e:
    st.error(f"Problem z połączeniem: {e}")
