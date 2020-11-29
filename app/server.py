from flask import Flask, redirect
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