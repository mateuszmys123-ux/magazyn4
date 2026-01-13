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

st.title("Zarządzanie Kategoriami (Supabase)")

# --- SEKCJA: DODAWANIE ---
st.header("Dodaj nową kategorię")
with st.form("add_category_form", clear_on_submit=True):
    # Pola zgodne ze schematem: 'kategorie' (wymagane) i 'opis' (opcjonalne)
    nazwa = st.text_input("Nazwa kategorii")
    opis = st.text_area("Opis")
    submit = st.form_submit_button("Dodaj")

    if submit:
        if nazwa:
            try:
                # Wstawianie danych do tabeli 'kategorie'
                data, count = supabase.table("kategorie").insert({
                    "kategorie": nazwa, 
                    "opis": opis
                }).execute()
                st.success(f"Dodano kategorię: {nazwa}")
                st.rerun()
            except Exception as e:
                st.error(f"Błąd podczas dodawania: {e}")
        else:
            st.warning("Nazwa kategorii jest wymagana.")

---

# --- SEKCJA: LISTA I USUWANIE ---
st.header("Lista kategorii")

try:
    # Pobieranie kategorii ze schematu
    response = supabase.table("kategorie").select("*").execute()
    categories = response.data

    if categories:
        df = pd.DataFrame(categories)
        st.dataframe(df, use_container_width=True)

        st.subheader("Usuń kategorię")
        # Tworzymy listę do wyboru dla użytkownika
        option = st.selectbox(
            "Wybierz kategorię do usunięcia:",
            options=categories,
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Usuń", type="primary"):
            try:
                # Usuwanie po ID
                supabase.table("kategorie").delete().eq("id", option['id']).execute()
                st.success("Kategoria została usunięta!")
                st.rerun()
            except Exception as e:
                st.error(f"Nie można usunąć kategorii. Upewnij się, że nie jest przypisana do produktów. Błąd: {e}")
    else:
        st.info("Brak kategorii w bazie danych.")

except Exception as e:
    st.error(f"Błąd połączenia: {e}")
