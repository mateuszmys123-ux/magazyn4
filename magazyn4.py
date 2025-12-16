import streamlit as st

# --- KONFIGURACJA ŚWIĄTECZNEGO TŁA ---
def add_christmas_bg():
    st.markdown(
        """
        <style>
        /* Ustawienie tła dla głównego kontenera aplikacji */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1544967082-d9d25d867d66?q=80&w=1920&auto=format&fit=crop");
            background-attachment: fixed;
            background-size: cover;
        }
        
        /* Opcjonalnie: Dodanie półprzezroczystego tła pod tekst, żeby był czytelny */
        div[data-testid="stVerticalBlock"] > div {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Wywołanie funkcji ustawiającej tło
add_christmas_bg()

# --- LOGIKA APLIKACJI (BACKEND) ---

# Inicjalizacja listy produktów (nasz "magazyn")
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = ["Młotek", "Śrubokręt", "Klucz francuski"]

def add_product(product_name):
    """Dodaje produkt do magazynu."""
    if product_name and product_name not in st.session_state['inventory']:
        st.session_state['inventory'].append(product_name)
        st.success(f"Dodano prezent: **{product_name}** 🎁")
    elif product_name:
        st.warning(f"Ten produkt (**{product_name}**) już leży pod choinką! 🎄")
    else:
        st.error("Wpisz nazwę, aby dodać prezent.")

def remove_product(product_name):
    """Usuwa produkt z magazynu."""
    if product_name in st.session_state['inventory']:
        st.session_state['inventory'].remove(product_name)
        st.success(f"Wysłano: **{product_name}** do Mikołaja 🎅 (Usunięto)")
    else:
        st.error(f"Nie ma takiego produktu: **{product_name}**.")

## --- INTERFEJS UŻYTKOWNIKA (FRONTEND) ---

st.title("🎅 Magazyn Świętego Mikołaja 🎄")
st.markdown("Zarządzaj listą prezentów i narzędzi w świątecznym nastroju.")

# --- Sekcja Dodawania Produktu ---
st.header("🎁 Dodaj do Worka")
new_product_name = st.text_input("Nazwa rzeczy do dodania:", key="add_input")

if st.button("Dodaj Prezent"):
    add_product(new_product_name)

st.divider()

# --- Sekcja Usuwania Produktu ---
st.header("❄️ Usuń z Magazynu")

if st.session_state['inventory']:
    product_to_remove = st.selectbox(
        "Wybierz rzecz do usunięcia:",
        st.session_state['inventory'],
        index=None,
        placeholder="Wybierz z listy...",
        key="remove_select"
    )
    if st.button("Usuń Prezent"):
        if product_to_remove:
            remove_product(product_to_remove)
        else:
            st.warning("Najpierw wybierz coś z listy.")
else:
    st.info("Worek jest pusty! Elfy mają przerwę. 🥛🍪")

st.divider()

# --- Sekcja Podglądu Magazynu ---
st.header("📋 Lista Obecności")
if st.session_state['inventory']:
    st.dataframe(
        st.session_state['inventory'],
        column_config={"value": "Nazwa Przedmiotu"},
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Magazyn świeci pustkami.")

st.caption(f"Liczba rzeczy w magazynie: **{len(st.session_state['inventory'])}**")
