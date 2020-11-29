from flask import Flask, redirect, request
from flask import render_template

# from .RegModel import RegModel
# reg_model = RegModel()

from .Controller import Controller

app = Flask(__name__)
controller = Controller()

@app.route("/")
def home():
    return redirect("/data")

@app.route("/data")
def data():
    data_obj = controller.get_data_page_data()
    return render_template('data.html', pop=data_obj["pop"], vis=data_obj["vis"], avg_vis=data_obj["avg_vis"])

@app.route("/populate")
def populate():
    controller.populate()
    return ("nothing")

@app.route("/update-population")
def update_population():
    city_id = request.args.get("city_id")
    population = request.args.get("population")
    controller.update_population(city_id, population)
    return ("nothing")

@app.route("/linear-regression")
def linear_regression():
    return render_template('linear-regression.html')