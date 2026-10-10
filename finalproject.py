import streamlit as st
import random
import time
import pandas as pd
import os

st.set_page_config(page_title="Казино додаток", page_icon="🎰", layout="wide")

if "balance" not in st.session_state:
    st.session_state.balance = 1000

if "history" not in st.session_state:
    st.session_state.history = []

if "total_deposited" not in st.session_state:
    st.session_state.total_deposited = 0

MAX_DEPOSIT_LIMIT = 2000

st.title("🎰 Онлайн Казино Streamlit")

st.sidebar.metric("💰 Баланс", f"${st.session_state.balance}")

if st.sidebar.button("Поповнити +$500"):
    st.session_state.balance += 500
    st.rerun()

if st.session_state.balance <= 0:
    if st.sidebar.button("Отримати бонус порятунку ($100)"):
        st.session_state.balance = 100
        st.rerun()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎡 Колесо Фортуни", "🎰 Слоти", "🪙 Оркешка", "🎲 Кістки", "🎁 Кейси", "📜 Історія"])

with tab1:
    st.header("Обертання Колеса Фортуни")
    bet_wheel = st.number_input("Ставка ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b_wheel")
    
    sectors = [
        {"label": "💥 ПРОГРАШ (0x)", "multiplier": 0},
        {"label": "🥉 1.5x Множник", "multiplier": 1.5},
        {"label": "💥 ПРОГРАШ (0x)", "multiplier": 0},
        {"label": "🥈 2x Множник", "multiplier": 2},
        {"label": "💥 ПРОГРАШ (0x)", "multiplier": 0},
        {"label": "🥇 3x Множник", "multiplier": 3},
        {"label": "💎 5x ДЖЕКПОТ", "multiplier": 5}
    ]
    
    wheel_placeholder = st.empty()
    wheel_placeholder.markdown("### 🎡 Крути колесо та перевір свою удачу!")
    
    if st.button("Крутити колесо!"):
        if bet_wheel > st.session_state.balance:
            st.error("Недостатньо коштів!")
        else:
            st.session_state.balance -= bet_wheel
            
            with st.spinner("Колесо обертається... 🌀"):
                for _ in range(12):
                    temp_sector = random.choice(sectors)
                    wheel_placeholder.markdown(f"## 🎡 [ {temp_sector['label']} ]")
                    time.sleep(0.15)
            
            final_sector = random.choice(sectors)
            wheel_placeholder.markdown(f"# 🎡 Результат: {final_sector['label']}")
            
            mult = final_sector["multiplier"]
            if mult > 0:
                win = int(bet_wheel * mult)
                st.session_state.balance += win
                st.success(f"🎉 Ви виграли ${win}! ({mult}x виплата)")
                st.session_state.history.insert(0, {"Гра": "Колесо", "Ставка": bet_wheel, "Результат": f"Виграш ({final_sector['label']})", "Виплата": f"+${win}"})
            else:
                st.error("❌ Ви програли! Пощастить наступного разу.")
                st.session_state.history.insert(0, {"Гра": "Колесо", "Ставка": bet_wheel, "Результат": "Програш", "Виплата": f"-${bet_wheel}"})

with tab2:
    st.header("Гральний автомат (Слоти)")
    bet1 = st.number_input("Ставка ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b1")
    
    if st.button("Крутити слоти!"):
        if bet1 > st.session_state.balance:
            st.error("Недостатньо коштів!")
        else:
            st.session_state.balance -= bet1
            symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]
            res = [random.choice(symbols) for _ in range(3)]
            
            st.markdown(f"## {res[0]} | {res[1]} | {res[2]}")
            
            if res[0] == res[1] == res[2]:
                win = bet1 * 10
                st.session_state.balance += win
                st.success(f"🎉 Джекпот! Виграш: ${win}")
                st.session_state.history.insert(0, {"Гра": "Слоти", "Ставка": bet1, "Результат": "Виграш (Джекпот)", "Виплата": f"+${win}"})
            elif res[0] == res[1] or res[1] == res[2] or res[0] == res[2]:
                win = int(bet1 * 1.5)
                st.session_state.balance += win
                st.info(f"✨ Збіг пари! Виграш: ${win}")
                st.session_state.history.insert(0, {"Гра": "Слоти", "Ставка": bet1, "Результат": "Виграш (Пара)", "Виплата": f"+${win}"})
            else:
                st.error("❌ Ви програли")
                st.session_state.history.insert(0, {"Гра": "Слоти", "Ставка": bet1, "Результат": "Програш", "Виплата": f"-${bet1}"})

with tab3:
    st.header("Орел чи Решка")
    bet2 = st.number_input("Ставка ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b2")
    choice = st.radio("Ваш вибір:", ["Орел", "Решка"])
    
    if st.button("Підкинути монету"):
        if bet2 > st.session_state.balance:
            st.error("Недостатньо коштів!")
        else:
            st.session_state.balance -= bet2
            result = random.choice(["Орел", "Решка"])
            
            st.write(f"Результат: **{result}**")
            
            if choice == result:
                win = bet2 * 2
                st.session_state.balance += win
                st.success(f"🎉 Перемога! Виграш: ${win}")
                st.session_state.history.insert(0, {"Гра": "Монета", "Ставка": bet2, "Результат": f"Виграш ({result})", "Виплата": f"+${win}"})
            else:
                st.error("❌ Ви програли")
                st.session_state.history.insert(0, {"Гра": "Монета", "Ставка": bet2, "Результат": f"Програш ({result})", "Виплата": f"-${bet2}"})

with tab4:
    st.header("Кидок кісток")
    bet3 = st.number_input("Ставка ($)", min_value=1, max_value=max(1, st.session_state.balance), value=min(10, st.session_state.balance), key="b3")
    target_sum = st.slider("Вгадайте загальну суму двох кісток:", 2, 12, 7)
    
    if st.button("Кинути кістки"):
        if bet3 > st.session_state.balance:
            st.error("Недостатньо коштів!")
        else:
            st.session_state.balance -= bet3
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            total = d1 + d2
            
            st.markdown(f"### Кістки: 🎲 {d1} та 🎲 {d2} (Сума: {total})")
            
            if total == target_sum:
                win = bet3 * 6
                st.session_state.balance += win
                st.success(f"🎉 Ідеальний збіг! Виграш: ${win}")
                st.session_state.history.insert(0, {"Гра": "Кістки", "Ставка": bet3, "Результат": f"Виграш (Сума {total})", "Виплата": f"+${win}"})
            else:
                st.error("❌ Ви програли")
                st.session_state.history.insert(0, {"Гра": "Кістки", "Ставка": bet3, "Результат": f"Програш (Сума {total})", "Виплата": f"-${bet3}"})

with tab5:
    st.header("🎁 Відкриття кейсів (Сміття та Імба)")
    st.write("Купуй кейси та випробовуй удачу: може випасти як повний мотлох, так і легендарний жирний дроп!")

    cases_config = {
        "🗑️ Сміттєвий бак ($10)": {
            "price": 10,
            "items": [
                {"name": "🍌 Бананова шкірка", "value": 1, "rarity": "Мотлох"},
                {"name": "🧦 Дірява шкарпетка", "value": 2, "rarity": "Мотлох"},
                {"name": "📦 Порожня коробка з-під піци", "value": 5, "rarity": "Звичайний"},
                {"name": "🔋 Сіта батарейка", "value": 8, "rarity": "Звичайний"},
                {"name": "💻 Зламані «жигулі» на флешці", "value": 15, "rarity": "Рідкісний"},
                {"name": "🏆 Золотий злиток (майже справжній)", "value": 50, "rarity": "ЛЕГЕНДАРНИЙ!"}
            ],
            "weights": [40, 30, 15, 10, 4, 1]
        },
        "📦 Стандартний кейс ($50)": {
            "price": 50,
            "items": [
                {"name": "🥤 М'ята банка коли", "value": 5, "rarity": "Мотлох"},
                {"name": "📰 Вчорашня газета", "value": 15, "rarity": "Звичайний"},
                {"name": "🎧 Навушники з одним робочим вухом", "value": 40, "rarity": "Звичайний"},
                {"name": "⌨️ Стара клавіатура", "value": 75, "rarity": "Рідкісний"},
                {"name": "📱 Б/У смартфон з тріснутим екраном", "value": 150, "rarity": "Епічний"},
                {"name": "💎 Справжній алмаз", "value": 400, "rarity": "ЛЕГЕНДАРНИЙ!"}
            ],
            "weights": [35, 30, 20, 10, 4, 1]
        },
        "👑 Елітний кейс ($200)": {
            "price": 200,
            "items": [
                {"name": "🪨 Звичайний камінь з вулиці", "value": 20, "rarity": "Мотлох"},
                {"name": "☕ Охолола кава", "value": 50, "rarity": "Звичайний"},
                {"name": "🕹️ Потертий геймпад", "value": 150, "rarity": "Рідкісний"},
                {"name": "💻 Ігровий ноутбук (б/в)", "value": 350, "rarity": "Епічний"},
                {"name": "🏎️ Ключі від спорткара", "value": 1200, "rarity": "ЛЕГЕНДАРНИЙ!"},
                {"name": "🏝️ Власний острів", "value": 5000, "rarity": "МІФІЧНИЙ!!!"}
            ],
            "weights": [30, 30, 25, 10, 4, 1]
        }
    }

    selected_case_name = st.selectbox("Оберіть кейс для відкриття:", list(cases_config.keys()))
    case_data = cases_config[selected_case_name]

    st.info(f"Вартість відкриття: **${case_data['price']}**")

    with st.expander("👀 Подивитися вміст кейса та шанси"):
        for item in case_data["items"]:
            st.write(f"- **{item['rarity']}** | {item['name']} (Цінність: ${item['value']})")

    case_placeholder = st.empty()

    if st.button("Відкрити кейс!", type="primary"):
        if case_data["price"] > st.session_state.balance:
            st.error("Недостатньо коштів для купівлі кейса!")
        else:
            st.session_state.balance -= case_data["price"]

            with st.spinner("Кейс відкривається..."):
                for _ in range(10):
                    rand_item = random.choice(case_data["items"])
                    case_placeholder.markdown(f"### 🌀 Крутимо... [{rand_item['rarity']}] {rand_item['name']}")
                    time.sleep(0.1)

            won_item = random.choices(case_data["items"], weights=case_data["weights"], k=1)[0]
            
            st.session_state.balance += won_item["value"]

            if won_item["rarity"] in ["ЛЕГЕНДАРНИЙ!", "МІФІЧНИЙ!!!"]:
                case_placeholder.markdown(f"# 🌟 ДЖЕКПОТ! ВИПАЛО: {won_item['rarity']} {won_item['name']} 🎉")
                st.balloons()
            elif won_item["rarity"] == "Епічний":
                case_placeholder.markdown(f"# 🔥 КРУТИЙ ДРОП: [{won_item['rarity']}] {won_item['name']}")
            elif won_item["rarity"] == "Рідкісний":
                case_placeholder.markdown(f"# ✨ Непогано: [{won_item['rarity']}] {won_item['name']}")
            else:
                case_placeholder.markdown(f"# 🗑️ Мотлох: [{won_item['rarity']}] {won_item['name']}")

            profit = won_item["value"] - case_data["price"]
            if profit >= 0:
                st.success(f"Ви забрали предмет вартістю ${won_item['value']}! (Профіт: +${profit})")
            else:
                st.warning(f"Ви забрали предмет вартістю ${won_item['value']} (Збиток: -${abs(profit)})")

            st.session_state.history.insert(0, {
                "Гра": "Кейси", 
                "Ставка": case_data["price"], 
                "Результат": f"Дроп: {won_item['name']} ({won_item['rarity']})", 
                "Виплата": f"+${won_item['value']}"
            })

with tab6:
    st.header("Історія ігор")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ще не зіграно жодної гри. Почніть грати, щоб побачити історію!")