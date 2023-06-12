import os
import json
from web3 import Web3
from dotenv import load_dotenv
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
import streamlit as st
import pandas as pd
from tables import all_cabins_table
from functions import load_contract
contract = load_contract()
#################################################################
# Load Contract and Web3
#################################################################

# Load .env enviroment variables into the notebook
load_dotenv()

# Define and connect a Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

accounts = w3.eth.accounts
address = st.selectbox(
    "Select Account", options=accounts, key="address_select")


################################################################################
# View Available Sailings
################################################################################

st.header("Available Cruise Sailings")
result = contract.functions.getAllSailings().call()
df_sailings = pd.DataFrame(result, columns=['Sailing ID', 'Cruise Line', 'Cruise Name', 'Ship Name', 'Departure Date',
                           'Departure Port', 'Number of Nights', 'Destination1', 'Destination2', 'Destination3', 'Price(ETH)'])
st.table(df_sailings)

################################################################################
# View Available Cabins on Each Sailing
################################################################################

st.header("View Available Cabins")
selected_sailing_id = st.selectbox(
    "Select a Sailing to View Available Cabins", options=df_sailings['Sailing ID'].values)

# Convert numpy integer to Python integer
selected_cabin_id = int(selected_sailing_id)
sailing_cabins = None

if (selected_cabin_id):
    sailing_cabins = all_cabins_table(selected_cabin_id)
    st.dataframe(sailing_cabins)

    ################################################################################
    # Choose a Cruise to Purchase (Mint)
    ################################################################################
    selected_cabin_id = st.selectbox(
        "Select a Cabin to Purchase", options=sailing_cabins.index.tolist()
    )  # The cabin ID is the same as the sailing ID

    selected_cabin_id = int(selected_cabin_id)
    value = int(sailing_cabins.iloc[selected_cabin_id]["Price(ETH)"])

    amount = st.number_input("Enter the amount to purchase", min_value=1)
    if st.button('Purchase'):
        st.success("Purchase Successful")
        tx_hash = contract.functions.mintCabin(selected_cabin_id, amount).transact(
            {'from': address, 'gas': 500000, 'value': value * amount})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
            

# ################################################################################
# # View Cabin Ownership and Token Balances
# ################################################################################

# st.header("My Cabins")
# my_cabins = contract.functions.balanceOfCabin(
#     address, selected_cabin_id).call()
# df_my_cabins = pd.DataFrame(
#     [{"Token ID": selected_cabin_id, "Balance": my_cabins}])
# st.table(df_my_cabins)

# ################################################################################
# # Transfer a Cabin to Another Address
# ################################################################################

# st.header("Transfer a Cabin")
# recipient = st.text_input("Recipient Address")
# selected_cabin_to_transfer = st.selectbox(
#     "Select a Cabin to Transfer", options=[selected_cabin_id])
# if st.button('Transfer'):
#     tx_hash = contract.functions.transferCabin(
#         recipient, selected_cabin_id, 1).transact(
#         {'from': address, 'gas': 500000})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write(receipt)
