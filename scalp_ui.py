import streamlit as st

st.title("Options Scalping Calculator")

MAX_RISK = 50

ticker = st.text_input("Ticker")

col1, col2 = st.columns(2)

with col1:
    stock_price = st.number_input("Current Stock Price")
    entry_level = st.number_input("Entry Level")
    invalidation_level = st.number_input("Stock Invalidation Level")

with col2:
    bid = st.number_input("Option Bid")
    ask = st.number_input("Option Ask")
    delta = st.number_input("Option Delta", value=0.60)

if st.button("Calculate Trade"):

    mid = (bid + ask) / 2

    # ENTRY
    stock_move_entry = entry_level - stock_price
    option_move_entry = stock_move_entry * delta
    entry_price = mid + option_move_entry

    # STOP LOSS (stock invalidation)
    stock_move_stop = invalidation_level - entry_level
    option_move_stop = stock_move_stop * delta
    stop_price = entry_price + option_move_stop

    # RISK
    risk_per_share = abs(entry_price - stop_price)

    # TAKE PROFIT (1:2 RR)
    take_profit = entry_price + (risk_per_share * 2)

    # Dollar values
    risk_dollars = risk_per_share * 100
    reward_dollars = (take_profit - entry_price) * 100

    contracts = int(MAX_RISK // risk_dollars) if risk_dollars > 0 else 0

    # Convert TP back to stock
    option_move_tp = take_profit - entry_price
    stock_move_tp = option_move_tp / delta if delta != 0 else 0
    stock_tp_price = entry_level + stock_move_tp

    st.subheader("Entry Price")
    st.write(round(entry_price,2))
    st.write("Stock at entry ≈", entry_level)

    st.subheader("Stop Loss")
    st.write(round(stop_price,2))
    st.write("Stock invalidation =", invalidation_level)

    st.subheader("Take Profit")
    st.write(round(take_profit,2))
    st.write("Stock TP ≈", round(stock_tp_price,2))

    st.subheader("Risk per Contract")
    st.write("$", round(risk_dollars,2))

    st.subheader("Reward")
    st.write("$", round(reward_dollars,2))

    st.subheader("Contracts Allowed (Max $50 Risk)")
    st.write(contracts)
