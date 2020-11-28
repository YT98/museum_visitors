# from sklearn.linear_model import LinearRegression
import pandas as pd

class RegModel():
    def __init__(self, db):
        # self.model = LinearRegression.model
        self.db = db
        self.load_data()

    def load_data(self):
        training_data = self.db.get_training_data()
        pop_ls = []
        avg_vis_ls = []
        for row in training_data:
            pop_ls.append(row[0])
            avg_vis_ls.append(row[1])
        self.pop_ls = pop_ls
        self.avg_vis_ls = avg_vis_ls
        
        