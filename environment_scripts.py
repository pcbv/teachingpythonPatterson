# These are a collection of scripts required for other needs. I have added these to the repository so you may use
# them in your own scripts.
# created by Ben Rose of the Patterson lab in September 2023


# import statements: these are other peoples' codes which are used to
import matplotlib.pyplot as plt
import numpy as np


# this first script takes as input two variables: the data you want to plot, and the colormap you want to use
# the colormap is from mpls colormaps. https://matplotlib.org/stable/tutorials/colors/colormaps.html
def colorpicker(data, cm):
    try:  # try loop checks if there are no errors.
        if cm == "viridis":  # checks for the specific colormap. users will have to implement colormaps as strings
            colors = plt.cm.viridis(np.linspace(0, 0.8, len(data)))  # linspace samples colormap len(data) number of
            # times
        elif cm == "cividis":
            colors = plt.cm.cividis(np.linspace(0, 0.8, len(data)))
        elif cm == "plasma":
            colors = plt.cm.plasma(np.linspace(0, 0.8, len(data)))
        elif cm == "blues":
            colors = plt.cm.Blues(np.linspace(1, 0.2, len(data)))
        else:  # this is an error that is raised if the user does not enter one of these four colormaps
            raise TypeError("Incorrect color map entered! Enter either plasma, cividis, or viridis!!")
        return colors  # returns the colormap, which is essentially a list of RGB values
    except TypeError:
        return None


# shorthand for saving an image via code instead of clicks. this will be enabled when the user sets the 'save' var to
# true. last variable is a preset pathway
def imagesaver(save, fig, image_title, image_pathway="/Users/benrose/Desktop"):
    if type(fig) == plt.Figure:  # checks that the operation can be done
        if save is True:
            fig.savefig(image_pathway + '/' + image_title + '.png',
                        dpi=300,
                        bbox_inches="tight",
                        pad_inches=0.1)
    else:  # if not, raises error that terminates the process
        raise TypeError("Remember, save must be a string, and the figure must be a matplotlib defined figure object.")