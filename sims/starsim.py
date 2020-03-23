
import numpy as np
from PIL import Image

class StarSim():

    def __init__(self, config):
        self.size = np.array( (config.getint('rows'), config.getint('cols')) )
        num_stars = config.getint('num_stars') if config['num_stars'] else None
        self.radius = 2
        self.enable_color = config.getboolean('enable_color')
        self.enable_galaxy = config.getboolean('enable_galaxy')
        self.enable_sparkle = config.getboolean('enable_sparkle')
        
        self.img = np.zeros((self.size[0], self.size[1], 3), dtype=np.uint8)
        self.collider = np.zeros(self.size, dtype=np.bool)
        
        self.init_stars(num_stars)

    def init_stars(self, num_stars):
        if num_stars is None:
            num_pixels = np.prod(self.size)
            num_stars = int(np.power(num_pixels, 1./len(self.size)))*3

        num_galaxy_stars = int(0.7*num_stars)
        
        stars = []
        if self.enable_galaxy:
            mean = self.size/2 + (np.random.sample(2) * self.size/2)
            cov = np.random.rand(2,2)*2 -1.
            cov = np.dot(cov, cov.T) * 50.
            eig = min(np.abs(np.linalg.eig(cov)[0]))
            if eig<5: cov *= 5./eig
            galaxy_stars = np.random.multivariate_normal(mean, cov, size=num_galaxy_stars).astype(np.uint8)
            for pos in galaxy_stars:
                if pos[0]>=self.radius and pos[0]<self.size[0]-self.radius and pos[1]>=self.radius and pos[1]<self.size[1]-self.radius:
                    stars.append(pos)
                    self.collider[pos[0]-self.radius:pos[0]+self.radius, pos[1]-self.radius:pos[1]+self.radius] = True
        
                
        stars_left = num_stars - len(stars)
        for i in range(stars_left):
            while True:
                pos = np.random.randint(self.radius, min(self.size)-self.radius, size=2)
                if not self.collider[pos[0], pos[1]]: break
            stars.append(pos)
            self.collider[pos[0]-self.radius:pos[0]+self.radius, pos[1]-self.radius:pos[1]+self.radius] = True

        self.star_pos = np.array(stars)
        
        self.star_period = np.random.sample(num_stars) +0.5
        self.star_time_aggregate= np.random.sample(num_stars) * self.star_period
        self.star_distance = np.random.sample(num_stars)[:,np.newaxis]
        
        if self.enable_color:
            self.star_col = np.random.sample((num_stars, 3))
        else:
            self.star_col = np.random.sample((num_stars, 1))
            self.star_col = np.tile(self.star_col, (1,3))
        self.star_col = self.star_col*150 +100
        self.star_col = self.star_col.astype(np.uint8)
    

    def render(self):
        return Image.fromarray(self.img).convert('RGB')
        
    
        
    def step(self, deltatime, data):
        self.star_time_aggregate += deltatime
        percentages = np.abs(self.star_time_aggregate / self.star_period)
        overtime = percentages>1.
        percentages[overtime] = 1.
        percentages = percentages*0.5 +0.5
        self.star_time_aggregate[overtime] = -self.star_period[overtime]

        colors = self.star_col * percentages[:, np.newaxis]


        self.img = np.zeros((self.size[0], self.size[1], 3), dtype=np.uint8)
        self.img[self.star_pos[:,0], self.star_pos[:,1]] = (colors).astype(np.uint8)

        if self.enable_sparkle:
            side_colors = (colors*0.3*self.star_distance).astype(np.uint8)
            sides = [(self.star_pos[:,0]+1, self.star_pos[:,1]),  (self.star_pos[:,0], self.star_pos[:,1]+1), 
                    (self.star_pos[:,0]-1, self.star_pos[:,1]),  (self.star_pos[:,0], self.star_pos[:,1]-1)  ]
            for x,y in sides:
                self.img[x,y] = np.maximum(self.img[x,y], side_colors)

            edge_colors = (colors*0.03*self.star_distance).astype(np.uint8)
            edges = [(self.star_pos[:,0]+1, self.star_pos[:,1]+1),  (self.star_pos[:,0]+1, self.star_pos[:,1]-1), 
                    (self.star_pos[:,0]-1, self.star_pos[:,1]+1),  (self.star_pos[:,0]-1, self.star_pos[:,1]-1)  ]
            for x,y in edges:
                self.img[x,y] = np.maximum(self.img[x,y], edge_colors)
        
        
        