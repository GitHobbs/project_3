import os
import json
import pandas as pd
import datetime
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Load_Contract Function
@st.cache(allow_output_mutation=True)
def load_contract():
    # Load the contract ABI
    with open(Path('./contracts/compiled/CruiseLine_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

# Cruise Sailing Inventory Management Feature
st.title("Cruise Line Dashboard")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

# State for new data
new_data = {}

@st.cache(allow_output_mutation=True)
def get_dataframe():
    return pd.DataFrame()

# Initial data as an empty DataFrame
initial_data = get_dataframe()

# Input fields
new_data['cruiseLine'] = st.text_input("Cruise Line")
new_data['cruiseName'] = st.text_input("Cruise Name")
new_data['shipName'] = st.text_input("Ship Name")
new_data['departurePort'] = st.text_input("Departure Port")
new_data['departureDate'] = st.date_input("Departure Date")
new_data['numberOfNights'] = st.number_input("Number of Nights", min_value=1)
new_data['priceETH'] = st.number_input("Price(ETH)")
for i in range(1, 8):
    new_data[f'destination{i}'] = st.text_input(f"Destination {i}")

def add_sailing(new_data):
    
    
    departure_date = datetime.datetime(new_data['departureDate'].year, new_data['departureDate'].month, new_data['departureDate'].day)
    departure_timestamp = int(departure_date.timestamp())

    # Call the createSailing function from the contract
    tx_hash = contract.functions.createSailing(
        departure_timestamp, 
        new_data['numberOfNights'], 
        new_data['shipName']
    ).transact({'from': address})

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Parse the SailingCreated event from the logs
    event = contract.events.SailingCreated().processReceipt(tx_receipt)
    print(event)
    # Initialize new_sailingId with a default value
    new_sailingId = 1

    # Check if event is not empty
    if event:
        # Get the new sailingId from the event logs
        new_sailingId = event[0]['args']['sailingId']

    return new_sailingId

    # Add the new sailingId to new_data
    #new_data['sailingId'] = new_sailingId

    # Convert new_data to a DataFrame and append it to initial_data
    #new_data_df = pd.DataFrame([new_data])
    #initial_data = pd.concat([initial_data, new_data_df], ignore_index=True)

if st.button('Add Sailing'):
    new_data['sailingId'] = add_sailing(new_data)
    initial_data = initial_data.append(new_data, ignore_index=True)

# Display the data
st.dataframe(initial_data)


################################################################################
# List Cruises
################################################################################




