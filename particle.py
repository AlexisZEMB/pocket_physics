import math

class Particle:
    def __init__(self, x, y, vx, vy, m, time_scale):
        self.x = x                      # x initial position
        self.y = y                      # y initial position
        self.vx = vx                    # x initial velocity
        self.vy = vy                    # y initial velocity
        self.m = m                      # mass of the particle
        self.G = 6.67 * 10e-11          # gravitational constant (m/s^2)
        self.r_min = 0.1                # Minimum distance to trigger merging
        self.time_scale = time_scale    # Time scale for the simulation

    def equals(self, p):
        """Return True if self and p are the same particle"""
        return self.x == p.x and self.y == p.y and self.vx == p.vx and self.vy == p.vy and self.m == p.m

    def get_closest_particles(self, liste_particules, n):
        """Return the n closest particles to self"""
        distances = []
        for p in liste_particules:
            if p != self:
                distance = math.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
                distances.append((p, distance))
        distances.sort(key=lambda x: x[1])
        return [p[0] for p in distances[:n]]

    def compute_new_position(self, liste_particules):
        """Compute gravitational pull from the 10 closest particles and update the velocity and position of the particle"""
        # Get 3 closest particles to self
        closest_particles = self.get_closest_particles(liste_particules, 3)

        for p in closest_particles:
            r = math.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)  # Distance between self and p

            for p in closest_particles:
                r = math.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
                if r >= self.r_min:
                    a = self.G * p.m / r**2
                    direction = math.atan2(p.y - self.y, p.x - self.x)
                    self.vx += a * math.cos(direction)
                    self.vy += a * math.sin(direction)

            time_step = self.time_scale / 100
            self.x += self.vx * time_step
            self.y += self.vy * time_step

            return self, None  # Return the updated particle and no particles to merge