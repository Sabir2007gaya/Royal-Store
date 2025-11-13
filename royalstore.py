import streamlit as st
import pandas as pd

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = ""
    st.session_state.users = pd.DataFrame({"username": ["admin"], "password": ["admin"], "role": ["admin"]})
    st.session_state.products = pd.DataFrame(columns=["product", "price"])
    st.session_state.cart = []

def admin_page():
    st.write("Admin Panel")
    # --- Create New User ---
    st.write("Create New User")
    with st.form("create_user"):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Create User")
        if submitted:
            if uname and pwd:
                if uname in st.session_state.users["username"].values:
                    st.error("User already exists.")
                else:
                    new_user = pd.DataFrame([{"username": uname, "password": pwd, "role": "user"}])
                    st.session_state.users = pd.concat([st.session_state.users, new_user], ignore_index=True)
                    st.success(f"User '{uname}' created.")
            else:
                st.warning("All fields required.")

    # --- Add Product ---
    st.write("Add Product")
    with st.form("add_product"):
        pname = st.text_input("Product Name")
        pprice = st.number_input("Price", min_value=1.0, step=0.5)
        submitted = st.form_submit_button("Add Product")
        if submitted:
            if pname:
                new_product = pd.DataFrame([{"product": pname, "price": pprice}])
                st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
                st.success(f"Product '{pname}' added.")
            else:
                st.warning("Product name required.")

    # --- Product List ---
    st.write("Product List")
    st.table(st.session_state.products[["product", "price"]])

def user_page(username):
    st.write(f"Welcome, {username}")
    st.write("Products List")
    if st.session_state.products.empty:
        st.info("No products available.")
        return

    cart = st.session_state.cart if "cart" in st.session_state else []

    for idx, row in st.session_state.products.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{row['product']}** - ₹{row['price']:.2f}")
        with col2:
            if st.button("Add to Cart", key=f"add_{idx}"):
                cart.append((row['product'], row['price']))
    st.session_state.cart = cart

    st.write("Cart")
    if cart:
        cart_df = pd.DataFrame(cart, columns=["Product", "Price"])
        st.table(cart_df)
        if st.button("Buy", key="buy_btn"):
            st.session_state.cart = []
            st.success("Order placed successfully!")
    else:
        st.info("Your cart is empty.")

def login_page():
    st.write("Login")
    role = st.radio("Login as:", ["admin", "user"])
    login_user = st.text_input("Username", key="login_user")
    login_pwd = st.text_input("Password", type="password", key="login_pwd")
    if st.button("Login"):
        user_row = st.session_state.users[
            (st.session_state.users["username"] == login_user) &
            (st.session_state.users["password"] == login_pwd) &
            (st.session_state.users["role"] == role)
        ]
        if not user_row.empty:
            st.session_state.logged_in = True
            st.session_state.user_role = role
            st.session_state.username = login_user
            st.success(f"Logged in as {role}.")
        else:
            st.error("Invalid credentials.")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = ""
    st.session_state.cart = []

def main():
    st.title("Kinder Joy")  # App Name
    if st.session_state.logged_in:
        st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.user_role})")
        if st.sidebar.button("Logout"):
            logout()
        if st.session_state.user_role == "admin":
            admin_page()
        else:
            user_page(st.session_state.username)
    else:
        login_page()

if __name__ == "__main__":
    main()





