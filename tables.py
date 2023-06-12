import pandas as pd
from functions import load_contract, replace_sailing_id_with_cruise_name
import streamlit as st



contract = load_contract()


def all_sailings_table():
    result = contract.functions.getAllSailings().call()
    if result:  # Checks if result is not an empty list
        result = result[1:]  # Skip the first element
        sailing_df = pd.DataFrame(result, columns=['Sailing ID', 'Cruise Line', 'Cruise Name', 'Ship Name', 'Departure Date',
                                                   'Departure Port', 'Number of Nights', 'Price(ETH)', 'Destination 1', 'Destination 2', 'Destination 3'])
        sailing_df.set_index('Sailing ID', inplace=True)
        return sailing_df
    else:
        return "No sailings found"


def all_cabins_table(sailingId):

    result = contract.functions.getSailingCabins(sailingId).call()
    if result:  # Checks if result is not an empty list 
        result = result[1:]  # Skip the first element
    cabins_df = pd.DataFrame(result, columns=['Cabin ID', 'Price(ETH)', 'Initial Availability', 'Cabin Type', 'Sailing ID'])
    cabins_df.set_index('Cabin ID', inplace=True)
    #cabins_df = replace_sailing_id_with_cruise_name(cabins_df, sailings_df)
    cabins_df.drop(['Sailing ID'], axis=1, inplace=True)
    return cabins_df
