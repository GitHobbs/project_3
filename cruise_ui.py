#imports
import streamlit as st
import pandas as pd

# tabs
from create_sailing import create_sailing_tab
from create_cabin import create_cabin_tab

# sailing table
from tables import all_sailings_table, all_cabins_table

# contract
from functions import load_contract


contract = load_contract()

# pinata import
#from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json


################################################################################
# Streamlit UI
################################################################################

# Cruise Sailing Inventory Management Feature
st.title("Cruise Line Dashboard")
st.write("Choose an account to get started")
st.markdown("---")

################################################################################
# Create Sailing and Cabins Tabs
################################################################################
tab1, tab2 = st.tabs(["Sailings", "Cabins"])

################################################################################
# Supplier Dashboard -- Create Sailings
################################################################################
with tab1:
    create_sailing_tab()
    sailing_table = all_sailings_table()
    if isinstance(sailing_table, pd.DataFrame):
        st.dataframe(sailing_table)
    else:
        st.write("No sailings found")


############################################################################
# Supplier Dashboard -- Create Cabins
############################################################################
with tab2:
    create_cabin_tab()

