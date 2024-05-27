from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import model


app = Flask(__name__)
CORS(app)


@app.route('/machine-learning', methods=['POST'])
def findAll():

    course = request.json["course"]
    # city = request.json["city"]
    ML = model.get_recommendations(course)
    return jsonify(ML)


if __name__ == '__main__':
    app.run(debug=True)