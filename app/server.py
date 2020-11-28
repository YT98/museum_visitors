from flask import Flask, redirect
from flask import render_template

from .Db import Db
# from .RegModel import RegModel
from .populate_db import populate_db

app = Flask(__name__)
db = Db()
# reg_model = RegModel()

@app.route("/")
def home():
    return redirect("/data")

@app.route("/data")
def data():
    pop_cols, vis_cols, avg_vis_cols = db.get_home_page_data()[0]
    pop, vis, avg_vis = db.get_home_page_data()[1]
    return render_template('data.html', pop_cols=pop_cols, pop=pop, vis_cols=vis_cols, vis=vis, avg_vis_cols=avg_vis_cols, avg_vis=avg_vis)

@app.route("/populate")
def populate():
    print("Populating database...")
    populate_db(db)
    return ("nothing")