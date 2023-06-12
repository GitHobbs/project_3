import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import json
from web3 import Web3


#################################################################
# Load Contract and Web3
#################################################################

# Load .env enviroment variables into the notebook
load_dotenv()

# Define and connect a Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)

# Load_Contract Function

# Load contract function from your cruise line file
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


###################################################################
# Functions
###################################################################

def add_sailing(new_data):

    # convert date to timestamp
    departure_date = datetime.datetime(
        new_data['departureDate'].year, new_data['departureDate'].month, new_data['departureDate'].day)
    departure_timestamp = int(departure_date.timestamp())

    # Call the createSailing function from the contract
    contract.functions.createSailing(
        new_data['cruiseLine'],
        new_data['cruiseName'],
        new_data['shipName'],
        departure_timestamp,
        new_data['departurePort'],
        new_data['numberOfNights'],
        new_data['price'],
        new_data['destination1'],
        new_data['destination2'],
        new_data['destination3'],
    ).transact({'from': address, 'gas': 500000})


def create_cabin(new_cabin_data):

    contract.functions.createCabin(
        int(new_cabin_data['price']),
        new_cabin_data['initialAvailability'],
        new_cabin_data['cabinType'],
        new_cabin_data['sailingId']
    ).transact(
        {'from': address, 'gas': 500000})
    #receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #st.write(receipt)


def replace_sailing_id_with_cruise_name(cabins_df, sailings_df):
    # Create a mapping from sailing_id to cruise_name
    mapping = sailings_df['Cruise Name']

    # Replace the 'Sailing ID' values in cabins_df with the 'Cruise Name' from the mapping
    cabins_df['Sailing'] = cabins_df['Sailing ID'].map(mapping)
    
    return cabins_df


def get_value_from_key(key, dataframe, column_name):
    if key in dataframe.index:
        return dataframe.loc[key, column_name]
    else:
        return None