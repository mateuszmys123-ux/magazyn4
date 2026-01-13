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
    # Pola zgodne ze schematem: 'kategorie' i 'opis'
    nazwa_kat = st.text_input("Nazwa kategorii")
    opis_kat = st.text_area("Opis")
    submitted = st.form_submit_button("Zapisz")

    if submitted:
        if nazwa_kat:
            try:
                # Wykonanie operacji bez st.rerun wewnątrz try/except
                supabase.table("kategorie").insert({
                    "kategorie": nazwa_kat, 
                    "opis": opis_kat
                }).execute()
                st.success(f"Dodano: {nazwa_kat}. Lista zostanie zaktualizowana.")
                # Zamiast rerun, używamy flagi do odświeżenia poza tym blokiem
                st.session_state['needs_refresh'] = True
            except Exception as e:
                st.error(f"Błąd bazy danych: {e}")
        else:
            st.warning("Nazwa jest wymagana.")

---

# --- SEKCJA LISTY I USUWANIE ---
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
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Usuń zaznaczoną kategorię", type="primary"):
            try:
                supabase.table("kategorie").delete().eq("id", to_delete['id']).execute()
                st.info("Usunięto. Kliknij przycisk poniżej, aby odświeżyć.")
                st.session_state['needs_refresh'] = True
            except Exception as e:
                st.error(f"Błąd: Kategoria może być przypisana do produktu. {e}")
    else:
        st.info("Baza jest pusta.")

except Exception as e:
    st.error(f"Błąd ładowania: {e}")

# JEDYNE MIEJSCE NA ODŚWIEŻENIE - POZA WSZYSTKIMI BLOKAMI TRY
if st.session_state.get('needs_refresh'):
    st.session_state['needs_refresh'] = False
    st.rerun()
