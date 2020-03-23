
import numpy as np
from PIL import Image

MAX_DODOS = 300

class DodoSim():

    def __init__(self, config):
        self.size = np.array( (config.getint('rows'), config.getint('cols')) )
        self.food_spawn_rate = 0.3

        self.init_world()

    def init_world(self):
        self.food_time = 0.
        self.food_pos = np.array([]).reshape(0,2)
        self.dodo_pos = np.array([]).reshape(0,2)
        self.dodo_vel = np.array([]).reshape(0,2)
        self.dodo_dna = np.array([]).reshape(0,3)
        self.dodo_energy = np.array([])
        self.dodo_eating = np.array([], dtype=np.bool)
        self.dodo_redprod_time = np.array([])

        for i in range(50):
            self.new_food()

        for i in range(5):
            self.new_dodo()
        

    def new_food(self):
        pos = np.random.sample(2)* (self.size-1)
        self.food_pos = np.concatenate([self.food_pos, pos[np.newaxis,:]])

    def new_dodo(self, parent=None):
        if self.dodo_pos.shape[0] >= MAX_DODOS:
            if not self.printed_warning:
                print('Reached max dodos.')
                self.printed_warning = True
            return 
        if parent is None or np.random.random()<0.1:
            dna = np.zeros(3)
            for i in range(150/5):
                dna[np.random.randint(3)] += 5
            pos = np.random.sample(2)* (self.size-1)
            vel = np.random.sample(2)* (self.size-1)
            vel /= np.linalg.norm(vel)
        else:
            dna = self.dodo_dna[parent]
            for i in range(np.random.randint(5)):
                indexP = np.random.randint(3)
                indexM = np.random.randint(3)
                while dna[indexP]+5 > 150: indexP = (indexP+1)%3
                dna[indexP] += 5
                while dna[indexM]-5 < 0: indexM = (indexM+1)%3
                dna[indexM] -= 5
            #dna = self.dodo_dna[parent] + np.random.randint(5, size=3)
            #in case they stack too much if they spawn close: random spawn
            #pos = np.random.sample(2)* (self.size-1)
            #vel = np.random.sample(2)* (self.size-1)
            #vel /= np.linalg.norm(vel)
            vel = -self.dodo_vel[parent]
            while True:
                dirs = np.array([[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]])
                pos = self.dodo_pos[parent] + dirs[np.random.randint(8)]*3
                if pos[0]>=0 and pos[1]>=0 and pos[0]<self.size[0] and pos[1]<self.size[1]:
                    break
        
        self.dodo_dna = np.concatenate([self.dodo_dna, dna[np.newaxis,:]])
        self.dodo_pos = np.concatenate([self.dodo_pos, pos[np.newaxis,:]])
        self.dodo_vel = np.concatenate([self.dodo_vel, vel[np.newaxis,:]])
        self.dodo_energy = np.append(self.dodo_energy, 100)
        self.dodo_eating = np.append(self.dodo_eating, False)
        self.dodo_redprod_time = np.append(self.dodo_redprod_time, 0.)


    def delete_food(self, food):
        self.food_pos = np.delete(self.food_pos, food, axis=0)

    def delete_dodo(self, dodo):
        mask = np.logical_not(dodo)
        self.dodo_dna = self.dodo_dna[mask]
        self.dodo_pos = self.dodo_pos[mask]
        self.dodo_vel = self.dodo_vel[mask]
        self.dodo_energy = self.dodo_energy[mask]
        self.dodo_eating = self.dodo_eating[mask]
        self.dodo_redprod_time = self.dodo_redprod_time[mask]
        

    def render(self):
        img = np.zeros((self.size[0], self.size[1], 3), dtype=np.uint8)
        food_pixel = self.food_pos.astype(np.uint8)
        dodo_pixel = self.dodo_pos.astype(np.uint8)
        img[food_pixel[:,0], food_pixel[:,1]] = (0, 0, 250)
        dna_viz = (150*self.dodo_dna / np.max(self.dodo_dna, axis=1)[:, np.newaxis]).astype(np.uint8)
        img[dodo_pixel[:,0], dodo_pixel[:,1]] = dna_viz+100
        return Image.fromarray(img).convert('RGB')
    
    #I like the naming convention, okay?
    def dodo_food(self, deltatime):
        self.food_time -= deltatime
        if self.food_time<=0.:
            self.new_food()
            self.food_time = np.random.exponential(self.food_spawn_rate)

    def dodo_seek(self):
        if self.food_pos.shape[0] == 0 or self.dodo_pos.shape[0] == 0:
            self.goal_dists = np.zeros(self.dodo_pos.shape[0])+np.inf
            self.closest_food = np.zeros(self.dodo_pos.shape[0], dtype=np.int)-1
            return
        dirs = self.food_pos - self.dodo_pos[:,np.newaxis,:]
        dists = np.linalg.norm(dirs, axis=2)
        self.closest_food = np.argmin(dists, axis=1)

        dirs = self.food_pos[self.closest_food] - self.dodo_pos
        dists = np.linalg.norm(dirs, axis=1)
        dists[dists<1.5] = 0.
        dirs /= dists[:, np.newaxis]
        ranges = self.dodo_dna[:,0]/10.0 + 2
        in_range = np.logical_and(dists < ranges, dists >= 1.5)

        self.dodo_vel[in_range] = dirs[in_range]
        self.goal_dists = dists

    def dodo_move(self, deltatime):
        move_range = deltatime * (5+self.dodo_dna[:, 1]/20)
        overshoot = move_range > self.goal_dists
        move_range[overshoot] = self.goal_dists[overshoot]
        move_range[self.dodo_eating] = 0.
        self.dodo_pos += self.dodo_vel*move_range[:, np.newaxis]

        closeness_dirs = np.repeat(self.dodo_pos[np.newaxis, :, :], self.dodo_pos.shape[0], axis=0)
        closeness_dirs = closeness_dirs - self.dodo_pos[:, np.newaxis, :]
        closeness_dists = np.linalg.norm(closeness_dirs, axis=2)
        collide = closeness_dists < 1.0
        closeness_dirs *= collide.astype(np.float)[:,:,np.newaxis]
        closeness_dirs = np.sum(closeness_dirs*(2.0 - closeness_dists[:,:,np.newaxis]), axis=1)
        self.dodo_pos += closeness_dirs

        under_range_x = self.dodo_pos[:,0] < 0
        under_range_y = self.dodo_pos[:,1] < 0
        over_range_x = self.dodo_pos[:,0] >= self.size[0]
        over_range_y = self.dodo_pos[:,1] >= self.size[1]

        self.dodo_pos[under_range_x,0] = 0.
        self.dodo_pos[under_range_y,1] = 0.
        self.dodo_pos[over_range_x,0] = self.size[0]-0.00001
        self.dodo_pos[over_range_y,1] = self.size[1]-0.00001
        self.dodo_vel[under_range_x,0] *= -1
        self.dodo_vel[under_range_y,1] *= -1
        self.dodo_vel[over_range_x,0] *= -1
        self.dodo_vel[over_range_y,1] *= -1

    def dodo_eat(self):
        self.dodo_eating = np.zeros_like(self.dodo_eating).astype(np.bool)
        self.dodo_eating = self.goal_dists < 1.5
        self.dodo_energy[self.dodo_eating] += 50
        self.delete_food(self.closest_food[self.dodo_eating])


    def dodo_health(self, deltatime):
        self.dodo_energy -= deltatime*(30 - 5*self.dodo_dna[:,2]/150)
        self.delete_dodo(self.dodo_energy <= 0.)

    def dodo_reproduce(self, deltatime):
        if self.dodo_pos.shape[0] == 0:
            print('All dodos died! Spawning new random dodos and increasing food spawn rate.')
            self.food_spawn_rate *= 0.95
            for i in range(5):
                self.new_dodo()
        else:
            self.dodo_redprod_time += deltatime*10
            reprod = self.dodo_redprod_time > (20 + 150-self.dodo_dna[:,2])
            self.dodo_redprod_time[reprod] = 0.
            for dodo in np.arange(reprod.shape[0])[reprod]:
                self.new_dodo(parent=dodo)

        
    def step(self, deltatime, data):
        self.printed_warning = False
        self.dodo_food(deltatime)
        self.dodo_seek()
        self.dodo_move(deltatime)
        self.dodo_eat()
        self.dodo_health(deltatime)
        self.dodo_reproduce(deltatime)
        
        
        