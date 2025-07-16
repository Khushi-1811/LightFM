import streamlit as st
import pandas as pd
from data import dummy_users, dummy_dishes
from datetime import datetime
import io

# --------------------------------
# Initialize multi-user session state
# --------------------------------
if "user_profiles" not in st.session_state:
    st.session_state.user_profiles = {}
    for user in dummy_users:
        st.session_state.user_profiles[user["user_id"]] = {
            "initial_data": {
                "goals": user["goals"].copy(),
                "price_sensitivity": user["price_sensitivity"],
                "weights": user["weights"].copy()
            },
            "goals": user["goals"].copy(),
            "price_sensitivity": user["price_sensitivity"],
            "weights": user["weights"].copy(),
            "action_log": [],
            "weight_history": [user["weights"].copy()]
        }
    st.session_state.current_user_id = dummy_users[0]["user_id"]

# --------------------------------
# Sidebar: select user
# --------------------------------
user_ids = list(st.session_state.user_profiles.keys())
selected_user_id = st.sidebar.selectbox("👤 Select User Profile", user_ids,
                                        index=user_ids.index(st.session_state.current_user_id))
st.session_state.current_user_id = selected_user_id
current_profile = st.session_state.user_profiles[selected_user_id]

# --------------------------------
# Sidebar: adjust only explicit goals & price sensitivity
# --------------------------------
st.sidebar.header(f"🎯 {selected_user_id} Settings")
goals = current_profile["goals"]
protein = st.sidebar.slider("Goal: Protein %", 10, 60, goals["protein"])
carbs = st.sidebar.slider("Goal: Carbs %", 10, 60, goals["carbs"])
fats = st.sidebar.slider("Goal: Fats %", 10, 60, goals["fats"])

price_sensitivity = st.sidebar.slider(
    "Price Sensitivity", 0.0, 1.0, current_profile["price_sensitivity"]
)

# ✅ Save updates
current_profile["goals"] = {"protein": protein, "carbs": carbs, "fats": fats}
current_profile["price_sensitivity"] = price_sensitivity

# --------------------------------
# Sidebar: show current learned weights (read-only)
# --------------------------------
st.sidebar.subheader("📈 Current Learned Feature Weights")
weights_df = pd.DataFrame([current_profile["weights"]])
st.sidebar.dataframe(weights_df)

# Save to weight history for evolution plots
current_profile["weight_history"].append(current_profile["weights"].copy())


# --------------------------------
# Compute final score
# --------------------------------
def compute_final_score(dish_features, user_weights):
    numerator = sum(
        dish_features.get(feature.replace("_factor", ""), 0) * weight
        for feature, weight in user_weights.items()
    )
    denominator = sum(user_weights.values()) + 1e-8
    return numerator / denominator

# --------------------------------
# Compute original scores once
# --------------------------------
if "original_scores" not in st.session_state:
    st.session_state.original_scores = {}
for user_id in st.session_state.user_profiles:
    if user_id not in st.session_state.original_scores:
        original_results = []
        initial_weights = st.session_state.user_profiles[user_id]["initial_data"]["weights"]
        for dish in dummy_dishes:
            orig_score = compute_final_score(dish["features"], initial_weights)
            original_results.append({"Dish": dish["name"], "Original Score": round(orig_score,3)})
        st.session_state.original_scores[user_id] = pd.DataFrame(original_results).set_index("Dish")

# --------------------------------
# Compute current scores
# --------------------------------
current_results = []
for dish in dummy_dishes:
    score = compute_final_score(dish["features"], current_profile["weights"])
    current_results.append({"Dish": dish["name"], "Current Score": round(score,3)})
current_scores_df = pd.DataFrame(current_results).set_index("Dish")

# --------------------------------
# Merge for comparison
# --------------------------------
comparison_df = st.session_state.original_scores[selected_user_id].join(current_scores_df)
comparison_df["Change"] = comparison_df["Current Score"] - comparison_df["Original Score"]
comparison_df = comparison_df.sort_values("Current Score", ascending=False)

# --------------------------------
# Show table
# --------------------------------
st.subheader("📊 Original vs Adapted Recommendation Scores")
st.dataframe(comparison_df, use_container_width=True)

# --------------------------------
# Update weights on actions
# --------------------------------
def update_weights(profile, dish_features, action):
    learning_map = {
        "ordered": 0.05,
        "add_to_cart": 0.04,
        "removed_from_cart": -0.04,
        "viewed_but_not_ordered": -0.02,
        "viewed_and_ordered": 0.07,
        "download_data_but_not_ordered": -0.01,
        "download_data_and_ordered": 0.05,
        "added_extra_items": 0.03
    }
    adjust = learning_map.get(action, 0.0)
    for feature_key in profile["weights"]:
        feature = feature_key.replace("_factor", "")
        if feature in dish_features:
            new_weight = profile["weights"][feature_key] + adjust * dish_features[feature]
            profile["weights"][feature_key] = max(0.0, min(1.0, new_weight))
    return profile


# --------------------------------
# Take actions
# --------------------------------
st.subheader("📝 Take Action on Dishes")
selected_dishes = st.multiselect("Select dishes to act on", [dish["name"] for dish in dummy_dishes])
action = st.radio("Action", [
    "ordered", "add_to_cart", "removed_from_cart",
    "viewed_but_not_ordered", "viewed_and_ordered",
    "download_data_but_not_ordered", "download_data_and_ordered",
    "added_extra_items"
])


if st.button("Submit Action"):
    for dish_name in selected_dishes:
        dish_data = next(d for d in dummy_dishes if d["name"] == dish_name)
        current_profile["action_log"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dish": dish_name,
            "action": action
        })
        update_weights(current_profile, dish_data["features"], action)
        current_profile["weight_history"].append(current_profile["weights"].copy())
    st.success(f"Logged & updated weights for {selected_dishes}")

# --------------------------------
# Reset user
# --------------------------------
if st.button("🔄 Reset Profile"):
    data = current_profile["initial_data"]
    current_profile["goals"] = data["goals"].copy()
    current_profile["price_sensitivity"] = data["price_sensitivity"]
    current_profile["weights"] = data["weights"].copy()
    current_profile["action_log"] = []
    current_profile["weight_history"] = [data["weights"].copy()]
    st.success(f"Profile for {selected_user_id} reset to original.")

# --------------------------------
# Show action log
# --------------------------------
if current_profile["action_log"]:
    st.subheader(f"📜 Action Log for {selected_user_id}")
    log_df = pd.DataFrame(current_profile["action_log"])
    st.dataframe(log_df)

    # download
    csv_buffer = io.StringIO()
    log_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇️ Download Action Log CSV",
        data=csv_buffer.getvalue(),
        file_name=f"{selected_user_id}_action_log.csv",
        mime="text/csv"
    )
else:
    st.info(f"No actions logged yet for {selected_user_id}.")

# --------------------------------
# Show weight evolution
# --------------------------------
st.subheader(f"📈 Weight Evolution Over Time for {selected_user_id}")
if current_profile["weight_history"]:
    history_df = pd.DataFrame(current_profile["weight_history"])
    st.line_chart(history_df)
