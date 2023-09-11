# this file serves as a real world example of python. Pandas and numpy are used to analyze data and matplotlib to plot.
# file consists of 2 columns per sample: wavelength and intensity. an un-plotted blank is the first column.
# goal is to average the three spectra, smooth them, plot them all together, and plot their lambda maxes
# import statements
import pandas as pd  # pandas for data analysis
import matplotlib.pyplot as plt  # pyplot for data visualization
from environment_scripts import colorpicker, imagesaver  # premade environment scripts
from matplotlib.ticker import MultipleLocator  # needed for ticks
import scipy as sp  # smoothing and linear regression



# set up classes and functions! This will make everything so much easier
class lambdaMaxData:  # sets up an object storing all the lambda maxes for linear regression and R^2 cal curve purposes
    def __init__(self, ph, value):
        self.ph = ph
        self.value = value

    # does linear regression on the line,
    def regression(self, ax):
        linreg = sp.stats.linregress(self.ph, self.value)  # makes a linear regression object

        def lin(x):
            return (linreg[0] * x) + linreg[1]  # sets eqn of line
        plotlist = [lin(x) for x in self.ph]  # makes list of linear regressed points
        ax.plot(self.ph, plotlist, label="Linreg", color="seagreen", alpha=0.5)  # plots the line making it transparent
        ax.plot(self.ph, self.value, label="Actual values", marker="o", color="navy")
        ax.text(11, 0, f"R²={round(linreg[2] ** 2, 3)}", ha="right", va="bottom")  # plots R2


def threeColumnAverage(cols):  # averages 3 columns: made function because we will do this 3x
    if len(cols) != 3:
        raise Exception("Make sure you put 3 columns in!")
    else:
        col1 = cols[0].to_numpy().astype(float)  # defines columns as numpy arrays so we can average them
        col2 = cols[1].to_numpy().astype(float)  # .to_numpy() turns to numpy array, .astype(float) changes type
        col3 = cols[2].to_numpy().astype(float)  # from string to float. Why was it a string? IDK!
    # does the averaging and smoothing in the return statement in order to save memory
    return sp.ndimage.gaussian_filter1d(((col1 + col2 + col3) / 3), axis=0, sigma=1).tolist()


labelfont = {"fontsize": 12}
labels = ["Free FITC", "FITC pH 5", "FITC pH 6", "FITC pH 7",
          "FITC pH 8", "FITC pH 9", "FITC pH 10", "FITC pH 11"]  # labels for graph
pH_list = [5, 6, 7, 8, 9, 10, 11]  # pHs
file = 'FITC-BSA calibration curve pH.csv'  # pathway of file
df = pd.read_csv(file, index_col=0)  # data frame object initialized as a pandas read CSV file function.
# Index is wavelength
droplist = [str(col) for col in df.columns if "Unnamed:" not in str(col)]  # returns label of every non-intensity col
droplist.extend(["Unnamed: 1", "Unnamed: 50"])  # adds in the blank and the final column of all nulls
df.drop(labels=droplist, axis=1, inplace=True)  # removes all columns which are not intensity values
df = df.iloc[1:102]  # removes instrument conditions at the end
col_iter = 1  # sets up a counter to do something every 3 times
intensitylist = []  # creates new list to store allthe intensities
for column in df.columns:  # iterates over columns and averages every 3
    if col_iter % 3 == 0:  # if the iteration is divisible by 3:
        intensitylist.append(threeColumnAverage([df[df.columns[col_iter-3]],
                                                 df[df.columns[col_iter-2]], df[df.columns[col_iter-1]]]))
    col_iter += 1
colors = colorpicker(intensitylist, "plasma")  # sets up colormap using envscripts
fig = plt.figure(constrained_layout=True)  # produces figure object
g = fig.add_gridspec(3, 2) # creates a grid  with 3 rows and 2 columns
ax1 = fig.add_subplot(g[0:2, :])  # adds main plot to rows 1,2, and all columns
ax2 = fig.add_subplot(g[2, :])  # adds sub plot
lmax = []
for n, ints in enumerate(intensitylist):  # iterates over an enumerate object spitting out (number, item)
    ax1.plot(df.index.astype(float), ints, color=colors[n], label=labels[n])  # plots x, y, labels and colors
    lmax.append(ints[df.index.astype(float).tolist().index(518.9299927)])  # adds index at lmax of 519 to the list
lmax = lmax[1::]
# adds all aspects of matplotlib graph to ax1
ax1.legend(loc="upper right", frameon=False)  # adds legend
ax1.set_xlim(500, 600)  # sets x limits
ax1.set_box_aspect(0.5)  # sets the aspect ratio of the graph
ax1.set_xlabel("Wavelength (nm)", **labelfont)  # adds x label
ax1.set_ylabel("Fluorescence (A.U.)", **labelfont)  # adds y label
ax1.set_yticks([0, 200, 400, 600])  # adds ticks
# minor ticks added using multiple locator object
ax1.yaxis.set_minor_locator(MultipleLocator(100))
ax1.xaxis.set_minor_locator(MultipleLocator(10))
# defines a lmax object to then undergo regression
ld = lambdaMaxData(pH_list, lmax)
ld.regression(ax2)
# more label stuff
ax2.legend(loc="upper left")
ax2.set_xlim(4.8, 11.2)
ax2.set_box_aspect(0.33)
ax2.set_xlabel("pH", **labelfont)
ax2.set_ylabel("Fluorescence (A.U.)", **labelfont)
imagesaver(save=True, fig=fig, image_title="pluh")  # premade save feature
fig.show()
