from flask import Flask,render_template, request, json
from flask.json import jsonify
import firestore
import base64
import os
import read_plate
import cv2
import LCD
import Servo

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def home():
    return render_template("admin.html")

@app.route('/detect')
def detect():
    return render_template("detect.html")

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        cmnd = request.form['cmnd']
        name = request.form['name']
        money = request.form['money']
        plate = request.form['plate']
        firestore.addToDB(cmnd, name, money, plate)
        response = app.response_class(
            status=200,
            response=json.dumps({'message': 'success'}),
            mimetype='application/json'
        )
        return response
    except Exception:
        return app.response_class(
            status=500,
            response=json.dumps({'message': 'Internal server error'}),
            mimetype='application/json'
        )

@app.route('/image')
def imageHandler():
    try:
        img_path = './static/images/demo.jpg';
        response = read_plate.get_plate(img_path)
        return jsonify(response=response)
    except Exception as e:
        print(e)
        return ''

@app.route('/users/plates', methods=['GET'])
def getAllPlates():
    try:
        data = firestore.getAllInfoPlate()
        response = app.response_class(
            status=200,
            response=json.dumps(data),
            mimetype='application/json'
        )
        return response
    except Exception:
        return app.response_class(
            status=500,
            response=json.dumps({'message': 'Internal server error'}),
            mimetype='application/json'
        )

@app.route('/users/info', methods=["POST"])
def updateMoney():
    try:
        plate = request.form["plate"]
        moneyBack = request.form["moneyBack"]
        firestore.updateDB(plate, moneyBack)
        response = app.response_class(
            status=200,
            response=json.dumps({"message": "success"}),
            mimetype='application/json'
        )
        return response
    except Exception:
        return app.response_class(
            status=500,
            response=json.dumps({'message': 'Internal server error'}),
            mimetype='application/json'
        )

@app.route('/camera/open', methods=['GET'])
def openCam():
    try:
        cam = cv2.VideoCapture(0) 
        ret, frame = cam.read()
        cv2.imwrite('./static/images/demo.jpg', frame)
        cam.release()
        cv2.destroyAllWindows()
        return app.response_class(
            status=200,
            response=json.dumps({'url': './static/images/demo.jpg'}),
            mimetype='application/json'
        )
    except Exception as identifier:
        print(identifier)
        return app.response_class(
            status=500,
            response=json.dumps({'message': 'Failed'}),
            mimetype='application/json'
        )


@app.route('/image/info', methods=['POST'])
def getPlateInfo():
    try:
        plate = request.form['plate']
        data = firestore.getInfoByPlate(plate)
        Servo.servo()
        LCD.LCD(plate)
        response = app.response_class(
            status=200,
            response=json.dumps(data),
            mimetype='application/json'
        )
        return response
    except Exception as identifier:
        LCD.LCD('Ban chua dang ki')
        print("get errors")
        print(identifier)
        return app.response_class(
            status=500,
            response=json.dumps({'message': 'Internal server error'}),
            mimetype='application/json'
        )


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0,pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = -1
    return response

if __name__ == "__main__":
    app.run(debug=True)