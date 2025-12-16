import streamlit as st

# Inicjalizacja listy produktów (nasz "magazyn")
# Używamy st.session_state do przechowywania danych, aby były trwałe
# podczas interakcji użytkownika w Streamlit.
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = ["Młotek", "Śrubokręt", "Klucz francuski"]

def add_product(product_name):
    """Dodaje produkt do magazynu."""
    if product_name and product_name not in st.session_state['inventory']:
        st.session_state['inventory'].append(product_name)
        st.success(f"Dodano: **{product_name}** do magazynu.")
    elif product_name:
        st.warning(f"Produkt **{product_name}** jest już w magazynie.")
    else:
        st.error("Wprowadź nazwę produktu, aby go dodać.")

def remove_product(product_name):
    """Usuwa produkt z magazynu."""
    if product_name in st.session_state['inventory']:
        st.session_state['inventory'].remove(product_name)
        st.success(f"Usunięto: **{product_name}** z magazynu.")
    else:
        st.error(f"Produkt **{product_name}** nie znajduje się w magazynie.")

## INTERFEJS UŻYTKOWNIKA STREAMLIT

st.title("Prosta Aplikacja Magazynowa 🛠️")
st.markdown("Dodawaj i usuwaj produkty z wirtualnego magazynu. (Bez ilości i cen)")

# --- Sekcja Dodawania Produktu ---
st.header("➕ Dodaj Produkt")
new_product_name = st.text_input("Nazwa produktu do dodania:", key="add_input")

if st.button("Dodaj do Magazynu"):
    add_product(new_product_name)

st.divider()

# --- Sekcja Usuwania Produktu ---
st.header("➖ Usuń Produkt")

# Tworzenie listy rozwijanej z aktualnymi produktami
if st.session_state['inventory']:
    product_to_remove = st.selectbox(
        "Wybierz produkt do usunięcia:",
        st.session_state['inventory'],
        index=None,  # Zaczynamy bez wybranego elementu
        placeholder="Wybierz produkt...",
        key="remove_select"
    )
    if st.button("Usuń z Magazynu"):
        if product_to_remove:
            remove_product(product_to_remove)
        else:
            st.warning("Wybierz produkt z listy, aby go usunąć.")
else:
    st.info("Magazyn jest pusty. Dodaj najpierw jakieś produkty!")


st.divider()

# --- Sekcja Podglądu Magazynu ---
st.header("📊 Aktualny Magazyn")
if st.session_state['inventory']:
    # Wyświetlanie produktów w formie tabeli/listy
    st.dataframe(
        st.session_state['inventory'],
        column_config={"value": "Nazwa Produktu"},
        hide_index=True
    )
else:
    st.info("Magazyn jest pusty.")

st.caption(f"Aktualna liczba produktów: **{len(st.session_state['inventory'])}**")
