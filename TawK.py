import base64
import streamlit as st

st.sidebar.image("TawK logo.png", use_container_width=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert image
img_base64 = get_base64_image("TawK_logo_drop.png")

# Display using HTML
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{img_base64}" width="280">
    </div>
    """,
    unsafe_allow_html=True
)
st.title("TawK")
st.write("Inventory Management System")
st.write("TawK is a streamlined inventory management system designed to simplify stock tracking, product transactions, and category management. Built with an intuitive interface, TawK allows users to efficiently monitor inventory levels, record transactions, and manage product details in real time. Whether for small businesses or larger operations, TawK ensures accurate inventory control, reducing errors and improving operational efficiency.")
