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
    pop_cols, vis_cols, avg_vis_cols = controller.get_home_page_data()[0]
    pop, vis, avg_vis = controller.get_home_page_data()[1]
    return render_template('data.html', pop_cols=pop_cols, pop=pop, vis_cols=vis_cols, vis=vis, avg_vis_cols=avg_vis_cols, avg_vis=avg_vis)

@app.route("/populate")
def populate():
    controller.populate()
    return ("nothing")