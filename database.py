import psycopg
import streamlit as st

def get_connection():
    
    return psycopg.connect(
        host = st.secrets["database"]["host"],
        port = st.secrets["database"]["port"], 
        dbname = st.secrets["database"]["name"],
        user = st.secrets["database"]["user"],
        password = st.secrets["database"]["password"]
    ) 
    
def save_user(google_id, email, full_name):
    with get_connection() as conn:
        
        with conn.cursor() as cur:
            cur.execute(
            """
            INSERT INTO users
            (google_id, email, full_name)

            VALUES (%s, %s, %s)

            ON CONFLICT (google_id)
            DO UPDATE SET
            email = EXCLUDED.email,
            full_name = EXCLUDED.full_name

            RETURNING id;
            """,
            (
            google_id,
            email,
            full_name
            )
            )
                    
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id

def get_user_by_google_id(google_id):

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT id
                FROM users
                WHERE google_id = %s;
                """,
                (google_id,)
            )

            result = cur.fetchone()

            if result is None:
                return None

            return result[0]

#####################
# This function checks if the user exists (then returns the user_id) else it saves the new user
########################   
def get_or_create_user(
    google_id,
    email,
    full_name
):

    user_id = get_user_by_google_id(
        google_id
    )

    if user_id is not None:

        return user_id

    return save_user(
        google_id,
        email,
        full_name
    )
    


        
def insert_order(cur, user_id):

    cur.execute(
        """
        INSERT INTO orders
        (user_id)

        VALUES (%s)

        RETURNING id;
        """,
        (user_id,)
    )

    order_id = cur.fetchone()[0]

    return order_id

def insert_grocery_item(
        cur,
        order_id,
        supermarket_name,
        product,
        quantity
):

    cur.execute(
        """
        INSERT INTO grocery_items
        (
            order_id,
            supermarket_name,
            product,
            quantity
        )

        VALUES (%s, %s, %s, %s);
        """,
        (
            order_id,
            supermarket_name,
            product,
            quantity
        )
    )
    
def save_order(user_id, carts):

    with get_connection() as conn:

        with conn.cursor() as cur:

            order_id = insert_order(
                cur,
                user_id
            )


            for supermarket, dataframe in carts.items():

                for _, row in dataframe.iterrows():

                    insert_grocery_item(
                        cur,
                        order_id,
                        supermarket,
                        row["products"],
                        row["quantity"]
                    )


            return order_id