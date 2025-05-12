from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TREE_DATA = {
    "Acacia": {"ET0": 1000, "Kc": 0.7, "Aa": 12},
    "Sidr": {"ET0": 1000, "Kc": 0.9, "Aa": 14},
    "Tamarix": {"ET0": 1000, "Kc": 0.6, "Aa": 10},
    "Ghaf": {"ET0": 1000, "Kc": 0.5, "Aa": 8}
}

SOIL_MULTIPLIERS = {
    "Sandy": 1.2,
    "Loamy": 1.0,
    "Clay": 0.85
}

@app.route("/")
def home():
    return "<h1>Tree Water Backend API</h1>"

@app.route("/trees")
def trees():
    return jsonify(list(TREE_DATA.keys()))

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    species = data.get("Tree_Species")
    count = int(data.get("Tree_Count", 1))
    soil = data.get("Soil_Type", "Loamy")
    zone = data.get("Zone", "Default")

    if species not in TREE_DATA:
        return jsonify({"error": "Unknown tree species"}), 400

    soil_factor = SOIL_MULTIPLIERS.get(soil, 1.0)
    tree = TREE_DATA[species]

    annual_liters = tree["ET0"] * tree["Kc"] * tree["Aa"] * soil_factor
    total_liters = annual_liters * count

    return jsonify({
        "Tree_Species": species,
        "Tree_Count": count,
        "Soil_Type": soil,
        "Zone": zone,
        "Annual_Water_Consumption_Liters": round(annual_liters, 2),
        "Total_Consumption_Liters": round(total_liters, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)