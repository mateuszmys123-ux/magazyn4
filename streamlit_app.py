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

st.set_page_config(page_title="Supabase Manager", layout="centered")
st.title("📂 Zarządzanie Kategoriami Produktów")

# --- SEKCJA: DODAWANIE ---
st.header("Dodaj nową kategorię")
with st.form("add_category_form", clear_on_submit=True):
    # Pola zgodne ze schematem z rysunku
    nazwa = st.text_input("Nazwa kategorii (kolumna: kategorie)")
    opis = st.text_area("Opis (kolumna: opis)")
    submit = st.form_submit_button("Dodaj do bazy")

    if submit:
        if nazwa:
            try:
                # POPRAWIONA LINIA 39: Poprawne wywołanie insert dla Supabase
                supabase.table("kategorie").insert({
                    "kategorie": nazwa, 
                    "opis": opis
                }).execute()
                
                st.success(f"Pomyślnie dodano kategorię: {nazwa}")
                st.rerun()
            except Exception as e:
                st.error(f"Błąd podczas dodawania: {e}")
        else:
            st.warning("Pole 'Nazwa kategorii' jest wymagane.")

---

# --- SEKCJA: LISTA I USUWANIE ---
st.header("Aktualne kategorie")

try:
    # Pobieranie danych z Supabase
    response = supabase.table("kategorie").select("*").execute()
    categories = response.data

    if categories:
        # Konwersja do DataFrame dla ładnego wyświetlania
        df = pd.DataFrame(categories)
        st.dataframe(df, use_container_width=True)

        st.subheader("Usuń kategorię")
        # Menu wyboru kategorii do usunięcia
        option = st.selectbox(
            "Wybierz kategorię do usunięcia:",
            options=categories,
            format_func=lambda x: f"ID: {x['id']} | Nazwa: {x['kategorie']}"
        )

        if st.button("Usuń wybraną kategorię", type="primary"):
            try:
                # Usuwanie rekordu na podstawie ID
                supabase.table("kategorie").delete().eq("id", option['id']).execute()
                st.success(f"Kategoria '{option['kategorie']}' została usunięta.")
                st.rerun()
            except Exception as e:
                st.error(f"Nie można usunąć kategorii. Może być powiązana z produktami. Błąd: {e}")
    else:
        st.info("Baza danych kategorii jest obecnie pusta.")

except Exception as e:
    st.error(f"Błąd połączenia z API Supabase: {e}")
