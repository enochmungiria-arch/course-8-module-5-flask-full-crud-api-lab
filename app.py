
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Task 1: Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Task 2: Get the data sent by the client
    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    # Task 3: Find the next available ID
    new_id = max((event.id for event in events), default=0) + 1

    new_event = Event(new_id, title.strip())
    events.append(new_event)

    # Task 4: Return the created event
    return jsonify(new_event.to_dict()), 201


# Task 1: Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Task 2 and 3: Loop through events to find the matching ID
    for event in events:
        if event.id == event_id:
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({"error": "A valid JSON object is required"}), 400

            title = data.get("title")

            if not isinstance(title, str) or not title.strip():
                return jsonify({"error": "A valid title is required"}), 400

            event.title = title.strip()

            # Task 4: Return the updated event
            return jsonify(event.to_dict()), 200

    # Event not found
    return jsonify({"error": "Event not found"}), 404


# Task 1: Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Task 2 and 3: Loop through events to find the matching ID
    for event in events:
        if event.id == event_id:
            events.remove(event)

            # Task 4: Return a success message
            return jsonify({
                "message": "Event deleted successfully",
                "event": event.to_dict()
            }), 200

    # Event not found
    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
