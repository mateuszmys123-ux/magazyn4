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
    nazwa_kat = st.text_input("Nazwa")
    opis_kat = st.text_area("Opis")
    submitted = st.form_submit_button("Dodaj")

    if submitted:
        if nazwa_kat:
            # POPRAWIONA LINIA 41 I OKOLICE:
            # Rozbicie na mniejsze kroki zapobiega błędom wykonania
            try:
                data_to_insert = {"kategorie": nazwa_kat, "opis": opis_kat}
                supabase.table("kategorie").insert(data_to_insert).execute()
                st.success(f"Dodano: {nazwa_kat}")
                st.button("Odśwież listę") # Alternatywa dla st.rerun wewnątrz form
            except Exception as e:
                st.error(f"Błąd Supabase: {e}")
        else:
            st.warning("Nazwa jest wymagana.")

---

# --- SEKCJA LISTY I USUWANIA ---
st.header("Lista")

try:
    # Pobieranie danych
    res = supabase.table("kategorie").select("*").execute()
    items = res.data

    if items:
        df = pd.DataFrame(items)
        st.dataframe(df, use_container_width=True)

        st.subheader("Usuń wpis")
        to_delete = st.selectbox(
            "Wybierz do usunięcia", 
            options=items, 
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Usuń", type="primary"):
            supabase.table("kategorie").delete().eq("id", to_delete['id']).execute()
            st.success("Usunięto!")
            st.rerun()
    else:
        st.info("Brak danych.")
except Exception as e:
    st.error(f"Błąd: {e}")
