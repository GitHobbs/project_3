import streamlit as st
from functions import add_sailing


def create_sailing_tab():
     # columns with in tab 1
    col1, col2 = st.columns(2)

    new_data = {}

    with col1:
        # Input fields
        new_data['cruiseLine'] = st.text_input("Cruise Line")
        new_data['cruiseName'] = st.text_input("Cruise Name")
        new_data['shipName'] = st.text_input("Ship Name")
        new_data['departureDate'] = st.date_input("Departure Date")
        new_data['departurePort'] = st.text_input("Departure Port")
        new_data['numberOfNights'] = st.number_input(
            "Number of Nights", min_value=1)
        new_data['price'] = int(st.number_input("Price(ETH)"))
        for i in range(1, 4):
            new_data[f'destination{i}'] = st.text_input(f"Destination {i}")

    with col2:
        # Use the padded class for the component
        st.write("Upload Cruise Image")
        st.button("Upload Image")
        st.image("assets/cruise.jpg")

    if st.button('Add Sailing'):
        new_data['sailingId'] = add_sailing(new_data)