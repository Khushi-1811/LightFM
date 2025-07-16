import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle
from datetime import datetime

st.set_page_config(page_title="FitShield Recommender", layout="wide")

# -------------------------------
# Load model and dataset
# -------------------------------
@st.cache_resource
def load_model_and_dataset():
    with open("lightfm_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("lightfm_dataset.pkl", "rb") as f:
        dataset = pickle.load(f)
    return model, dataset

model, dataset = load_model_and_dataset()
user_id_map, _, item_id_map, _ = dataset.mapping()
dish_ids = list(item_id_map.keys())

# -------------------------------
# Dummy dish metadata
# -------------------------------
dummy_dishes = [{"dish_id": d, "name": f"Dish {d.split('_')[-1]}"} for d in dish_ids]

# -------------------------------
# Log user actions
# -------------------------------
def log_action(user_id, dish_id, action, log_path="interactions_log.json"):
    new_entry = {
        "user_id": user_id,
        "dish_id": dish_id,
        "action": action,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        with open(log_path, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    logs.append(new_entry)
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)

# -------------------------------
# Recommend top N dishes
# -------------------------------
def recommend_dishes(user_id, top_n=5):
    if user_id not in user_id_map:
        return []
    internal_uid = user_id_map[user_id]
    internal_iids = [item_id_map[d] for d in dish_ids]
    scores = model.predict([internal_uid] * len(internal_iids), internal_iids)
    top_indices = np.argsort(scores)[::-1][:top_n]
    return [(dish_ids[i], scores[i]) for i in top_indices]

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🍽️ FitShield - Personalized Dish Recommender")

# User selection
user_id = st.selectbox("👤 Select your user ID", list(user_id_map.keys()))

# Action logging interface
st.subheader("📝 Log Your Actions on Dishes")
for dish in dummy_dishes:
    dish_name = dish["name"]
    dish_id = dish["dish_id"]
    with st.expander(f"{dish_name}"):
        action = st.radio(
            f"Choose action for {dish_name}",
            ["liked", "searched", "menu_interest", "viewed_and_ordered", "viewed_not_ordered",
             "downloaded_and_ordered", "downloaded_not_ordered", "added_extra_items", "added_or_removed_from_cart"],
            key=f"action_{dish_id}"
        )
        if st.button(f"✅ Log Action for {dish_name}", key=f"log_{dish_id}"):
            log_action(user_id, dish_id, action)
            st.success(f"Action '{action}' logged for {dish_name}")

# Show logs (optional)
if st.checkbox("📜 Show my session logs"):
    try:
        with open("interactions_log.json", "r") as f:
            logs = json.load(f)
        user_logs = [l for l in logs if l["user_id"] == user_id]
        if user_logs:
            st.write(pd.DataFrame(user_logs))
        else:
            st.info("No actions logged yet.")
    except FileNotFoundError:
        st.info("No log file found.")

# Divider
st.markdown("---")

# Recommendation trigger
if st.button("🔁 Show Recommendations Based on My Actions"):
    st.subheader("🔝 Recommended Dishes for You")
    top_n = st.slider("Top N Recommendations", 3, 10, 5)
    recommendations = recommend_dishes(user_id, top_n)

    if recommendations:
        for dish_id, score in recommendations:
            dish_name = next((d["name"] for d in dummy_dishes if d["dish_id"] == dish_id), dish_id)
            st.markdown(f"- **{dish_name}** (Score: `{score:.3f}`)")
    else:
        st.warning("User not found in trained model.")
