import streamlit as st
from functions import create_cabin
from tables import all_sailings_table, all_cabins_table
import pandas as pd
from streamlit_card import card

custom_label = '<p style="color:blue;">This is a blue paragraph.</p>'
st.markdown(custom_label, unsafe_allow_html=True)

def create_cabin_tab():
    # Get all sailings
    sailings_list = all_sailings_table()

    if isinstance(sailings_list, pd.DataFrame) and not sailings_list.empty:
        st.markdown("---")
        st.header("Create a Cabin")

        # State for new cabin data
        new_cabin_data = {}

        col1, col2 = st.columns(2)

        with col1:
            selected_sail = st.selectbox(
                "Select a Cruise", options=sailings_list['Cruise Name'], key='select_sail_input')

            cabin_types = ['Interior', 'Outside View', 'Balcony', 'Suite']

            new_cabin_data['price'] = st.number_input(
                "Price(ETH)", key='price_input')
            new_cabin_data['initialAvailability'] = st.number_input(
                "Initial Availability", min_value=1, key='initial_availability_input')
            new_cabin_data['cabinType'] = st.selectbox(
                "Cabin Type", options=cabin_types)

            filtered_sailings = sailings_list[sailings_list['Cruise Name'] == selected_sail]
            if not filtered_sailings.empty:
                new_cabin_data['sailingId'] = int(filtered_sailings.index[0])
            else:
                st.error("No sailings match the selected cruise name.")

            # add conditional to check if all fields are filled
            if new_cabin_data['price'] != 0 and new_cabin_data['initialAvailability'] != 0 and new_cabin_data['cabinType'] != None  and new_cabin_data['sailingId'] != None:
                if st.button('Create Cabin', key='create_cabin_button'):
                    create_cabin(new_cabin_data)
                    st.success("Cabin created successfully!")
            else:   
                st.warning("Please fill in all fields.")

        with col2:
            st.write("Upload Cabin Image")
            st.button("Upload Image", key='upload_image_button')
            st.image("assets/cabin.jpg")

        if( new_cabin_data['sailingId'] and selected_sail):
          cabin_table =  all_cabins_table(new_cabin_data['sailingId'] )
          st.dataframe(cabin_table)
        else:
            st.write("No cabins found")
        
        
    else:
        st.write("No sailings found")

