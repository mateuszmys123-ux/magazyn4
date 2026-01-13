import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Inicjalizacja połączenia z Supabase przy użyciu Secrets
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

st.set_page_config(page_title="Supabase Category Manager", layout="centered")
st.title("📂 Zarządzanie Kategoriami")

# --- SEKCJA: DODAWANIE KATEGORII ---
st.header("Dodaj nową kategorię")
with st.form("add_category_form", clear_on_submit=True):
    # Nazwy pól zgodne z kolumnami w Twojej bazie danych
    nazwa = st.text_input("Nazwa kategorii (kolumna: kategorie)")
    opis = st.text_area("Opis (kolumna: opis)")
    submit = st.form_submit_button("Dodaj do bazy")

    if submit:
        if nazwa:
            try:
                # Linia 41: Poprawne wykonanie zapisu i natychmiastowe odświeżenie danych
                supabase.table("kategorie").insert({
                    "kategorie": nazwa, 
                    "opis": opis
                }).execute()
                
                st.success(f"Dodano kategorię: {nazwa}")
                st.rerun()  # Wymuszenie odświeżenia, aby nowa kategoria pojawiła się na liście
            except Exception as e:
                st.error(f"Wystąpił błąd podczas zapisu: {e}")
        else:
            st.warning("Musisz podać nazwę kategorii.")

---

# --- SEKCJA: WYŚWIETLANIE I USUWANIE ---
st.header("Aktualna lista kategorii")

try:
    # Pobranie wszystkich kategorii
    response = supabase.table("kategorie").select("*").execute()
    categories = response.data

    if categories:
        # Prezentacja danych w tabeli
        df = pd.DataFrame(categories)
        st.dataframe(df[["id", "kategorie", "opis"]], use_container_width=True)

        st.subheader("Usuń kategorię")
        # Wybór rekordu do usunięcia
        selected_cat = st.selectbox(
            "Wybierz kategorię do usunięcia:",
            options=categories,
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Usuń trwale", type="primary"):
            try:
                # Usuwanie na podstawie klucza głównego 'id'
                supabase.table("kategorie").delete().eq("id", selected_cat['id']).execute()
                st.success("Kategoria została usunięta.")
                st.rerun()
            except Exception as e:
                st.error(f"Błąd: Nie można usunąć kategorii, jeśli są do niej przypisane produkty. {e}")
    else:
        st.info("Brak kategorii w bazie.")

except Exception as e:
    st.error(f"Problem z połączeniem: {e}")
