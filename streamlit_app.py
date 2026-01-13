import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Inicjalizacja klienta Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

st.title("Zarządzanie Kategoriami Supabase")

# --- SEKCJA DODAWANIA ---
st.header("Dodaj nową kategorię")

# Formularz do dodawania danych
with st.form("category_form", clear_on_submit=True):
    # Nazwy kolumn muszą być identyczne jak na Twoim schemacie: 'kategorie' i 'opis'
    nazwa_input = st.text_input("Nazwa kategorii")
    opis_input = st.text_area("Opis")
    submit_button = st.form_submit_button("Dodaj kategorię")

    if submit_button:
        if nazwa_input:
            try:
                # LINIA 37 (poprawiona): Przekazanie słownika i wywołanie .execute()
                # Brak st.rerun() bezpośrednio tutaj zapobiega błędom przepływu
                query = supabase.table("kategorie").insert({
                    "kategorie": nazwa_input, 
                    "opis": opis_input
                }).execute()
                
                st.success(f"Dodano: {nazwa_input}")
                # Zamiast st.rerun(), używamy mechanizmu powiadomienia użytkownika 
                # lub przycisku odświeżającego poniżej
            except Exception as e:
                st.error(f"Błąd bazy danych: {e}")
        else:
            st.warning("Pole 'Nazwa kategorii' jest wymagane.")

---

# --- SEKCJA LISTY I USUWANIA ---
st.header("Aktualne kategorie")

try:
    # Pobieranie danych z tabeli 'kategorie'
    response = supabase.table("kategorie").select("*").execute()
    data = response.data

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df[["id", "kategorie", "opis"]], use_container_width=True)

        st.subheader("Usuń kategorię")
        selected_item = st.selectbox(
            "Wybierz element do usunięcia",
            options=data,
            format_func=lambda x: f"ID: {x['id']} | {x['kategorie']}"
        )

        if st.button("Usuń zaznaczone", type="primary"):
            try:
                # Usuwanie po ID
                supabase.table("kategorie").delete().eq("id", selected_item['id']).execute()
                st.success("Usunięto pomyślnie!")
                st.rerun() # Tu st.rerun jest bezpieczniejszy (poza st.form)
            except Exception as e:
                st.error(f"Błąd usuwania (sprawdź czy kategoria nie ma przypisanych produktów): {e}")
    else:
        st.info("Baza danych jest pusta.")

except Exception as e:
    st.error(f"Błąd połączenia: {e}")
