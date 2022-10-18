# Coulomb's Force Simulation
Coulomb's Force Simulation using realistic enough values.
___
This python script generates random points with mass and electromagnetic charge (any points can be specified by editing the code) and shows a sped up simulation of those points.
___
edit const variables to change different settings (here are some important ones):
- ** *MIN_DISTANCE* ** Since force is calculated by diving **xyz** by **distance**, any distance value very close to zero will cause the force to become VERY large and launch the particle at unrealistic speeds. so we limit the distance value to MIN_DISTANCE. (set too high and force will cap out at a low value but set too low and particles will fly at very high speeds) 
- *Q* default q charge value for each particle.
- *M* mass of each particle
- *METER* how many pixels is one meter in CI units.
