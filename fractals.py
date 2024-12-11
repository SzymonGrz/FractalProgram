from __future__ import division
import random
import ctypes
import numpy as np

def point_distance(a, p, distance: float):
    return (a[0] + (p[0] - a[0]) * (distance), a[1] + (p[1] - a[1])*(distance))

def list_of_colors(amount):
    colors = np.random.randint(0, 256, size=(amount, 3))
    return [tuple(color) for color in colors]

def chaos_game_fractal(iterations : int, distance : float, vertices : list):

    if len(vertices) == 0:
        return [],[]

    number_of_vertices = len(vertices)
    j = vertices[0]
    colors = list_of_colors(number_of_vertices)
    points = []
    point_colors = []

    for i in range(iterations):
        x = random.randint(0, number_of_vertices-1)
        j = point_distance(vertices[x], j, 1- distance)
        points.append(j)
        point_colors.append(colors[x])


    return points, point_colors

def chaos_game_fractal_restricted(iterations : int, jump : float, points: list, condition):

    if(condition == 1):
        points, colors = restricted_fractal(iterations, jump, points, lambda x, new_x : x == new_x)
    elif(condition == 2):
        points, colors = restricted_fractal(iterations, jump, points, lambda x, new_x : (new_x - x == -1) or (new_x == 3 and x == 0))
    elif(condition == 3):
        points, colors = restricted_fractal(iterations, jump, points, 
            lambda x, new_x : (new_x - x == 2) or (new_x - x == -2) or (new_x == 3 and x == 1))
        
    return points, colors

def restricted_fractal(iterations : int, jump : float, vertices: list, condition):
    
    if(len(vertices) == 0):
        return []
    
    number_of_vertices = len(vertices)

    j = vertices[0]
    x = random.randint(0, number_of_vertices-1)
    points = []
    color_list = list_of_colors(number_of_vertices)
    colors = []

    for i in range(iterations):
        new_x = random.randint(0, number_of_vertices-1)
        if(condition(x, new_x)):
            continue
        else:
            x = new_x
        j = point_distance(vertices[x], j, jump)
        points.append(j)
        colors.append(color_list[x])

    return points, colors

def affine_fractal(iterations, chances : list, x_transform : list, y_transform : list) :

    try:
        if(len(chances) == 0 ):
            return []

        points = []
        colors = list_of_colors(len(chances))
        point_colors = []

        point = (0, 0) #(random.uniform(0, 1), random.uniform(0, 1))

        for i in range(iterations):
            x = random.uniform(0, sum(chances))
            for j in range(0, len(chances)):
                suma = sum(chances[0 : j+1])
                if(x <= suma):
                    point = (x_transform[j][0] * point[0] + x_transform[j][1] * point[1] + x_transform[j][2],
                            y_transform[j][0] * point[0] + y_transform[j][1] * point[1] + y_transform[j][2])
                    points.append(point)
                    point_colors.append(colors[j])
                    break
        
        return points, point_colors
    except(ValueError, OverflowError):
        return [], []
    
def mandelbrot_c(width, height, iterations, xmin, xmax, ymin, ymax):

    lib = ctypes.CDLL('./mandelbrot.dll')

    lib.mandelbrot_set.argtypes= [
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), 
        ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double
    ]

    output = np.zeros((width*height), dtype=np.int32)
    lib.mandelbrot_set(width, height, iterations, output.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
                       xmin, xmax, ymin, ymax)
    n3 = output.reshape((height, width))

    return n3

def julia_c(c, width, height, iterations, xmin, xmax, ymin, ymax):
    lib = ctypes.CDLL('./mandelbrot.dll')

    lib.julia_set.argtypes = [ ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float,
            ctypes.POINTER(ctypes.c_int), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]

    output = np.zeros((width*height), dtype=np.int32)
    lib.julia_set(width, height, iterations, c.real, c.imag, output.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
                   xmin, xmax, ymin, ymax)
    n3 = output.reshape((height, width))
    
    return n3

def draw_image(points : list, colors: list = None, width = 500, height = 500) :

    points = np.array(points)

    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()

    if x_max == x_min:
        x_max += 1
    if y_max == y_min:
        y_max += 1

    if height == 0:
        height += 2
    if width == 0:
        width += 2

    if colors is None:
        image = np.zeros((height, width), dtype=np.uint8)
    else:
        image = np.zeros((height, width, 3), dtype=np.uint8)
        colors = np.array(colors)

    image_height = height-1
    image_width = width-1

    scale_x = image_width / (x_max - x_min)
    scale_y = image_height / (y_max - y_min)

    points[:, 0] = (points[:, 0] - x_min) * scale_x
    points[:, 1] = (points[:, 1] - y_min) * scale_y

    points = np.round(points).astype(int)

    valid_points = (points[:, 0] >= 0) & (points[:, 0] < image.shape[1]) & \
               (points[:, 1] >= 0) & (points[:, 1] < image.shape[0])
    points = points[valid_points]

    if colors is not None:
        colors = colors[valid_points]

    if colors is None:
        image[points[:, 1], points[:, 0]] = 255
    else:
        image[points[:, 1], points[:, 0]] = colors

    return image

def draw_vertices(vertices: list):

    im_width = 500
    im_height = 500

    min_x = min(vertices, key=lambda p: p[0])[0]
    max_x = max(vertices, key=lambda p: p[0])[0]

    min_y = min(vertices, key=lambda p: p[1])[1]
    max_y = max(vertices, key=lambda p: p[1])[1]

    if(min_x < 0):
        vertices = [[x - min_x, y] for [x, y] in vertices]
    if(min_y < 0):
        vertices = [[x, y - min_y] for [x, y] in vertices]

    
    width = abs(max_x - min_x)
    height = abs(max_y - min_y)

    try: 
        scale_x = im_width / width
    except(ZeroDivisionError):
        scale_x = 1
    try:
        scale_y = im_height / height
    except(ZeroDivisionError):
        scale_y = 1

    scaled_vertices = [(x * scale_x, y * scale_y) for x, y in vertices]
    return scaled_vertices


def l_system_fractal(axiom: str, rules: dict, iterations: int):

    route = axiom
    new_route = ""
    for j in range(iterations):
        l = len(route)
        for i in route:
            if i in rules:
                new_route += rules[i]
            else:
                new_route += i
        route = new_route
        new_route = ""

    return route

def rectangle_fractal(width: int, height : int, list_of_rectangles: dict, iterations : int, depth: int, color_level: int):

    main_rectangle = np.array([[0, 0], [0, height],[width, height] ,[width, 0]])
    src = np.array(main_rectangle)
    src = np.hstack([src, np.ones((src.shape[0], 1))])

    function_list = []

    if(len(list_of_rectangles) > 0):
        for rect in list_of_rectangles.values():
            dst_i = [rect[i:i + 2] for i in range(0, len(rect), 2)]
            dst = np.array(dst_i)
            transformation_matrix, _, _, _ = np.linalg.lstsq(src, dst, rcond=None)
            a, b = transformation_matrix[0]
            c, d = transformation_matrix[1]
            e, f = transformation_matrix[2]
            function_list.append([a, b, c, d, e, f])

    points = np.column_stack((
        np.random.uniform(0, width, iterations),
        np.random.uniform(0, height, iterations)
    ))

    function_array = np.array(function_list)
    color_list = list_of_colors(len(function_list))
    color_array = np.array(color_list)

    colors = np.empty(3)
    for j in range(depth):

        func_indices = np.random.randint(0, len(function_array), iterations)

        selected_functions = function_array[func_indices]
        a = selected_functions[:, 0]
        b = selected_functions[:, 1]
        c = selected_functions[:, 2]
        d = selected_functions[:, 3]
        e = selected_functions[:, 4]
        f = selected_functions[:, 5]

        new_x = a * points[:, 0] + b * points[:, 1] + e
        new_y = height - (c * points[:, 0] + d * points[:, 1] + f)

        points = np.column_stack((new_x, new_y))

        if j == depth - color_level:
            colors = color_array[func_indices]

    return points.tolist(), colors.tolist()


