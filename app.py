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

# Helper function to find event by ID
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    
    # Validate input
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Generate new ID (max current ID + 1)
    new_id = max(event.id for event in events) + 1 if events else 1
    
    # Create new event
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    
    # Validate input
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Find the event
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Update the title
    event.title = data["title"]
    
    return jsonify(event.to_dict()), 200

# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Remove the event
    events.remove(event)
    
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
