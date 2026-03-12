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

    # stock movement to level
    stock_move = level - stock_price

    # option move estimate
    option_move = stock_move * delta

    # entry estimate
    entry_price = mid + option_move

    # stop loss
    stop_loss = entry_price * 0.83
    risk_per_share = abs(entry_price - stop_loss)

    # take profit
    take_profit = entry_price + (risk_per_share * 2)

    # dollar values
    risk_dollars = risk_per_share * 100
    reward_dollars = (take_profit - entry_price) * 100

    contracts = int(MAX_RISK // risk_dollars) if risk_dollars > 0 else 0

    # ----------------------------------
    # Convert option prices back to stock
    # ----------------------------------

    option_move_stop = stop_loss - entry_price
    option_move_tp = take_profit - entry_price

    stock_move_stop = option_move_stop / delta if delta != 0 else 0
    stock_move_tp = option_move_tp / delta if delta != 0 else 0

    stock_at_entry = level
    stock_at_stop = stock_at_entry + stock_move_stop
    stock_at_tp = stock_at_entry + stock_move_tp

    # ------------------------
    # DISPLAY
    # ------------------------

    st.subheader("Entry Estimate")
    st.write(round(entry_price,2))
    st.write("Stock price at entry ≈", round(stock_at_entry,2))

    st.subheader("Stop Loss")
    st.write(round(stop_loss,2))
    st.write("Stock price at stop ≈", round(stock_at_stop,2))

    st.subheader("Take Profit")
    st.write(round(take_profit,2))
    st.write("Stock price at TP ≈", round(stock_at_tp,2))

    st.subheader("Risk per Contract")
    st.write("$", round(risk_dollars,2))

    st.subheader("Reward")
    st.write("$", round(reward_dollars,2))

    st.subheader("Contracts Allowed (Max $50 Risk)")
    st.write(contracts)
