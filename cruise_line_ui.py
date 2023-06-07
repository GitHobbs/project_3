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


def load_contract():
    # Load the contract ABI
    with open(Path('./contracts/compiled/CruiseLine_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    print("contract_address")
    print(contract_address)
    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Supplier Dashboard -- Create Sailings
################################################################################

# Cruise Sailing Inventory Management Feature
st.title("Cruise Line Dashboard")
st.write("Choose an account to get started")

# Demo contract functions
result = contract.functions.getSailing(2).call()
st.write(result)

accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

st.markdown("---")
st.header("Create a Sailing")

# State for new data
new_data = {}


def get_dataframe():
    return pd.DataFrame()

##############################
# Functions
##############################


def add_sailing(new_data):

    departure_date = datetime.datetime(
        new_data['departureDate'].year, new_data['departureDate'].month, new_data['departureDate'].day)
    departure_timestamp = int(departure_date.timestamp())
    
    # Call the createSailing function from the contract
    contract.functions.createSailing(
        departure_timestamp,
        new_data['numberOfNights'],
        new_data['shipName']
    ).transact({'from': address, 'gas': 500000})


def create_cabin(new_cabin_data):
    tx_hash = contract.functions.createCabin(
        int(new_cabin_data['price']),
        new_cabin_data['initialAvailability'],
        new_cabin_data['cabinType'],
        new_cabin_data['sailingId']
        ).transact(
        {'from': address, 'gas': 500000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)


# Initial data as an empty DataFrame
initial_data = pd.DataFrame()

tab1, tab2 = st.tabs(["Cruise", "Cabins"])

with tab1:

    # columns with in tab 1
    col1, col2 = st.columns(2)

    with col1:
        # Input fields
        new_data['cruiseLine'] = st.text_input("Cruise Line")
        new_data['cruiseName'] = st.text_input("Cruise Name")
        new_data['shipName'] = st.text_input("Ship Name")
        new_data['departurePort'] = st.text_input("Departure Port")
        new_data['departureDate'] = st.date_input("Departure Date")
        new_data['numberOfNights'] = st.number_input(
            "Number of Nights", min_value=1)
        new_data['priceETH'] = st.number_input("Price(ETH)")
        for i in range(1, 5):
            new_data[f'destination{i}'] = st.text_input(f"Destination {i}")

    with col2:

        # Use the padded class for the component
        st.write("Upload Cruise Image")
        st.button("Upload Image")
        st.image("assets/cruise.jpg")

    if st.button('Add Sailing'):
        new_data['sailingId'] = add_sailing(new_data)
        st.write(new_data)
    # initial_data = initial_data.append(new_data, ignore_index=True)

    result = contract.functions.getAllSailings().call()
    del result[0]
    df = pd.DataFrame(result, columns=['ID', 'Date', 'Nights', 'Cruise'])
    df.set_index('ID', inplace=True)
    st.table(df)

    sailings_list = df.drop(columns=['Date', 'Nights'])

################################################################################
# Supplier Dashboard -- Create Cabins
################################################################################

st.markdown("---")
st.header("Create a Cabin")

# State for new cabin data
new_cabin_data = {}

@st.cache(allow_output_mutation=True)
def get_cabin_dataframe():
    return pd.DataFrame()

# Initial cabin data as an empty DataFrame
initial_cabin_data = get_cabin_dataframe()

# Input fields
new_cabin_data['sailingId'] = st.selectbox("Select Sailing ID", options=initial_data['sailingId'].unique())
cabin_types = ['Interior', 'Outside View', 'Balcony', 'Suite']
new_cabin_data['cabinType'] = st.selectbox("Cabin Type", options=cabin_types)
new_cabin_data['price'] = st.number_input("Price(ETH)", key='price_input')
new_cabin_data['initialAvailability'] = st.number_input("Initial Availability", min_value=1, key='initial_availability_input')

# new_cabin_data['availability'] will equal initialAvailability for now
new_cabin_data['availability'] = new_cabin_data['initialAvailability']

if st.button('Create Cabin'):
    new_cabin_data['tokenId'] = create_cabin(new_cabin_data)
    initial_cabin_data = initial_cabin_data.append(new_cabin_data, ignore_index=True)

# Display the cabin data
st.dataframe(initial_cabin_data)




with tab2:
    ############################################################################
    # Supplier Dashboard -- Create Cabins
    ################################################################################
    st.markdown("---")
    st.header("Create a Cabin")
    # State for new cabin data
    new_cabin_data = {}

    col1, col2 = st.columns(2)

    with col1:
        selected_sail = st.selectbox(
            "Select a Cruise", options=sailings_list['Cruise'])

        cabin_types = ['Interior', 'Outside View', 'Balcony', 'Suite']

        # st.selectbox("Select a Sailing", options=cabin_types)

        # price = st.number_input("Price(ETH)", key='price_input')

        # initial_availability = st.number_input("Initial Availibility", min_value=1, key='initial_availability_input')
        new_cabin_data['price'] = st.number_input(
            "Price(ETH)", key='price_input')
        new_cabin_data['initialAvailability'] = st.number_input(
            "Initial Availability", min_value=1, key='initial_availability_input')
        new_cabin_data['cabinType'] = st.selectbox(
            "Cabin Type", options=cabin_types)
        # new_cabin_data['availability'] = new_cabin_data['initialAvailability']
        new_cabin_data['sailingId'] = int(sailings_list[sailings_list['Cruise']
                                        == selected_sail].index[0])
   


if st.button('Create Cabin'):
    new_cabin_data['tokenId'] = create_cabin(new_cabin_data)
    st.write(new_cabin_data)
    