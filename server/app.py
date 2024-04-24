from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# Endpoint for handling messages (GET and POST)
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Retrieve and return messages in ascending order of time created
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        response = make_response(jsonify(messages), 200)
        return response
    
    elif request.method == 'POST':
        # Create a new message and add it to the database
        data = request.get_json()
        new_message = Message(body=data["body"], username=data["username"])
        db.session.add(new_message)
        db.session.commit()
        # Return the newly created message in the response
        response = make_response(jsonify(new_message.to_dict()), 201)
        return response

# Endpoint for updating or deleting a message by its ID
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # Retrieve the message to be updated or deleted
    update = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        # Update the message attributes based on the provided JSON data
        data = request.get_json()
        for attr in data:
            setattr(update, attr, data[attr])
        db.session.add(update)
        db.session.commit()
        # Return the updated message in the response
        response = make_response(jsonify(update.to_dict()), 200)
        return response
    
    elif request.method == 'DELETE':
        # Delete the specified message from the database
        db.session.delete(update)
        db.session.commit()
        # Return a success message indicating that the message was deleted
        response = make_response(jsonify({"delete_successful": True, "message": "Message deleted."}), 200)
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)