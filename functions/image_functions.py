from __future__ import division
from tkinter import filedialog
from matplotlib.axes import Axes
from PIL import Image

import functions.fractals as fractals

def plot(plot1 : Axes, canvas, points : list = None, vertices : list = None, colors : list = None, scaled = False):

    [collection.remove() for collection in plot1.collections]
    [image.remove() for image in plot1.images]

    if(vertices is not None and len(vertices) != 0):
        plot1.scatter(*zip(*vertices), c="y")
    if(points is not None and len(points) != 0):

        xmin = min(points, key=lambda p: p[0])[0]
        ymin = min(points, key=lambda p: p[1])[1]
        xmax = max(points, key=lambda p: p[0])[0]
        ymax = max(points, key=lambda p: p[1])[1]

        if scaled:
            img = fractals.draw_image(points = points, colors=colors,  width = int(xmax-xmin), height = int(ymax-ymin))
        else:
            img = fractals.draw_image(points, colors)
    
        image=Image.fromarray(img)    

        if colors is None:
            height, width = img.shape
        else:
            height, width, _ = img.shape
            
        xmax = width + xmin
        ymax = height + ymin

        plot1.imshow(image, cmap='gist_grey', origin = 'lower', extent=(xmin, xmax, ymin, ymax))

    canvas.draw()

def save_image(subplot : Axes):
    file_path = filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

    subplot.figure.savefig(file_path, dpi = 300)