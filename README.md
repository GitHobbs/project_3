#aWei

# project_3
aWei is a protocol built on the blockchain that allows cruise lines and hotels to tokenize and distribute cabin and room night inventory in a decentralized way.

## Summary

aWei is a web3 platform that allows cruise lines to transparently manage, price, and sell inventory on the Ethereum blockchain.  It provides cruise lines with a UI and dashboard that allows them to add mintable inventory to the platform, track and fulfill bookings, and adjust pricing.  It also provides them with a customer UI that allows travelers to browse inventory and mint cabin reservations as NFTs directly from the cruise line.

## Supplier Interface

- allow cruiseline to input inventory information including:
  - departure date
  - return date
  - destinations visited
  - cabin type
  - price (ETH)
  - port of origin
  - cruise line
  - total available inventory
- create ERC 1155 mintable contract where travelers can mint cruise cabin NFTs

## Customer Interface

- show cruise and cabin offerings
- browse inventory
- make bookings
- mint NFT representing customer reservation (AI generated image?) upon purchase

## Functionality

- use solidity NFT contracts to tokenize cruise cabin inventory
- pin metadata and images to IPFS

## Steps

1.  Build smart contracts
2.  Create .py/.env files for UI's
3.  Create .py file for Pinata
4.  Design supplier interface and dashboard using Streamlit
5.  Design customer interface using Streamlit
6.  Test contract and UI functionality using Ganache

## Benefits to cruise line to tokenize cabin inventory

1.  Increase direct-to-consumer bookings (increases margins by decreasing commissions paid and third party mark ups)
2.  Reduce reliance on online travel operators and other middlemen (inventory management is under direct control of the cruise line)
3.  Cut out significant accounts payable and inventory tracking bloat (everything tracked on chain)
4.  Funds are escrowed on chain and cruise lines are not subject to payment deliquincies and OTA bankruptcies (trustless)
5.  Provides cruise lines with access to the web3 market (reduce advertising expense)
6.  Capture royalties on the resale of cabins on the secondary market
7.  Increased inventory transparency
8.  Gives cruise lines complete control over pricing and eliminates rate parity agreements with OTA's
9.  Receive token rewards for using the platform
10. Market to past customers more easily by issuing rewards for used NFT holders (on chain rewards program)

## Benefits to the consumer

1.  The ability to transfer and sell cabin inventory via a marketplace (no longer subject to cancellation and change policies)
2.  Reduce costs due to supplier cost savings that can be passed to the end user
3.  Status - show off your travel reservations to other members of the community (keepsake NFT)
4.  Keep reservations in a web3 wallet as opposed to carrying physcial documents
5.  Receive token rewards for using the platform (can be used for upgrades, excursions, etc)
