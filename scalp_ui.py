import streamlit as st

st.title("Options Scalping Calculator")

MAX_RISK = 50

ticker = st.text_input("Ticker")

col1, col2 = st.columns(2)

with col1:
    stock_price = st.number_input("Current Stock Price")
    level = st.number_input("Support / Resistance Level")

with col2:
    bid = st.number_input("Option Bid")
    ask = st.number_input("Option Ask")
    delta = st.number_input("Option Delta", value=0.60)

if st.button("Calculate Trade"):

    mid = (bid + ask) / 2
    spread = ask - bid

    stock_move = level - stock_price
    option_move = stock_move * delta

    entry_price = mid + option_move

    entry1 = round(entry_price + 0.01,2)
    entry2 = round(entry_price + 0.03,2)
    entry3 = round(entry_price + 0.05,2)

    stop_loss = entry_price * 0.83
    risk_per_share = abs(entry_price - stop_loss)

    take_profit = entry_price + (risk_per_share * 2)

    risk_dollars = risk_per_share * 100
    reward_dollars = (take_profit - entry_price) * 100

    contracts = int(MAX_RISK // risk_dollars) if risk_dollars > 0 else 0

    st.subheader("Entry Estimate")
    st.write(round(entry_price,2))

    st.subheader("Entry Ladder")
    st.write(entry1, entry2, entry3)

    st.subheader("Stop Loss")
    st.write(round(stop_loss,2))

    st.subheader("Take Profit (1:2 RR)")
    st.write(round(take_profit,2))

    st.subheader("Risk Per Contract")
    st.write("$", round(risk_dollars,2))

    st.subheader("Reward")
    st.write("$", round(reward_dollars,2))

    st.subheader("Contracts Allowed (Max $50 Risk)")
    st.write(contracts)
