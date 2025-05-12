
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

@app.route('/')
def form():
    return '''
    <h2>Tree Water Consumption Calculator</h2>
    <form action="/calculate" method="post">
        <label for="Tree_Species">Select Tree Species:</label>
        <select name="Tree_Species">
            {options}
        </select>
        <button type="submit">Calculate</button>
    </form>
    '''.format(options=''.join(f'<option value="{tree}">{tree}</option>' for tree in tree_data["Tree_Species"]))

@app.route('/trees', methods=['GET'])
def get_trees():
    return jsonify(tree_data["Tree_Species"].tolist())

@app.route('/calculate', methods=['POST'])
def calculate():
    species = request.form.get("Tree_Species") or request.json.get("Tree_Species")
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

    return jsonify({
        "Tree_Species": species,
        "Annual_Water_Consumption_Liters": round(W_c, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
