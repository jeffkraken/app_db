from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "/data/database.db"

def get_connection():
    return sqlite3.connect(DATABASE)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>POS Terminal v1.0</title>
        <style>
            body {
                background-color: #000000;
                color: #00ff00;
                font-family: "Courier New", Courier, monospace;
                margin: 0;
                padding: 20px;
            }

            .pos-container {
                border: 4px solid #00ff00;
                padding: 20px;
                background-color: #001100;
                box-shadow: 0 0 20px #00ff00;
            }

            h1 {
                text-align: center;
                border-bottom: 2px solid #00ff00;
                padding-bottom: 10px;
                margin-top: 0;
                letter-spacing: 3px;
            }

            .controls {
                margin-bottom: 15px;
            }

            button {
                background-color: #003300;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 10px 20px;
                font-family: "Courier New", Courier, monospace;
                font-size: 14px;
                cursor: pointer;
                box-shadow: 3px 3px 0 #00aa00;
            }

            button:active {
                box-shadow: none;
                transform: translate(3px, 3px);
            }

            table {
                width: 100%;
                border-collapse: collapse;
                background-color: #000000;
            }

            th, td {
                border: 1px solid #00ff00;
                padding: 8px;
                text-align: left;
            }

            th {
                background-color: #003300;
            }

            tbody tr:nth-child(even) {
                background-color: #001a00;
            }

            .status-bar {
                margin-top: 15px;
                padding-top: 10px;
                border-top: 2px solid #00ff00;
                font-size: 12px;
            }

            .blink {
                animation: blink-animation 1s steps(2, start) infinite;
            }

            @keyframes blink-animation {
                to {
                    visibility: hidden;
                }
            }
        </style>
    </head>
    <body>
        <div class="pos-container">
            <h1>STUDENT POS TERMINAL v1.0</h1>

            <div class="controls">
                <button onclick="loadUsers()">LOAD 10 RANDOM CUSTOMERS</button>
            </div>

            <table id="userTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>FIRST</th>
                        <th>LAST</th>
                        <th>EMAIL</th>
                        <th>IP</th>
                        <th>BOT</th>
                        <th>UUID</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>

            <div class="status-bar">
                STATUS: <span id="statusText">READY</span>
                <span class="blink">█</span>
            </div>
        </div>

        <script>
            function loadUsers() {
                const status = document.getElementById("statusText");
                status.textContent = "LOADING...";

                fetch('/users')
                    .then(response => response.json())
                    .then(data => {
                        const tableBody = document.querySelector("#userTable tbody");
                        tableBody.innerHTML = "";

                        data.forEach(user => {
                            const row = document.createElement("tr");

                            user.forEach(field => {
                                const cell = document.createElement("td");
                                cell.textContent = field;
                                row.appendChild(cell);
                            });

                            tableBody.appendChild(row);
                        });

                        status.textContent = "10 RECORDS LOADED";
                    })
                    .catch(error => {
                        status.textContent = "ERROR";
                        alert("SYSTEM ERROR: Unable to load users");
                    });
            }
        </script>
    </body>
    </html>
    """

@app.route("/users", methods=["GET"])
def users():
    conn = get_connection()
    cursor = conn.cursor()

    # Pull 10 random users
    cursor.execute("SELECT * FROM users ORDER BY RANDOM() LIMIT 10;")
    rows = cursor.fetchall()

    conn.close()
    return jsonify(rows)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "ip_address",
        "paired_bot",
        "uuid"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (first_name, last_name, email, ip_address, paired_bot, uuid)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["first_name"],
        data["last_name"],
        data["email"],
        data["ip_address"],
        data["paired_bot"],
        data["uuid"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "User added successfully"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
