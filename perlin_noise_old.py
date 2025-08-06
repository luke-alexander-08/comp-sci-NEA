import numpy as np
import matplotlib.pyplot as plt
import math

gradients = [(1, 0), (0.707, 0.707), (0, 1), (-0.707, 0.707), (-1, 0), (-0.707, -0.707), (0, -1), (0.707, -0.707)] # 8 pseudorandom gradient vectors which will be assigned to each point

def hash_func(ix, iy): # hash function using large primes. SWITCH TO PERMUTATION TABLE EVENTUALLY. does not allow for variance of seeds. 
    # print()
    return (ix * 1836311903 ^ iy * 2971215073) & 0xffffffff

def get_gradient(ix,iy):
    return gradients[hash_func(ix,iy) % 7]  # indexed from 0,7

def dot_product(v1, v2):
    return (v1[0] * v2[0]) + (v1[1] * v2[1])   # finds dot product between two vectors

def fade(n):
    return 6*n**5 - 15*n**4 + 10*n**3

def lerp(a,b,t):
    return a+t*(b-a)

def perlin(x,y):
    ix,iy = int(x), int(y) # floors x,y values
    nearby_corners = [(ix,iy), (ix+1,iy), (ix,iy+1), (ix+1,iy+1)] # bottom left, bottom right, top left, top right
    gradients = [get_gradient(a,b) for a,b in nearby_corners] # get 4 nearby corner gradient vectors. 
    distances = []
    # print(gradients)

    for nx,ny in nearby_corners:
        dx = x-nx
        dy = y-ny
        distances.append((dx,dy))
        # print(dx,dy)

    fx = fade(distances[0][0])
    fy = fade(distances[0][1])
    # print(fx,fy)

    dots = []
    for i in range(0, 4):
        dots.append(dot_product(gradients[i], distances[i]))
    # print(dots)

    #interpolations
    x1 = lerp(dots[0], dots[1], fx)
    x2 = lerp(dots[2], dots[3], fx)

    y1 = lerp(x1, x2, fy)

    # print(dots)
    return y1

def gen_noise(dimensions:tuple, scale):
    height, width = dimensions
    noise_map = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            noise_map[y, x] = perlin(x / width * scale, y / height * scale) # normalise to 0->1 range by dividing, scale sets "zoom"
    
    # print(noise_map)
    return noise_map

def fractal_noise(base_amplitude:float, base_frequency:float, persistence:float, lacunarity:float, octaves: int, dimensions:tuple):
    total = np.zeros(dimensions)
    max_amp = 0
    for _ in range(octaves):
        print("octave")
        noise_map = gen_noise(dimensions, base_frequency)
        total += noise_map * base_amplitude

        max_amp += base_amplitude

        base_frequency *= lacunarity
        base_amplitude *= persistence
    


    return total/max_amp
