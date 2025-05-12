
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

soil_loss_modifier = {
    "Sandy": 1500,
    "Loamy": 500,
    "Clay": 300
}

tree_data = pd.DataFrame({
    "Tree_Species": [
        "Acacia", "Sidr", "Tamarix", "Ghaf",
        "Moringa", "Neem", "Date Palm", "Olive", "Eucalyptus", "Jujube"
    ],
    "ET0_mm_per_year": [
        1800, 1600, 1700, 1500,
        1700, 1750, 1600, 1500, 1800, 1550
    ],
    "Kc": [
        0.45, 0.50, 0.55, 0.30,
        0.60, 0.50, 0.75, 0.65, 0.70, 0.60
    ],
    "Canopy_Area_m2": [
        8, 12, 6, 10,
        5, 7, 15, 8, 20, 6
    ],
    "Irrigation_Efficiency": [
        0.9, 0.85, 0.8, 0.95,
        0.9, 0.85, 0.75, 0.9, 0.8, 0.88
    ],
    "Soil_Type": [
        "Sandy", "Loamy", "Clay", "Sandy",
        "Loamy", "Sandy", "Loamy", "Clay", "Sandy", "Loamy"
    ]
})

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    species = data.get("Tree_Species")
    count = int(data.get("Tree_Count", 1))

    row = tree_data[tree_data["Tree_Species"] == species]

    if row.empty:
        return jsonify({"error": "Tree species not found"}), 404

    row = row.iloc[0]
    ET0 = row.ET0_mm_per_year
    Kc = row.Kc
    A = row.Canopy_Area_m2
    IE = row.Irrigation_Efficiency
    Ls = soil_loss_modifier.get(row.Soil_Type, 1000)

    W_c = ((ET0 * Kc * A) / IE) + Ls
    total = W_c * count

    return jsonify({
        "Tree_Species": species,
        "Tree_Count": count,
        "Annual_Water_Consumption_Liters": round(W_c, 2),
        "Total_Consumption_Liters": round(total, 2)
    })
