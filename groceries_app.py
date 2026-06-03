import streamlit as st
import pandas as pd
from email_service import send_mail
from groceries_helper import save_cart




st.title("🛒 Make your grocery list")

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------

if "carts" not in st.session_state:
    st.session_state.carts = {}

if "selected_shop" not in st.session_state:
    st.session_state.selected_shop = "Νέο Κατάστημα"

# προσωρινό καλάθι μέχρι να αποθηκευτεί νέο κατάστημα
if "temp_cart" not in st.session_state:
    st.session_state.temp_cart = pd.DataFrame(
        columns=["products", "quantity"]
    )
    
if 'send' not in st.session_state:
    st.session_state.send = False

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.title("🛒 Supermarkets")

    # Δεν επιτρέπουμε να υπάρχει το "Νέο Κατάστημα"
    # μέσα στα πραγματικά shops
    shops = [
        shop for shop in st.session_state.carts.keys()
        if shop != "Νέο Κατάστημα"
    ]

    # Προσθέτουμε χειροκίνητα την επιλογή
    options = shops + ["Νέο Κατάστημα"]

    # ασφαλές index
    if st.session_state.selected_shop in options:
        index = options.index(st.session_state.selected_shop)
    else:
        index = 0

    selected = st.radio(
        "Επέλεξε κατάστημα",
        options,
        index=index
    )

    st.session_state.selected_shop = selected

# -------------------------------------------------
# ΕΠΙΛΟΓΗ ΚΑΤΑΣΤΗΜΑΤΟΣ
# -------------------------------------------------

if st.session_state.selected_shop == "Νέο Κατάστημα":

    new_shop = st.text_input(
        "Γράψε το όνομα του καταστήματος:"
    )

    current_df = st.session_state.temp_cart

else:

    new_shop = st.session_state.selected_shop

    current_df = st.session_state.carts[new_shop]

# -------------------------------------------------
# ΠΡΟΣΘΗΚΗ ΠΡΟΪΟΝΤΩΝ
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    product = st.text_input("Ποιο προϊόν θέλεις;")

with col2:
    quantity = st.text_input("Πόση ποσότητα θέλεις;")

# -------------------------------------------------
# BUTTON ΠΡΟΣΘΗΚΗΣ
# -------------------------------------------------

if st.button("➕ Προσθήκη στη λίστα"):

    if product and quantity:

        new_row = pd.DataFrame([
            {
                "products": product,
                "quantity": quantity
            }
        ])

        current_df = pd.concat(
            [current_df, new_row],
            ignore_index=True
        )

        # Αν είναι νέο κατάστημα
        if st.session_state.selected_shop == "Νέο Κατάστημα":

            st.session_state.temp_cart = current_df

        # Αν είναι υπάρχον
        else:

            st.session_state.carts[new_shop] = current_df

        st.success("Προστέθηκε!")
        st.rerun()

# -------------------------------------------------
# ΕΜΦΑΝΙΣΗ LISTAS
# -------------------------------------------------

st.write("### 🛒 Η λίστα σου:")

st.dataframe(current_df)

# -------------------------------------------------
# DELETE BUTTONS
# -------------------------------------------------

for i, row in current_df.iterrows():

    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        st.write(row["products"])

    with col2:
        st.write(row["quantity"])

    with col3:

        if st.button("❌", key=f"delete_{i}"):

            current_df = (
                current_df
                .drop(i)
                .reset_index(drop=True)
            )

            if st.session_state.selected_shop == "Νέο Κατάστημα":

                st.session_state.temp_cart = current_df

            else:

                st.session_state.carts[new_shop] = current_df

            st.rerun()

# -------------------------------------------------
# ΟΛΟΚΛΗΡΩΣΗ ΚΑΛΑΘΙΟΥ
# -------------------------------------------------

if st.button("Ολοκλήρωση Καλαθιού"):

    # μόνο αν είναι νέο κατάστημα
    if st.session_state.selected_shop == "Νέο Κατάστημα":

        # validations
        if not new_shop:
            st.warning("Γράψε όνομα καταστήματος")

        elif new_shop == "Νέο Κατάστημα":
            st.warning("Διάλεξε διαφορετικό όνομα")

        else:

            # αποθήκευση cart
            st.session_state.carts[new_shop] = (
                st.session_state.temp_cart.copy()
            )

            # το κάνουμε selected
            st.session_state.selected_shop = new_shop

            # reset temp cart
            st.session_state.temp_cart = pd.DataFrame(
                columns=["products", "quantity"]
            )

            st.success(
                f"Το κατάστημα '{new_shop}' αποθηκεύτηκε!"
            )
            save_cart(
                        new_shop,
                        current_df
                    )
            st.rerun()

    else:

        st.success("Το καλάθι ενημερώθηκε!")
        
# ------------------------
# SEND EMAIL
# ------------------------
if st.button("Send"):
    st.session_state.send = True

if st.session_state.send:
    reciever = st.text_input("Email")

    if st.button("📧 Αποστολή email"):
        if reciever:

            send_mail(
                reciever,
                st.session_state.carts
            )

            st.success("Το email στάλθηκε.")

            st.session_state.clear()
            st.rerun()
        else:
            st.warning("Βάλε email πρώτα!")

# Upgrades of the App:
# 1. Data sent to PostgreSql
# 2. Create functions
# 3. A button that user can insert the dates they want PostgreSQL takes the list of product of thhat period and assess  
#    if they are nutritious and propose the user with what they could improve or change