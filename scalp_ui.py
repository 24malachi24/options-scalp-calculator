import streamlit as st

st.title("Options Scalping Calculator")

MAX_RISK = 50

ticker = st.text_input("Ticker")

col1, col2 = st.columns(2)

with col1:
    stock_price = st.number_input("Current Stock Price")
    entry_level = st.number_input("Desired Entry Level")

with col2:
    bid = st.number_input("Option Bid")
    ask = st.number_input("Option Ask")
    delta = st.number_input("Option Delta", value=0.60)

direction = st.selectbox("Trade Type", ["Call", "Put"])

if st.button("Calculate Trade"):

    mid = (bid + ask) / 2
    spread = ask - bid

    # ENTRY MOVE
    if direction == "Call":
        stock_move_entry = entry_level - stock_price
    else:
        stock_move_entry = stock_price - entry_level

    option_move_entry = stock_move_entry * delta

    entry_price = mid + option_move_entry

    # LATENCY BUFFER
    latency_buffer = max(spread * 0.5, 0.03)

    entry_low = entry_price - latency_buffer
    entry_high = entry_price + latency_buffer

    # RISK SETTINGS
    option_loss = MAX_RISK / 100

    stop_price = entry_price - option_loss

    # STOCK INVALIDATION
    stock_move_stop = option_loss / delta

    if direction == "Call":
        stock_invalidation = entry_level - stock_move_stop
    else:
        stock_invalidation = entry_level + stock_move_stop

    # TAKE PROFIT
    take_profit = entry_price + (option_loss * 2)

    # STOCK TARGET
    option_move_tp = take_profit - entry_price
    stock_move_tp = option_move_tp / delta

    if direction == "Call":
        stock_tp = entry_level + stock_move_tp
    else:
        stock_tp = entry_level - stock_move_tp

    # DISPLAY
    st.subheader("Entry")

    st.write("Calculated Entry:", round(entry_price,2))

    st.write("Latency Range:")
    st.write(round(entry_low,2), "to", round(entry_high,2))

    st.write("Stock Entry Level:", entry_level)

    st.subheader("Stop Loss")

    st.write("Option Stop:", round(stop_price,2))
    st.write("Stock Invalidation:", round(stock_invalidation,2))

    st.subheader("Take Profit")

    st.write("Option TP:", round(take_profit,2))
    st.write("Stock TP:", round(stock_tp,2))

    st.subheader("Risk")

    st.write("Max Loss: $50 per contract")

    st.subheader("Spread")

    st.write("Spread:", round(spread,2))
