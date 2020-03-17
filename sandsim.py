
import numpy as np

class SandSim():

    def __init__(self, size, num_particles=None):
        if isinstance(size, int): size = (size,size)
        if len(size) > 2: raise ValueError("Size needs to be 2D")
        self.size = np.array(size)
        
        self.img = np.zeros(self.size, dtype=np.uint8)
        #add border?
        #self.img[0,:] = 150
        #self.img[:,0] = 150
        #self.img[-1,:] = 150
        #self.img[:,-1] = 150
        
        self.init_particles(num_particles)

    def init_particles(self, num_particles):
        if num_particles is None:
            num_pixels = np.prod(self.size)
            num_particles = int(np.power(num_pixels, 1./len(self.size)))
            
        self.particle_pos = np.random.sample((num_particles, 2)) * (self.size-1)
        self.particle_vel = np.zeros((num_particles, 2))
        
        pixel_pos = self.particle_pos.astype(np.int)
        self.img[pixel_pos[:,0], pixel_pos[:,1]] = 255
    

    def render(self):
        return self.img
        
    
    def apply_forces(self, deltatime, data):
        self.particle_pos = self.particle_pos + self.particle_vel*deltatime
        self.particle_pos[:,0] = np.clip(self.particle_pos[:,0], 0., self.size[0]-0.001)
        self.particle_pos[:,1] = np.clip(self.particle_pos[:,1], 0., self.size[1]-0.001)
        
        self.particle_vel = np.random.sample(self.particle_vel.shape) - 0.5
    
        
    def step(self, deltatime, data):
        self.old_pos = self.particle_pos
        
        self.apply_forces(deltatime, data)
        
        #all dirs the particles are taking and the number of steps of length 1
        dirs = self.particle_pos - self.old_pos
        norm = np.linalg.norm(dirs, axis=1)
        dirs[norm>1e-6] /= norm[norm>1e-6,np.newaxis]
        steps = np.ceil(norm).astype(np.int)
        
        #all substeps from oldpos to goal
        path_steps = np.arange(np.max(steps)+2)
        paths = self.old_pos[:,np.newaxis,:] + path_steps[np.newaxis,:,np.newaxis] * dirs[:,np.newaxis,:]
        
        #set goal as last step
        num = len(self.particle_pos)
        paths[np.arange(num), steps, :] = self.particle_pos #last step
        pixel_paths = paths.astype(np.int)
        pixel_paths[:,:,0] = np.clip(pixel_paths[:,:,0], 0, self.size[0]-1)
        pixel_paths[:,:,1] = np.clip(pixel_paths[:,:,1], 0, self.size[1]-1)
        
        #check each path until collision
        #hard vectorise, as particles might collide with each other
        #here: order of particles determines which particle gets to stay, for simplicity
        for i in range(num):
            #remove particle at old pos, might be placed here again down the line!
            self.img[pixel_paths[i,0,0], pixel_paths[i,0,1]] = 0
            points_in_img = self.img[pixel_paths[i,:,0], pixel_paths[i,:,1]]
            first_collision = np.argmax(points_in_img>0)
            
            #collision! -> take point one step before
            if first_collision>0 and first_collision <= steps[i]:
                self.particle_pos[i,:] = paths[i, first_collision-1, :]
            #else: goal pos already in particle_pos
                
            pixel_pos = self.particle_pos[i].astype(np.int)
            self.img[pixel_pos[0], pixel_pos[1]] = 255
        
        
        