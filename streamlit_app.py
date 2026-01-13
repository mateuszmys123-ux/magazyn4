import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Połączenie z Supabase przy użyciu Secrets
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

st.title("Zarządzanie Kategoriami")

# --- SEKCJA DODAWANIE ---
st.header("Dodaj nową kategorię")
with st.form("category_form", clear_on_submit=True):
    # Nazwy pól muszą pasować do bazy: 'kategorie' i 'opis'
    nazwa_kat = st.text_input("Nazwa kategorii")
    opis_kat = st.text_area("Opis")
    submitted = st.form_submit_button("Zapisz")

    if submitted:
        if nazwa_kat:
            try:
                # Wykonanie zapisu bez przypisywania do zmiennej, aby uniknąć błędów typu 'NoneType'
                supabase.table("kategorie").insert({
                    "kategorie": nazwa_kat, 
                    "opis": opis_kat
                }).execute()
                
                st.success(f"Dodano: {nazwa_kat}. Odśwież stronę, aby zobaczyć zmiany.")
            except Exception as e:
                st.error(f"Błąd zapisu w linii 37-44: {e}")
        else:
            st.warning("Nazwa jest wymagana.")

---

# --- SEKCJA LISTA I USUWANIE ---
st.header("Lista kategorii")

try:
    # Pobieranie rekordów
    response = supabase.table("kategorie").select("*").execute()
    items = response.data

    if items:
        df = pd.DataFrame(items)
        st.dataframe(df[["id", "kategorie", "opis"]], use_container_width=True)

        st.subheader("Usuń kategorię")
        # x['id'] to bigint z Twojego schematu
        to_delete = st.selectbox(
            "Wybierz do usunięcia", 
            options=items, 
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Usuń", type="primary"):
            try:
                # Usuwanie po ID
                supabase.table("kategorie").delete().eq("id", to_delete['id']).execute()
                st.success("Usunięto!")
                st.rerun() 
            except Exception as e:
                st.error(f"Nie można usunąć – kategoria może być używana w produktach. Błąd: {e}")
    else:
        st.info("Brak danych w tabeli.")

except Exception as e:
    st.error(f"Błąd połączenia: {e}")
