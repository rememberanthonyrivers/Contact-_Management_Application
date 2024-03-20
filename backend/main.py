# this file will contain the main enpoints of our app
# CRUD app
# ///////////////////////////////////////////////////////
# Create
# - first name
# - last name
# - email
# ///////////////////////////////////////////////////////
# Request
# type: GET, POST, PATCH(update), DELETE
# sends json
# ///////////////////////////////////////////////////////
# Response
# returns a response form the backend
# also give us a status code: 200, 404, 500
# returns json
# ///////////////////////////////////////////////////////
from flask import request, jsonify
from config import app, db
from models import Contact


# python decorator for getting the data
@app.route("/contacts", methods=["GET"])
def get_contacts():
    # getting all of the different contacts in our contact database
    contacts = Contact.query.all()
    # Since we cant return python objects, this line converts our contacts list to json using a one liner lamba fucntion
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts}), 200


# python decorator for creating the contact object and then to be added to the database
@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    #  checkss to make sure if we have a first, last name and email in the databe
    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email"}),
            400,
        )
    # creates a new object from our Contact model
    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    # Let's add a new object of our create contact method to the database
    try:
        db.session.add(
            new_contact
        )  # our object is not in the staging area to be added to the database
        db.session.commit()  # anything in the staging area will now be added to the database
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    # returns a msg to the user displaying the user Created with a 201 status code
    return jsonify({"message": "User Created!"}), 201


# python decorator for updating the contact list
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    # checks if the contact object exists, and displays a 404 if the user is not found
    if not contact:
        return jsonify({"message": "User not found."}), 404
    # this line parses through the Json data
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    # saves the session to the database
    db.session.commit()
    # returns a msg to the user with the displaying the user is updated with a 200 status code
    return jsonify({"message": "User Updated"}), 200


# python decorator for deleting the contact from the contact list
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    # looks for the contact with the user id
    contact = Contact.query.get(user_id)
    # if it doesnt exist lets return a 404
    if not contact:
        return jsonify({"message": "User not found."}), 404
    # the below line deletes the contact and then saves the current database session
    db.session.delete(contact)
    db.session.commit()
    # returns a msg to the user with the displaying the user is deleted with a 200 status code
    return jsonify({"message": "User Deleted"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # ^ these two lines of code creates our database
    app.run(debug=True)
