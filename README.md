# Coulomb's Force Simulation
Coulomb's Force Simulation using realistic enough values.
___
This python script generates random points with mass and electromagnetic charge (any points can be specified by editing the code) and shows a sped up simulation of those points.

## Variables
edit const variables to change different settings (here are some important ones):
- ****MIN_DISTANCE**** Since force is calculated by diving **q1.q2** by **distance**, any distance value very close to zero will cause the force to become VERY large and launch the particle at unrealistic speeds. so we limit the distance value to MIN_DISTANCE. (set too high and force will cap out at a low value but set too low and particles will fly at very high speeds) 
- ****Q**** default q charge value for each particle.
- ****M**** mass of each particle
- ****METER**** how many pixels is one meter in CI units. (will probably need to change ****MIN_DISTANCE**** too)

## Screenshots
![screenshot](https://github.com/0xIrakli/Coulombs-Force-Simulation/blob/master/screenshots/screenshot.jpg)
![screenshot1](https://github.com/0xIrakli/Coulombs-Force-Simulation/blob/master/screenshots/screenshot1.jpg)
![screenshot2](https://github.com/0xIrakli/Coulombs-Force-Simulation/blob/master/screenshots/screenshot2.jpg)
![screenshot3](https://github.com/0xIrakli/Coulombs-Force-Simulation/blob/master/screenshots/screenshot3.jpg)
