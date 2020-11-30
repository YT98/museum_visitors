from flask import Flask, redirect, request
from flask import render_template

from .Controller import Controller
from .RegModel import RegModel

class State:
    def __init__(self):
        self.controller = Controller()
        self.reg_model = None
        self.has_model = False
        self.pred = None

    def set_reg_model(self, model):
        self.reg_model = model
        self.has_model = True

    def set_pred(self, pred):
        self.pred = "{:,}".format(pred)


state = State()
app = Flask(
        __name__,
        static_url_path='', 
        static_folder='/tmp'
    )


@app.route("/")
def home():
    return redirect("/data")

@app.route("/data")
def data():
    data_obj = state.controller.get_data_page_data()
    return render_template('data.html', pop=data_obj["pop"], vis=data_obj["vis"], avg_vis=data_obj["avg_vis"])

@app.route("/populate")
def populate():
    state.controller.populate()
    return ("nothing")

@app.route("/update-population")
def update_population():
    city_id = request.args.get("city_id")
    population = request.args.get("population")
    state.controller.update_population(city_id, population)
    return ("nothing")

@app.route("/linear-regression")
def linear_regression():
    return render_template('linear-regression.html', has_model=state.has_model, pred=state.pred)

@app.route("/linear-regression/create-model")
def create_model():
    reg_model = RegModel(state.controller)
    reg_model.save_plot()
    state.set_reg_model(reg_model)
    return ("nothing")

@app.route("/linear-regression/predict")
def predict():
    pop = int(request.args.get("population"))
    pred = state.reg_model.predict(pop)
    state.set_pred(pred[0][0])
    return ("nothing")