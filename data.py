# -------------------------------
# Dummy Users
# -------------------------------

dummy_users = [
    {
        "user_id": "user_1",
        "goals": {"protein": 35, "carbs": 40, "fats": 25},
        "price_sensitivity": 0.7,
        "weights": {
            "density_factor": 0.2, "satiety_factor": 0.3, "euclidean_factor": 0.2,
            "protein_overrule_factor": 0.1, "good_fats_factor": 0.15, "sugar_content_factor": 0.05
        }
    },
    {
        "user_id": "user_2",
        "goals": {"protein": 25, "carbs": 50, "fats": 25},
        "price_sensitivity": 0.5,
        "weights": {
            "density_factor": 0.25, "satiety_factor": 0.25, "euclidean_factor": 0.2,
            "protein_overrule_factor": 0.05, "good_fats_factor": 0.15, "sugar_content_factor": 0.1
        }
    },
    {
        "user_id": "user_3",
        "goals": {"protein": 40, "carbs": 30, "fats": 30},
        "price_sensitivity": 0.9,
        "weights": {
            "density_factor": 0.15, "satiety_factor": 0.35, "euclidean_factor": 0.1,
            "protein_overrule_factor": 0.2, "good_fats_factor": 0.1, "sugar_content_factor": 0.1
        }
    },
    {
        "user_id": "user_4",
        "goals": {"protein": 20, "carbs": 60, "fats": 20},
        "price_sensitivity": 0.3,
        "weights": {
            "density_factor": 0.2, "satiety_factor": 0.3, "euclidean_factor": 0.15,
            "protein_overrule_factor": 0.05, "good_fats_factor": 0.2, "sugar_content_factor": 0.1
        }
    },
    {
        "user_id": "user_5",
        "goals": {"protein": 30, "carbs": 45, "fats": 25},
        "price_sensitivity": 0.6,
        "weights": {
            "density_factor": 0.25, "satiety_factor": 0.25, "euclidean_factor": 0.2,
            "protein_overrule_factor": 0.1, "good_fats_factor": 0.1, "sugar_content_factor": 0.1
        }
    },
    {
        "user_id": "user_6",
        "goals": {"protein": 50, "carbs": 30, "fats": 20},
        "price_sensitivity": 0.4,
        "weights": {
            "density_factor": 0.3, "satiety_factor": 0.3, "euclidean_factor": 0.1,
            "protein_overrule_factor": 0.2, "good_fats_factor": 0.05, "sugar_content_factor": 0.05
        }
    }
]

# -------------------------------
# Dummy Dishes
# -------------------------------

dummy_dishes = [
    {"dish_id": "dish_1", "name": "Grilled Chicken Bowl",
     "features": {"density": 0.7, "satiety": 0.8, "euclidean": 0.2,
                  "protein_overrule": 0.6, "good_fats": 0.4, "sugar_content": 0.3}},
    {"dish_id": "dish_2", "name": "Quinoa Veggie Salad",
     "features": {"density": 0.5, "satiety": 0.6, "euclidean": 0.3,
                  "protein_overrule": 0.5, "good_fats": 0.3, "sugar_content": 0.2}},
    {"dish_id": "dish_3", "name": "Steak with Avocado",
     "features": {"density": 0.8, "satiety": 0.7, "euclidean": 0.1,
                  "protein_overrule": 0.7, "good_fats": 0.6, "sugar_content": 0.4}},
    {"dish_id": "dish_4", "name": "Light Greek Yogurt",
     "features": {"density": 0.4, "satiety": 0.5, "euclidean": 0.4,
                  "protein_overrule": 0.4, "good_fats": 0.2, "sugar_content": 0.1}},
    {"dish_id": "dish_5", "name": "Salmon Power Plate",
     "features": {"density": 0.9, "satiety": 0.9, "euclidean": 0.2,
                  "protein_overrule": 0.8, "good_fats": 0.7, "sugar_content": 0.5}},
    {"dish_id": "dish_6", "name": "Fruit Parfait",
     "features": {"density": 0.3, "satiety": 0.4, "euclidean": 0.5,
                  "protein_overrule": 0.3, "good_fats": 0.1, "sugar_content": 0.2}},
    {"dish_id": "dish_7", "name": "Chicken Wrap",
     "features": {"density": 0.6, "satiety": 0.7, "euclidean": 0.3,
                  "protein_overrule": 0.6, "good_fats": 0.5, "sugar_content": 0.3}},
    {"dish_id": "dish_8", "name": "Tofu Buddha Bowl",
     "features": {"density": 0.5, "satiety": 0.8, "euclidean": 0.2,
                  "protein_overrule": 0.5, "good_fats": 0.3, "sugar_content": 0.2}},
    {"dish_id": "dish_9", "name": "Beef Stir Fry",
     "features": {"density": 0.7, "satiety": 0.6, "euclidean": 0.3,
                  "protein_overrule": 0.7, "good_fats": 0.6, "sugar_content": 0.4}},
    {"dish_id": "dish_10", "name": "Protein Pasta Bowl",
     "features": {"density": 0.8, "satiety": 0.9, "euclidean": 0.1,
                  "protein_overrule": 0.8, "good_fats": 0.7, "sugar_content": 0.5}},
    {"dish_id": "dish_11", "name": "Berry Smoothie",
     "features": {"density": 0.4, "satiety": 0.5, "euclidean": 0.4,
                  "protein_overrule": 0.4, "good_fats": 0.2, "sugar_content": 0.1}},
    {"dish_id": "dish_12", "name": "Keto Avocado Bowl",
     "features": {"density": 0.9, "satiety": 0.7, "euclidean": 0.2,
                  "protein_overrule": 0.9, "good_fats": 0.8, "sugar_content": 0.6}},
    {"dish_id": "dish_13", "name": "Light Veggie Soup",
     "features": {"density": 0.3, "satiety": 0.4, "euclidean": 0.5,
                  "protein_overrule": 0.3, "good_fats": 0.1, "sugar_content": 0.2}},
    {"dish_id": "dish_14", "name": "Turkey Sandwich",
     "features": {"density": 0.5, "satiety": 0.6, "euclidean": 0.3,
                  "protein_overrule": 0.5, "good_fats": 0.3, "sugar_content": 0.2}},
    {"dish_id": "dish_15", "name": "Pesto Chicken Plate",
     "features": {"density": 0.6, "satiety": 0.7, "euclidean": 0.3,
                  "protein_overrule": 0.6, "good_fats": 0.5, "sugar_content": 0.3}}
]
