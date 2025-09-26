import numpy as np
from math import floor

class RNG:
    def generate_perm(self):
        # Generate a list of integers from 0 to 255 of length 256
        raw_perm = np.arange(256)
        # Shuffle the permutation table
        np.random.shuffle(raw_perm)
        # Combine perm for indexes > 255
        self.permtable = np.tile(raw_perm,2)


class PerlinNoise:
    def __init__(self,seed):
        # Specs
        self.random_number_generator = RNG()
        self.seed = seed
        np.random.seed(self.seed) # Sets the seed

        self.gradients = np.array([[1, 0], [0, 1], [-1, 0], [0, -1],
                      [1, 1], [-1, 1], [-1, -1], [1, -1]])
        # Generates permutation table
        self.random_number_generator.generate_perm()
        self.permtable = self.random_number_generator.permtable
    

    def interpolate(self,a0:float,a1:float,w:float):
        # a0 and a1 are the two values
        # w is the interpolation weight
        return (a1-a0) * (3.0 - w * 2.0) * w*w + a0 # Cubic interpolation function

    # Compute gradient at that point
    def random_gradient(self,ix:int,iy:int):
        # Calculate hash value for the gradient point

        # Note & bitwise is faster
        idx = (self.permtable[ix & 255]+iy) & 255 # Don't bother asking IT WORKS DONT TOUCH IT!! 
        return self.gradients[self.permtable[idx]&7] # Choose one out of the 8

    def perlin(self, x: float, y: float):

        # Floor instead of int() for correct behavior with negatives
        x0, y0 = floor(x), floor(y)
        x1, y1 = x0 + 1, y0 + 1

        sx, sy = x - x0, y - y0

        # Interpolate top corners
        n0 = self.dot_grid_gradient(x0, y0, x, y)
        n1 = self.dot_grid_gradient(x1, y0, x, y)
        ix0 = self.interpolate(n0, n1, sx)

        # Interpolate bottom corners
        n2 = self.dot_grid_gradient(x0, y1, x, y)
        n3 = self.dot_grid_gradient(x1, y1, x, y)
        ix1 = self.interpolate(n2, n3, sx)

        # Return normalized mapped value
        return self.interpolate(ix0,ix1,sy)

    # Get gradient at grid point
    def dot_grid_gradient(self,ix:int,iy:int,x:float,y:float):
        # x,y are the float coordinates of point
        # ix,iy are the integer coordinates of the current grid point we are sampling from
        # Get gradient
        gradient = self.random_gradient(ix,iy)
        # Dot product dx -> x-ix * grad x and dy -> x-iy * grad y
        return ((x-ix) * gradient[0]) + ((y-iy) * gradient[1])