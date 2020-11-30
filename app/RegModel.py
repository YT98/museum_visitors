from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class RegModel():
    def __init__(self, controller):
        self.model = LinearRegression()
        self.image_path = "/tmp/plot.jpg"
        self.load_data(controller)
        self.train()

    def load_data(self, controller):
        training_data = controller.get_training_data()
        pop_ls = []
        avg_vis_ls = []
        for row in training_data:
            pop_ls.append(row[0])
            avg_vis_ls.append(row[1])
        pop_ls = np.array(pop_ls).reshape(-1, 1)
        avg_vis_ls = np.array(avg_vis_ls).reshape(-1, 1)
        self.x = pop_ls
        self.y = avg_vis_ls
        
    def train(self):
        x = self.x
        self.model.fit(self.x, self.y)

    def predict(self, population):
        reg_pop = np.array(population).reshape(-1, 1)
        pred = self.model.predict(reg_pop)
        pred = np.round(pred, decimals=0)
        return pred

    def get_pearson(self):
        return np.round(np.corrcoef(self.x, self.y)[0][1], decimals=2)

    def get_rsquared(self):
        return np.round(self.model.score(self.x, self.y), decimals=2)

    def save_plot(self):
        # Init figure and axes
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        # Plot data points and Linear Regression line
        ax.scatter(self.x, self.y, color='b')
        ax.plot(self.x, self.model.predict(self.x), color='r', linewidth=3)
        # Format plot
        ax.set_yticks(np.arange(self.y.min(), self.y.max(), 1000000))
        ax.set_xticks(np.arange(self.x.min(), self.x.max(), 2000000))
        ax.set_xlabel("Population")
        ax.set_ylabel("Average Visitors")
        # Add r-squared and pearson coefficient text box
        textstr = "R^2 = {} \n Pearson = {}".format(self.get_rsquared(), self.get_pearson())
        props = dict(boxstyle='square', facecolor='white', alpha=0.5)
        ax.text(0.90, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                horizontalalignment='right', verticalalignment='top', bbox=props)
        # Save figure
        plt.savefig(self.image_path, bbox_inches='tight')