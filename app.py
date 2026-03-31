from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb://db:27017/")
db = client["gst_db"]
collection = db["bills"]

# ------------------ UI ------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart GST Billing</title>
    <style>
        body {
            font-family: 'Segoe UI';
            background: linear-gradient(to right, #667eea, #764ba2);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            width: 320px;
        }

        h2 {
            margin-bottom: 20px;
            color: #333;
        }

        select, input {
            margin: 8px 0;
            padding: 10px;
            width: 100%;
            border-radius: 8px;
            border: 1px solid #ccc;
        }

        button {
            margin-top: 15px;
            padding: 12px;
            width: 100%;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: 0.3s;
        }

        button:hover {
            background: #5a67d8;
        }

        #result {
            margin-top: 20px;
            font-weight: bold;
            color: green;
        }
    </style>
</head>
<body>

<div class="card">
    <h2>Smart GST Billing</h2>

    <select id="category1">
        <option value="18">📱 Electronics (18%)</option>
        <option value="5">👕 Clothes (5%)</option>
        <option value="12">🍔 Eatery (12%)</option>
    </select>
    <input id="price1" placeholder="Item 1 Price">

    <select id="category2">
        <option value="18">📱 Electronics (18%)</option>
        <option value="5">👕 Clothes (5%)</option>
        <option value="12">🍔 Eatery (12%)</option>
    </select>
    <input id="price2" placeholder="Item 2 Price">

    <button onclick="calculate()">Generate Bill</button>

    <h3 id="result"></h3>
</div>

<script>
function calculate() {
    fetch('/bill', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            items: [
                {
                    price: Number(document.getElementById('price1').value),
                    gst: Number(document.getElementById('category1').value)
                },
                {
                    price: Number(document.getElementById('price2').value),
                    gst: Number(document.getElementById('category2').value)
                }
            ]
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('result').innerHTML =
            "Total: ₹" + data.final + " | GST: ₹" + data.gst;
    });
}
</script>

</body>
</html>
"""

# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)


def calculate_gst(price, gst_rate):
    return (price * gst_rate) / 100


@app.route('/bill', methods=['POST'])
def generate_bill():
    data = request.json
    items = data.get("items", [])

    total = 0
    total_gst = 0

    for item in items:
        price = item.get("price") or 0
        gst = item.get("gst") or 0

        gst_amount = calculate_gst(price, gst)
        total += price
        total_gst += gst_amount

    final_amount = total + total_gst

    bill_data = {
        "items": items,
        "subtotal": total,
        "gst": total_gst,
        "final": final_amount
    }

    # Save to MongoDB
    result = collection.insert_one(bill_data)
    bill_data["_id"] = str(result.inserted_id)

    return jsonify(bill_data)


# ------------------ Run ------------------

if __name__ == "__main__":
    print("Starting Smart GST App...")
    app.run(host="0.0.0.0", port=5000)