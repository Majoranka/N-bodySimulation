# N-bodySimulation
Interactive n-body simulation based on pygame using a simple model. The goal is not to have a completely true model, but to provide a fun way of exploring n body simulation.
To make the simulation faster and more user friendly, we use an unrealistically strong gravity model.

# Getting the code to run
The requirements to run the code are having Python (any version of Python 3 should work) and the module pygame installed. To run the code, simply download the code with the data file (which should be kept in the same file as the script) and then run the code. 

![Snímka obrazovky (18)](https://github.com/mariangloser/N-bodySimulation/assets/147488596/ae3889f8-529f-4a1e-a278-0ef96e3862e6)






































# Controls
Left click spawns a small particle, while a right click can be used to move the camera. Holding the mouse button spawns arbitrarily big body. The camera can be moved using also the arrows and pressing spacebar.

# Remarks
Delta time is not used in the simulation, so that the computation is faster, though this can be very easily modified. The exponent used in the computation of gravity can also be easily modified by changing the exponent parameter in the code. To maximize performance (focusing on the actual simulation and perhaps realism) the stars can be turned off by changing the stars parameter to False.
