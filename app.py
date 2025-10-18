from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory "database"
read_goals = []

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Reading Goals API is running!"})

# Get all goals
@app.route("/goals", methods=["GET"])
def get_goals():
    return jsonify(read_goals)

# Add a new goal
@app.route("/goals", methods=["POST"])
def add_goal():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing title"}), 400
    
    new_goal = {
        "id": len(read_goals) + 1,
        "title": data["title"],
        "dateAdded": data.get("dateAdded", datetime.now().isoformat()),
        "read": data.get("read", False)
    }
    read_goals.append(new_goal)
    print(f"Added goal: {new_goal['title']}")
    return jsonify(new_goal), 201

# Update an existing goal
@app.route("/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    data = request.get_json()
    for goal in read_goals:
        if goal["id"] == goal_id:
            goal["title"] = data.get("title", goal["title"])
            goal["read"] = data.get("read", goal["read"])
            return jsonify(goal)
    return jsonify({"error": "Goal not found"}), 404

# Delete a goal
@app.route("/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    global read_goals
    read_goals = [goal for goal in read_goals if goal["id"] != goal_id]
    return jsonify({"message": "Goal deleted"}), 200

PORT = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
