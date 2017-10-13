import math
import random
import numpy as np

class Heightmap:

    def __init__(self, params, debug=False):
        self.params = params

        # start making the heightmap
        self.size = params.get('size')

        # empty array of arrays, size by size
        # NOTE: grid references in the form of self.grid[num][num] need to be in the format of [y][x], or vertical coordinate first, then horizontal
        self.grid = np.zeros((self.size, self.size))

        # set corner heights
        minheight = self.params.get('height_range')[0]
        maxheight = self.params.get('height_range')[1]

        self.grid[0][0] = random.randint(minheight, maxheight)
        self.grid[self.size - 1][0] = random.randint(minheight, maxheight)
        self.grid[0][self.size - 1] = random.randint(minheight, maxheight)
        self.grid[self.size - 1][self.size - 1] = random.randint(minheight, maxheight)

        # Process the rest of the map, passing the 4 corners
        self._subdivide(0, 0, self.size - 1, self.size - 1)

        # compute average and record highest and lowest heights
        avg = []
        m = []
        l = []
        heights = []
        for g in self.grid:
            heights.extend(g)
            m.append(max(g))
            l.append(min(g))
            avg.append(sum(g) / float(len(g)))

        self.highest_height = max(m)
        self.lowest_height = min(l)
        self.average_height = sum(avg) / float(len(avg))
        sea_percent = params.get('sea_percent')
        heights.sort()
        self.sealevel = heights[ round(len(heights) * (sea_percent / 100)) ]

        if sea_percent == 100:
            self.sealevel = 255

        if debug:
            print("Sea level at {} or {}%".format(self.sealevel, sea_percent))


    def height_at(self, x, y):
        return self.grid[x][y]

    def _adjust(self, xa, ya, x, y, xb, yb):
        """ fix the sides of the map """ 

        # if the altitude is still blank. This is totally backwards and the grid is actually stored in y,x format
        if self.grid[x][y] == 0:
           
            # this is a distance calculation that doesn't apply perfectly for hexes since in 4 of 6 directions, you traverse both x and y...
            d = math.fabs(xa - xb) + math.fabs(ya - yb)

            # constant
            ROUGHNESS = self.params.get('roughness')

            # v is the average of the altitudes of hexes a and b, plus or minus a random factor times roughness times crude distance...wut?
            v = (self.grid[xa][ya] + self.grid[xb][yb]) / 2.0 + (random.random() - 0.5) * d * ROUGHNESS
            
            # int cast of the modulous of the absolute value of v... Modulus should be unnecessary given later limit based on height_range. 
            c = int(math.fabs(v) % 257)

            # this is what controls the map wrapping, commented out because we're doing a patch, not a full world
            # if we're at the left side of the map
            #if y == 0:
                # set the right edge of the map to match 
            #    self.grid[x][self.size - 1] = c

            # not sure what the heck this does, it's for some kind of mirroring
            # if we're at the top or bottom of the map,
            #if x == 0 or x == self.size - 1:
                # and we're left of the far-right side of the map
            #    if y < self.size - 1:
                    # set the horizontal mirror equal to the same height
            #        self.grid[x][self.size - 1 - y] = c

            # keep heights within map range
            range_low, range_high = self.params.get('height_range')
            if c < range_low:
                c = range_low
            elif c > range_high:
                c = range_high
            self.grid[x][y] = c

    def _subdivide(self, x1, y1, x2, y2):
        """ subdivide the heightmap iterate """

        # If the two hexes passed in aren't adjacent...
        if not ((x2 - x1 < 2.0) and (y2 - y1 < 2.0)):
            # set x and y to the midpoint between the two hexes
            x = int((x1 + x2) / 2)
            y = int((y1 + y2) / 2)

            # calculate the 'average' altitude of both the 2 passed in hexes and their mirrors
            v = int((self.grid[x1][y1] + self.grid[x2][y1] + self.grid[x2][y2] + self.grid[x1][y2]) / 4)
            #v = int((self.grid[x1][y1] + self.grid[x2][y2]) / 2)

            # ensure the result fits within the established height range
            range_low, range_high = self.params.get('height_range')
            if v < range_low:
                v = range_low
            elif v > range_high:
                v = range_high
            # set the hex altitude
            self.grid[x][y] = v

            # wtf does this do?
            self._adjust(x1, y1, x, y1, x2, y1)
            self._adjust(x2, y1, x2, y, x2, y2)
            self._adjust(x1, y2, x, y2, x2, y2)
            self._adjust(x1, y1, x1, y, x1, y2)

            # call recursive subdivisions from existing corners and the y,x midpoint
            self._subdivide(x1, y1, x, y)
            self._subdivide(x, y1, x2, y)
            self._subdivide(x, y, x2, y2)
            self._subdivide(x1, y, x, y2)
                                         
