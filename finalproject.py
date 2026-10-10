import streamlit as st
import random
import time
import pandas as pd
import os


def get_secret_key():
    key = os.getenv()

st.set_page_config(page_title="Casino App", page_icon="🎰", layout="wide")

if "balance" not in st.session_state:
    st.session_state.balance = 1000

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎰 Streamlit Online Casino")

st.sidebar.metric("💰 Balance", f"${st.session_state.balance}")

if st.sidebar.button("Deposit +$500"):
    st.session_state.balance += 500
    st.rerun()

if st.session_state.balance <= 0:
    if st.sidebar.button("Claim Relief Bonus ($100)"):
        st.session_state.balance = 100
        st.rerun()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎡 Wheel Spinner", "🎰 Slots", "🪙 Coin Flip", "🎲 Dice", "📜 History"])

with tab1:
    st.header("Lucky Wheel Spinner")
    bet_wheel = st.number_input("Bet ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b_wheel")
    
    sectors = [
        {"label": "💥 LOSE (0x)", "multiplier": 0},
        {"label": "🥉 1.5x Multiplier", "multiplier": 1.5},
        {"label": "💥 LOSE (0x)", "multiplier": 0},
        {"label": "🥈 2x Multiplier", "multiplier": 2},
        {"label": "💥 LOSE (0x)", "multiplier": 0},
        {"label": "🥇 3x Multiplier", "multiplier": 3},
        {"label": "💎 5x JACKPOT", "multiplier": 5}
    ]
    
    wheel_placeholder = st.empty()
    wheel_placeholder.markdown("### 🎡 Spin the wheel to test your luck!")
    
    if st.button("Spin the Wheel!"):
        if bet_wheel > st.session_state.balance:
            st.error("Insufficient funds!")
        else:
            st.session_state.balance -= bet_wheel
            
            with st.spinner("Spinning the wheel... 🌀"):
                for _ in range(12):
                    temp_sector = random.choice(sectors)
                    wheel_placeholder.markdown(f"## 🎡 [ {temp_sector['label']} ]")
                    time.sleep(0.15)
            
            final_sector = random.choice(sectors)
            wheel_placeholder.markdown(f"# 🎡 Result: {final_sector['label']}")
            
            mult = final_sector["multiplier"]
            if mult > 0:
                win = int(bet_wheel * mult)
                st.session_state.balance += win
                st.success(f"🎉 You won ${win}! ({mult}x payout)")
                st.session_state.history.insert(0, {"Game": "Spinner", "Bet": bet_wheel, "Result": f"Win ({final_sector['label']})", "Payout": f"+${win}"})
            else:
                st.error("❌ You Lost! Better luck next time.")
                st.session_state.history.insert(0, {"Game": "Spinner", "Bet": bet_wheel, "Result": "Loss", "Payout": f"-${bet_wheel}"})

with tab2:
    st.header("Slot Machine")
    bet1 = st.number_input("Bet ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b1")
    
    if st.button("Spin Slots!"):
        if bet1 > st.session_state.balance:
            st.error("Insufficient funds!")
        else:
            st.session_state.balance -= bet1
            symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]
            res = [random.choice(symbols) for _ in range(3)]
            
            st.markdown(f"## {res[0]} | {res[1]} | {res[2]}")
            
            if res[0] == res[1] == res[2]:
                win = bet1 * 10
                st.session_state.balance += win
                st.success(f"🎉 Jackpot! Win: ${win}")
                st.session_state.history.insert(0, {"Game": "Slots", "Bet": bet1, "Result": "Win (Jackpot)", "Payout": f"+${win}"})
            elif res[0] == res[1] or res[1] == res[2] or res[0] == res[2]:
                win = int(bet1 * 1.5)
                st.session_state.balance += win
                st.info(f"✨ Pair Match! Win: ${win}")
                st.session_state.history.insert(0, {"Game": "Slots", "Bet": bet1, "Result": "Win (Pair)", "Payout": f"+${win}"})
            else:
                st.error("❌ You Lost")
                st.session_state.history.insert(0, {"Game": "Slots", "Bet": bet1, "Result": "Loss", "Payout": f"-${bet1}"})

with tab3:
    st.header("Coin Flip")
    bet2 = st.number_input("Bet ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b2")
    choice = st.radio("Your Choice:", ["Heads", "Tails"])
    
    if st.button("Flip Coin"):
        if bet2 > st.session_state.balance:
            st.error("Insufficient funds!")
        else:
            st.session_state.balance -= bet2
            result = random.choice(["Heads", "Tails"])
            
            st.write(f"Result: **{result}**")
            
            if choice == result:
                win = bet2 * 2
                st.session_state.balance += win
                st.success(f"🎉 Winner! Win: ${win}")
                st.session_state.history.insert(0, {"Game": "Coin Flip", "Bet": bet2, "Result": f"Win ({result})", "Payout": f"+${win}"})
            else:
                st.error("❌ You Lost")
                st.session_state.history.insert(0, {"Game": "Coin Flip", "Bet": bet2, "Result": f"Loss ({result})", "Payout": f"-${bet2}"})

with tab4:
    st.header("Dice Roll")
    bet3 = st.number_input("Bet ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b3")
    target_sum = st.slider("Predict the total sum of two dice:", 2, 12, 7)
    
    if st.button("Roll Dice"):
        if bet3 > st.session_state.balance:
            st.error("Insufficient funds!")
        else:
            st.session_state.balance -= bet3
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            total = d1 + d2
            
            st.markdown(f"### Dice: 🎲 {d1} and 🎲 {d2} (Total: {total})")
            
            if total == target_sum:
                win = bet3 * 6
                st.session_state.balance += win
                st.success(f"🎉 Perfect Match! Win: ${win}")
                st.session_state.history.insert(0, {"Game": "Dice", "Bet": bet3, "Result": f"Win (Sum {total})", "Payout": f"+${win}"})
            else:
                st.error("❌ You Lost")
                st.session_state.history.insert(0, {"Game": "Dice", "Bet": bet3, "Result": f"Loss (Sum {total})", "Payout": f"-${bet3}"})

with tab5:
    st.header("Game History")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No games played yet. Start playing to see your history!")