import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.figure import Figure 
import math
from PIL import Image

def mandelbrot():

    x,y=np.ogrid[-2:1:5000j,-1.5:1.5:5000j]

    z  = 0
    c  = x + y * 1j

    iterations  = 20
    
    for g in range(iterations):
        z=z**2 + c

    mask = np.abs(z) < 2

    # img = Image.fromarray(mask, 'L')

    plt.imshow(mask.T,extent=[-2,1,-1.5,1.5])

    # plt.gray()
    plt.show()
    # img.show()

def mandelbrot_colored(size, iterations) :

    y,x=np.ogrid[-2:2:size *1j,-2:2:size*1j]

    z_array  = np.array(size * size)
    c  = x + y * 1j

    max_iterations = iterations

    iterations_until_divergence = max_iterations + np.zeros(c.shape)

    for h in range(size):
        for w in range(size):
            z = 0
            for i in range(max_iterations):
                z = z ** 2 + c[h][w]
                if z * np.conj(z) > 4:
                    iterations_until_divergence[h][w] = i
                    break
    plt.imshow(iterations_until_divergence, cmap=cm.gnuplot2)
    plt.show()
    
                


def mandelbrot2():
    x = -2
    y = -2

    points_x = []
    points_y = []

    epsilon = 0.001
    maxiterations = 40

    while x < 2:
        while y < 2:
            z_real = 0
            z_imag = 0
            c_real = x
            c_imag = y
            # iterations = 0
            for i in range(maxiterations):
                z_real2 = z_real*z_real - z_imag*z_imag + c_real
                z_imag = 2 * z_real* z_imag + c_imag
                z_real = z_real2
                # iterations += 1 
            if(z_real*z_real+z_imag*z_imag < 4):
                points_x.append(c_real)
                points_y.append(c_imag)
            y += epsilon
        x += epsilon
        y = -2

    plt.scatter(points_x, points_y, s=0.5)
    plt.show()


def julia_set2(c):

    x = -2
    y = -2

    points_x = []
    points_y = []

    epsilon = 0.001
    maxiterations = 10

    while y < 2:
        while x < 2:
            z = x + y * 1j
            iterations = 0
            while abs(z) < 2 and iterations <= maxiterations:
                z=z**2 + c
                iterations += 1 
            if(abs(z) < 2):
                points_x.append(x)
                points_y.append(y)    
            x += epsilon
        y += epsilon
        x = -2

    plt.scatter(points_x, points_y, s=0.5)
    plt.show()

def julia_set3(c, size, iterations):
    
    y,x=np.ogrid[-1.4:1.4:size*1j,-1.4:1.4:size*1j]

    z_array  = x + y * 1j

    max_iterations  = iterations

    iterations_until_divergence = max_iterations + np.zeros(z_array.shape)
    not_already_diverged = iterations_until_divergence < 10000
    diverged_in_past = iterations_until_divergence > 10000

    for i in range(max_iterations):
        z_array = z_array**2 + c
        
        z_size_array = z_array * np.conj(z_array)
        diverging = z_size_array > 4

        diverging_now = diverging & not_already_diverged
        iterations_until_divergence[diverging_now]  = i
        not_already_diverged = np.invert(diverging_now) & not_already_diverged

        diverged_in_past = diverged_in_past | diverging_now
        z_array[diverged_in_past] = 0

    plt.imshow(iterations_until_divergence, cmap=cm.twilight_shifted)

    # plt.gray()
    plt.show()

def julia_set(c):

    x_res, y_res = 300, 300
    xmin, xmax = -1.5, 1.5
    width = xmax - xmin
    ymin, ymax = -1.5, 1.5
    height = ymax - ymin

    z_abs_max = 10
    max_iter = 1000

    julia = np.zeros((x_res, y_res))

    # Loop over each pixel
    for ix in range(x_res):
        for iy in range(y_res):
            # Map pixel position to a point in the complex plane
            z = complex(ix / x_res * width + xmin,
                        iy / y_res * height + ymin)
            # Iterate
            iteration = 0
            while abs(z) <= z_abs_max and iteration < max_iter:
                z = z**2 + c
                iteration += 1
            iteration_ratio = iteration / max_iter    
            # Set the pixel value to be equal to the iteration_ratio
            julia[ix, iy] = iteration_ratio

    # Plot the array using matplotlib's imshow
    fig, ax = plt.subplots()
    ax.imshow(julia, interpolation='nearest', cmap=cm.gnuplot2)
    plt.axis('off')
    plt.show()


# def sierpinski(ax, levels=4, x=0, y=0, size=1):
#     if levels == 0:
#         ax.add_patch(plt.Rectangle((x, y), size, size, color='navy'))
#     else:
#         size3 = size / 3
#         for i in range(3):
#             for j in range(3):
#                 if i != 1 or j != 1:
#                     draw_fractal(ax, levels - 1, x + i * size3, y + j * size3, size3)


def julia_set_main(c, size):
    y,x=np.ogrid[-2:2:size*1j,-2:2:size*1j]

    z  = x + y * 1j

    iterations = 20

    for g in range(iterations):
        z=z**2 + c

    mask = abs(z) < 2

    plt.imshow(mask.T,extent=[-2,2,-2,2], cmap = cm.gnuplot2)
    plt.show()





def sierpinski_triangle_ifs(iterations):
    print("abcd")

    a = (0, 0)
    b = (10, 0)
    c = (5, 5*math.sqrt(3))
    
    points= [a, b, c]

    if(iterations == 1):
        points.append(half_point(points[0], points[1]))
        points.append(half_point(points[1], points[2]))
        points.append(half_point(points[2], points[0]))
    else:
        points.append(half_point(points[0], points[1]))
        points.append(half_point(points[1], points[2]))
        points.append(half_point(points[2], points[0]))

        iter = 3

        for j in range(iterations):
            for i in range(iter, len(points)):
                points.append(half_point(points[0], points[i]))
                points.append(half_point(points[1], points[i]))
                points.append(half_point(points[2], points[i]))
            iter = 3**j


    points_x = []
    points_y = []

    for p in points:
        points_x.append(p[0])
        points_y.append(p[1])

    plt.scatter(points_x, points_y)
    plt.show()
    return

# def point_on_triangle(pt1, pt2, pt3):
#     """
#     Random point on the triangle with vertices pt1, pt2 and pt3.
#     """
#     x, y = random.random(), random.random()
#     q = abs(x - y)
#     s, t, u = q, 0.5 * (x + y - q), 1 - 0.5 * (q + x + y)
#     return (
#         s * pt1[0] + t * pt2[0] + u * pt3[0],
#         s * pt1[1] + t * pt2[1] + u * pt3[1],
#     )

def point_on_triangle(pt1, pt2, pt3):
    """
    Random point on the triangle with vertices pt1, pt2 and pt3.
    """
    x, y = random.uniform(0, 1), random.uniform(0, 1)
    p = []
    p.append((1 - math.sqrt(x)) * pt1[0] + (math.sqrt(x) * (1 - y)) * pt2[0] + (math.sqrt(x) * y) * pt3[0])
    p.append(1 - math.sqrt(x) * pt1[1] + (math.sqrt(x) * (1 - y)) * pt2[1] + (math.sqrt(x) * y) * pt3[1])
    return p



def sierpinski_triangle_chaos(iterations: int):

    a = (0, 0)
    b = (10, 0)
    c = (5, 5*math.sqrt(3))
    
    points= [a, b, c]

    d = point_on_triangle(a,b,c)
    
    for i in range(iterations):
        x = random.randint(0, 2)
        d = point_distance(points[x], d, 0.5)
        points.append(d)

    points_x = []
    points_y = []

    for p in points:
        points_x.append(p[0])
        points_y.append(p[1])

    plt.scatter(points_x, points_y)
    plt.show()

def sierpinski_square_chaos(iterations):
    a = (0, 0)
    b = (12, 0)
    c = (12, 12)
    d = (0, 12)
    e = (0, 6)
    f = (6, 0)
    g = (12, 6)
    h = (6, 12)
    
    points= [a, b, c, d, e, f, g, h]

    j = (random.uniform(0, 12), random.uniform(0, 12))
    
    for i in range(iterations):
        x = random.randint(0, 7)
        j = two_thirds_point(points[x], j)
        points.append(j)

    points_x = []
    points_y = []

    for p in points:
        points_x.append(p[0])
        points_y.append(p[1])

    plt.scatter(points_x, points_y)
    plt.show()

def pieciokat_chaos(iterations):

    #punkty poprawić
    a = (0, 1)
    b = (-(math.sin(2*math.pi/5)), math.cos(2*math.pi/5))
    c = (-(math.sin(4*math.pi/5)), -math.cos(math.pi/5))
    d = (math.sin(4*math.pi/5), -math.cos(math.pi/5))
    e = (math.sin(2*math.pi/5), math.cos(2*math.pi/5))

    points = [a, b, c, d, e]

    j = (random.uniform(0, 1), random.uniform(0, 1))
    
    for i in range(iterations):
        x = random.randint(0, 4)
        j = point_distance(points[x], j, 1- 0.618)
        points.append(j)

    points_x = []
    points_y = []

    for p in points:
        points_x.append(p[0])
        points_y.append(p[1])

    plt.scatter(points_x, points_y)
    plt.show()

################################################################################


def chaos_game_fractal(iterations : int, distance : float, points : list):

    if len(points) == 0:
        return []

    number_of_vertices = len(points)
    j = points[0]

    for i in range(iterations):
        x = random.randint(0, number_of_vertices-1)
        j = point_distance(points[x], j, 1- distance)
        points.append(j)

    return points

    # points_x = []
    # points_y = []

    # for p in points:
    #     points_x.append(p[0])
    #     points_y.append(p[1])

    #ANIMATION
    # fig = plt.figure()
    # plt.xlim(-1, 12)
    # plt.ylim(-1, 12)
    # graph, = plt.plot([], [], "o")

    # def animate(i):
    #     graph.set_data(points_x[:i+1], points_y[:i+1])
    #     return graph
    # ani = FuncAnimation(fig, animate, frames=iterations, interval=1)

    # plt.scatter(points_x, points_y, s=0.05, marker="d")
    
    # plt.show()

def chaos_game_fractal_restricted(iterations : int, jump : float, points: list, condition):


    #TODO poprawić. Zamienić x i new_x na punkty
    if(condition == 1):
        points = restricted_fractal(iterations, jump, points, lambda point_a, point_b : point_a == point_b)
    elif(condition == 2):
        points = restricted_fractal(iterations, jump, points, lambda x, new_x : (new_x - x == -1) or (new_x == 3 and x == 0))
    elif(condition == 3):
        points = restricted_fractal(iterations, jump, points, 
            lambda x, new_x : (new_x - x == 2) or (new_x - x == -2) or (new_x == 3 and x == 1))
        
    return points

    # points_x = []
    # points_y = []

    # for p in points:
    #     points_x.append(p[0])
    #     points_y.append(p[1])

    # plt.scatter(points_x, points_y, s=0.5, )
    # plt.show()

def restricted_fractal(iterations : int, jump : float, points: list, condition):
    
    if(len(points) == 0):
        return []
    
    number_of_vertices = len(points)


    # was_the_same : bool = False

    j = points[0]
    x = random.randint(0, number_of_vertices-1)

    for i in range(iterations):
        new_x = random.randint(0, number_of_vertices-1)
        if(condition(points[x], points[new_x])):
            continue
        else:
            x = new_x
        j = point_distance(points[x], j, jump)
        points.append(j)

    return points


        

def half_point(a, p):
    return ((a[0] + p[0])/2, (a[1]+p[1])/2)

def two_thirds_point(a, p):
    return (a[0] + (p[0] - a[0]) * (1/3), a[1] + (p[1] - a[1])*(1/3))

def point_distance(a, p, distance: float):
    return (a[0] + (p[0] - a[0]) * (distance), a[1] + (p[1] - a[1])*(distance))

def barnsley_fern(iterations: int):

    points = []
    x: float

    point = (random.uniform(0, 3), random.uniform(0, 10))

    for i in range(iterations):
        x = random.randint(1, 100)
        if x <= 1:
            point = (0, 0.16 * point[1])
        elif x <= 8:
            point = (0.2 * point[0] - 0.26 * point[1], 0.23 * point[0] + 0.22* point[1] + 1.6) 
        elif x <= 15:
            point = (-0.15 * point[0] + 0.28 * point[1], 0.26 * point[0] + 0.24 * point[1] + 0.44)
        else:
            point = (0.85 * point[0] + 0.04 * point[1], -0.04 * point[0] + 0.85 * point[1] + 1.6)
        points.append(point)
        
    
    return points
    
    #plt.show()

def fractal(iterations, chances : list, x_transform : list, y_transform : list) :

    points = []

    point = (random.uniform(0, 1), random.uniform(0, 1))

    for i in range(iterations):
        x = random.uniform(0, 100)
        for j in range(0, len(chances)):
            suma = sum(chances[0 : j+1])
            if(x <= suma):
                point = (x_transform[j][0] * point[0] + x_transform[j][1] * point[1] + x_transform[j][2],
                         y_transform[j][0] * point[0] + y_transform[j][1] * point[1] + y_transform[j][2])
                points.append(point)
                break

    points_x = []
    points_y = []

    for p in points:
        points_x.append(p[0])
        points_y.append(p[1])

    plt.scatter(points_x, points_y, s = 0.5)
    plt.show()

    

def main():
    print("main")
    
    # julia_set(c = -0.1 - 0.65j)
    #mandelbrot()
    #mandelbrot2()
    # fig, ax = plt.subplots()
    # ax.set_aspect(1)
    # ax.axis('off')
    # sierpinski(ax)
    # plt.show()
    #sierpinski_triangle_ifs(10)
    #sierpinski_triangle_chaos(1000000)
    #sierpinski_square_chaos(1000000)
    
    #pieciokat_chaos(1000000)

    #paproć Bernsley'a
    #paproc(1000000)
    
    #trójkąt sierpińskiego
    # chaos_game_fractal(10000, 0.5,  [(0, 0),(10, 0),(5, 5*math.sqrt(3))])
    # chaos_game_fractal(10000, 0.5,  [(0, 0),(10, 0),(5, 5*math.sqrt(3))])

    #dywan sierpińskiego
    #chaos_game_fractal(1000000, (2/3), [(0, 0), (12, 0), (12, 12), (0, 12), (0, 6), (6, 0), (12, 6), (6, 12)])

    #pięciokąt
    # chaos_game_fractal(1000000, 0.618, [(0, 1),
    # (-(math.sin(2*math.pi/5)), math.cos(2*math.pi/5)),
    # (-(math.sin(4*math.pi/5)), -math.cos(math.pi/5)),
    # (math.sin(4*math.pi/5), -math.cos(math.pi/5)),
    # (math.sin(2*math.pi/5), math.cos(2*math.pi/5))])

    #fraktal Viscek'a
    #chaos_game_fractal(1000000, (2/3), [(0, 0),(12, 0), (12, 12), (0, 12), (6, 6)])

    #chaos_game_fractal_restricted(1000000, 0.5, [(0, 0), (10, 0), (10, 10), (0, 10)], 3)
    
    # restricted_fractal(1000000, 0.5, [(0, 0), (10, 0), (10, 10), (0, 10)], 
    #                 lambda x, new_x : (new_x - x == 2) or (new_x - x == -2) or (new_x == 3 and x == 1))

    #pięciokąt wariacja
    #if new_x == x:

    #trójkąt obrócony w kwadracie
    #if (old_x+x) / 2 == 1:

    #czworokąt bez sąsiednich wierzchołków

    # was_the_same : bool = False

    # j = (random.uniform(0, 1), random.uniform(0, 1))
    
    # for i in range(iterations):
    #     new_x = random.randint(0, 3)
    #     if(was_the_same):
    #         if(new_x - x == 1) or (new_x - x == -1) or (new_x == 3 and x == 0) or (new_x ==0 and x == 3):
    #             continue
    #     if new_x == x:
    #         was_the_same = True
    #     else:
    #         was_the_same = False
    #         x = new_x

    #pięciokąt bez sąsiednich wierzchołków

    # was_the_same : bool = False

    # j = (random.uniform(0, 1), random.uniform(0, 1))
    
    # for i in range(iterations):
    #     new_x = random.randint(0, 4)
    #     if(was_the_same):
    #         if(new_x - x == 1) or (new_x - x == -1) or (new_x == 4 and x == 0) or (new_x ==0 and x == 4):
    #             continue
    #     if new_x == x:
    #         was_the_same = True
    #     else:
    #         was_the_same = False
    #         x = new_x

    #t-kwadrat
    #if(new_x - x == 2) or (new_x - x == -2) or (new_x == 3 and x == 1):

    #kwadrat bez poprzednich wierzchołków
    # if(new_x - x == -1) or (new_x == 3 and x == 0):

    #kwadrat bez tego samego wierzchołka
    #if(new_x == x)

    #kwadrat
    #chaos_game_fractal(1000000, 0.55, [(0,0), (0, 12) , (6, 6), (-6, 6)])

    # fractal(100000, chances = [78.747, 21.253], x_transform = [[0.824, 0.281, -0.1],[0.088, 0.281, 0.534]],
    #          y_transform=[[-0.212, 0.864, 0.095],[-0.464, -0.378, 1.041]])
    
    # fractal(100000, chances = [1, 7, 7, 85], x_transform=[[0,0,0], [0.2, -0.26, 0], [-0.15, 0.28, 0], [0.85, 0.04,0]],
    #         y_transform=[[0, 0.16, 0],[0.23, 0.22, 1.6], [0.26, 0.24, 0.44], [-0.04, 0.85, 1.6]])


    #julia_set(c = -0.1 - 0.65j)
    # julia_set2(c = 0.285 + 0.01j)
    julia_set3(c = -0.4 + 0.6j, size=4000, iterations = 20)
    # mandelbrot2()
    # mandelbrot_colored(1000, 70)
    # mandelbrot()
    # julia_set_main(c = 0.285 + 0.01j, size=5000)




if __name__ == '__main__':
    main()