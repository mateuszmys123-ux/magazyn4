import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Inicjalizacja połączenia z Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

st.set_page_config(page_title="Zarządzanie Kategoriami", layout="centered")
st.title("📂 Panel Administratora: Kategorie")

# --- SEKCJA: DODAWANIE ---
st.header("Dodaj nową kategorię")
with st.form("form_dodawania", clear_on_submit=True):
    # Pola zgodne ze schematem: 'kategorie' oraz 'opis'
    nazwa_kat = st.text_input("Nazwa kategorii")
    opis_kat = st.text_area("Opis")
    submit = st.form_submit_button("Zapisz w bazie")

    if submit:
        if nazwa_kat:
            try:
                # LINIA 41: Poprawne i bezpieczne wywołanie insert
                supabase.table("kategorie").insert({
                    "kategorie": nazwa_kat, 
                    "opis": opis_kat
                }).execute()
                
                st.success(f"Dodano kategorię: {nazwa_kat}")
                st.rerun()  # Odświeżenie interfejsu
            except Exception as e:
                st.error(f"Błąd zapisu: {e}")
        else:
            st.warning("Pole 'Nazwa kategorii' jest wymagane.")

---

# --- SEKCJA: LISTA I USUWANIE ---
st.header("Lista wszystkich kategorii")

try:
    # Pobranie danych
    response = supabase.table("kategorie").select("*").execute()
    dane = response.data

    if dane:
        df = pd.DataFrame(dane)
        # Wyświetlamy tabelę (id, kategorie, opis)
        st.dataframe(df[["id", "kategorie", "opis"]], use_container_width=True)

        st.subheader("Usuń kategorię")
        # Wybór wiersza do usunięcia
        wybrana_opcja = st.selectbox(
            "Wybierz kategorię do skasowania:",
            options=dane,
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Potwierdź usunięcie", type="primary"):
            try:
                # Usuwanie na podstawie ID
                supabase.table("kategorie").delete().eq("id", wybrana_opcja['id']).execute()
                st.success("Usunięto pomyślnie!")
                st.rerun()
            except Exception as e:
                st.error(f"Nie można usunąć. Kategoria może być używana w tabeli produkty. Szczegóły: {e}")
    else:
        st.info("Baza danych jest pusta.")

except Exception as e:
    st.error(f"Błąd komunikacji z Supabase: {e}")
