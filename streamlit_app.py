import streamlit as st
import psycopg2
import pandas as pd

# Funkcja nawiązująca połączenie z bazą danych
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        port=st.secrets["DB_PORT"]
    )

st.set_page_config(page_title="Zarządzanie Kategoriami", layout="centered")
st.title("📦 System Zarządzania Kategoriami")

# --- SEKCJA 1: DODAWANIE KATEGORII ---
st.header("Dodaj Nową Kategorię")
with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 2])
    with col1:
        nazwa = st.text_input("Nazwa kategorii (wymagane)")
    with col2:
        opis = st.text_input("Opis (opcjonalne)")
    
    submit = st.form_submit_button("Dodaj do bazy")

    if submit:
        if nazwa:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO kategorie (kategorie, opis) VALUES (%s, %s)",
                    (nazwa, opis)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"Pomyślnie dodano kategorię: {nazwa}")
            except Exception as e:
                st.error(f"Błąd bazy danych: {e}")
        else:
            st.warning("Proszę podać nazwę kategorii.")

---

# --- SEKCJA 2: LISTA I USUWANIE ---
st.header("Aktualne Kategorie")

try:
    conn = get_connection()
    # Pobieramy kategorie oraz licznik produktów, które do nich należą (dla bezpieczeństwa)
    query = """
        SELECT k.id, k.kategorie, k.opis, COUNT(p.id) as liczba_produktow
        FROM kategorie k
        LEFT JOIN produkty p ON k.id = p.kategoria_id
        GROUP BY k.id
        ORDER BY k.id DESC
    """
    df = pd.read_sql_query(query, conn)
    
    if not df.empty:
        # Wyświetlanie tabeli
        st.dataframe(df[['id', 'kategorie', 'opis', 'liczba_produktow']], use_container_width=True)

        # Usuwanie
        st.subheader("Usuń Kategorię")
        selected_cat_id = st.selectbox(
            "Wybierz kategorię do usunięcia",
            options=df['id'].tolist(),
            format_func=lambda x: f"ID: {x} | {df[df['id']==x]['kategorie'].values[0]}"
        )

        # Sprawdzenie czy kategoria ma przypisane produkty
        products_count = df[df['id'] == selected_cat_id]['liczba_produktow'].values[0]

        if st.button("Usuń wybraną kategorię", type="primary"):
            if products_count > 0:
                st.error(f"Nie można usunąć tej kategorii! Jest do niej przypisanych {products_count} produktów.")
            else:
                cur = conn.cursor()
                cur.execute("DELETE FROM kategorie WHERE id = %s", (int(selected_cat_id),))
                conn.commit()
                cur.close()
                st.success("Kategoria została usunięta.")
                st.rerun()
    else:
        st.info("Brak kategorii w bazie danych.")
    
    conn.close()
except Exception as e:
    st.error(f"Błąd połączenia: {e}")
