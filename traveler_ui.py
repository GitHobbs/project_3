import os
import json
from web3 import Web3
from dotenv import load_dotenv
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
import streamlit as st
import pandas as pd

load_dotenv()

# Define and connect a Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Load contract function from your cruise line file
from cruise_line import load_contract
contract = load_contract()

accounts = w3.eth.accounts

st.title("Cruise Line Booking")
st.write("Choose an account to get started")

address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# View Available Sailings
################################################################################

st.header("Available Cruise Sailings")
result = contract.functions.getAllSailings().call()
df_sailings = pd.DataFrame(result, columns=['Sailing ID', 'Departure Date', 'Number Of Nights', 'Ship Name'])
st.table(df_sailings)

################################################################################
# View Available Cabins on Each Sailing
################################################################################

st.header("Available Cabins on Each Sailing")
selected_sailing_id = st.selectbox(
    "Select a Sailing to View Available Cabins", options=df_sailings['Sailing ID'].values)
sailing = contract.functions.getSailing(selected_sailing_id).call()
cabin = contract.functions.getCabin(selected_sailing_id).call()
cabin["Sailing"] = sailing
df_cabins = pd.DataFrame([cabin], columns=['Cabin Type', 'Price', 'Availability', 'Sailing'])
st.table(df_cabins)

################################################################################
# Choose a Cruise to Purchase (Mint)
################################################################################

st.header("Purchase a Cabin")
selected_cabin_id = st.selectbox(
    "Select a Cabin to Purchase", options=[selected_sailing_id])  # The cabin ID is the same as the sailing ID
amount = st.number_input("Enter the amount to purchase", min_value=1)
if st.button('Purchase'):
    tx_hash = contract.functions.mintCabin(selected_cabin_id, amount).transact(
        {'from': address, 'gas': 500000, 'value': cabin['Price'] * amount})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)

################################################################################
# View Cabin Ownership and Token Balances
################################################################################

st.header("My Cabins")
my_cabins = contract.functions.balanceOfCabin(address, selected_cabin_id).call()
df_my_cabins = pd.DataFrame([{"Token ID": selected_cabin_id, "Balance": my_cabins}])
st.table(df_my_cabins)

################################################################################
# Transfer a Cabin to Another Address
################################################################################

st.header("Transfer a Cabin")
recipient = st.text_input("Recipient Address")
selected_cabin_to_transfer = st.selectbox(
    "Select a Cabin to Transfer", options=[selected_cabin_id])
if st.button('Transfer'):
    tx_hash = contract.functions.transferCabin(
        recipient, selected_cabin_id, 1).transact(
        {'from': address, 'gas': 500000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
