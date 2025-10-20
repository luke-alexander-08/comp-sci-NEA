import numpy as np
import matplotlib.pyplot as plt
import time
start = time.time()
SEED = 0

gradients = np.array([(1, 0), (0.707, 0.707), (0, 1), (-0.707, 0.707), (-1, 0), (-0.707, -0.707), (0, -1), (0.707, -0.707)]) # 8 pseudorandom gradient vectors which will be assigned to each point


def fade(n):
    return 6*n**5 - 15*n**4 + 10*n**3

def perlin(width, height, octaves =1, frequency=1, amplitude=1, persistence=0.5, lacunarity=2.0, SEED=0):
    perm_table = np.arange(0, 255, dtype=int) # start, stop, data type. returns nums from 0-255
    np.random.seed = SEED
    np.random.shuffle(perm_table)
    perm_table = np.stack([perm_table, perm_table]).flatten() # duplicate elements of the table, then turns it one dimensional using flatten(). apparently therefore making it more efficient to perform operations, as no need for modulo fucntion. 

    total_noise = np.zeros((width, height))
    max_amplitude = 0   
    for _ in range(octaves):
        print(f"Octave: {_}")
        x, y = np.mgrid[0:width, 0:height]
        scaled_x = x / width * frequency
        scaled_y = y/ height * frequency 

        xi = scaled_x.astype(int) # cast numpy array to integer parts. 
        xf = scaled_x - xi # get fraction parts

        yi = scaled_y.astype(int) # cast numpy array to integer parts. 
        yf = scaled_y - yi # get fraction parts

        # find hash values for each corner and then find gradients

        h_ul = perm_table[perm_table[xi & 255] + (yi&255)] # using AND operations to ensure all elements are held within the array. Array was doubled earlier, so that modulo isn't used now - instead simple AND is sure to be constrained to the set. 
        h_ur = perm_table[perm_table[(xi+1) & 255] + (yi&255)]
        h_bl = perm_table[perm_table[xi & 255] + ((yi+1)&255)]
        h_br = perm_table[perm_table[(xi+1) & 255] + ((yi+1)&255)]

        g_ul = gradients[h_ul % 8]
        g_ur = gradients[h_ur % 8]
        g_bl = gradients[h_bl % 8]
        g_br = gradients[h_br % 8]

        #distance vectors
        d_ul = np.stack([xf,yf], axis=-1) # stacking fractional parts. visualised as a grid of 2 deep cubes, access fractional parts via index. 
        d_ur = np.stack([xf-1, yf], axis=-1) # x direction is negative, relative distance
        d_bl = np.stack([xf, yf-1], axis=-1)
        d_br = np.stack([xf-1, yf-1], axis=-1)

        # dot products

        dot_ul = np.sum(d_ul * g_ul, axis=-1)  # multiply x,y components by its vector. and then sum through axis=-1, adding those "cubes" from earlier. 
        dot_ur = np.sum(d_ur * g_ur, axis=-1) 
        dot_bl = np.sum(d_bl * g_bl, axis=-1) 
        dot_br = np.sum(d_br * g_br, axis=-1) 
        
        #interpolation
        u = fade(xf)
        v = fade(yf)

        #lerp a+t*(b-a)

        x1 = dot_ul + u*(dot_ur-dot_ul)
        x2 = dot_bl + u*(dot_br-dot_bl)

        noise_map = x1 + v*(x2-x1) # vertical interpolation 
        total_noise += noise_map * amplitude
        
        max_amplitude += amplitude

        amplitude *= persistence
        frequency *= lacunarity

    return total_noise / max_amplitude


