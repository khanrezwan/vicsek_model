# Vicksek Model Simulation Using Python [MESA](https://mesa.readthedocs.io/en/latest/)

## Setup:
1. Download the repo. open terminal
2. Create vurtual environment
    - `$ python3 -m venv /path/to/vicsek_model`
3. Activate the virtual environment
    - `$ source /path/to/vicsek_model/bin/activate`
4. Install the dependencies
    - `$ pip install -r /path/to/vicsek_model/requirements.txt`

## To Run:
1. Activate the virtual environment
    - `$ source /path/to/vicsek_model/bin/activate`
2. Run
    - `$ python3 /path/to/vicsek_model/PhaseModel.py`

## Deactivate the Virtual Environment
1. `$ deactivate`

## Vicsek Model Overview:

### Parameters:
- Particles are in square shaped cell size L with periodic boundary. Variable name `L`. Global Variable.
-  Interaction radius r. Variable name `Radius`. Global Variable.
-  Total time steps variable for simulation `Steps`. Global Variable.
-  Agents to be simulated: Variable name `Agents`. Global Variable.
-  Random noise &eta; `eta`. Global Variable.
-  Velocity v<sub>i</sub>(t). variable name `Velocity`
-  Heading &theta;<sub>i</sub>(t). variable name `theta` (in `class PhaseAgent(Agent)`) .
-  Position x<sub>i</sub>(t). variable name `position` (in `class PhaseAgent(Agent)`).

### Protocol:
1. at each time interval &Delta; t = 1 the particle/agent updates position and heading using following rule:
    - <img src="https://latex.codecogs.com/svg.image?x_i(t&plus;1)&space;=&space;x_i(t)&plus;&space;v_i(t)&space;\Delta&space;t" title="x_i(t+1) = x_i(t)+ v_i(t) \Delta t" />
    - <img src="https://latex.codecogs.com/svg.image?\theta_{i}(t&plus;1)&space;=&space;{\langle&space;\theta_{i}(t)&space;\rangle}_r&space;&plus;&space;\Delta&space;\theta" title="\theta_{i}(t+1) = {\langle \theta_{i}(t) \rangle}_r + \Delta \theta" />
- Here,  
        <img src="https://latex.codecogs.com/svg.image?{\langle&space;\theta_{i}(t)&space;\rangle}_r&space;=&space;arctan&space;\Bigg[&space;\dfrac{{\langle&space;\sin(\theta(t))&space;\rangle}_r}{{\langle&space;\cos(\theta(t))&space;\rangle}_r}\Bigg]" title="{\langle \theta_{i}(t) \rangle}_r = arctan \Bigg[ \dfrac{{\langle \sin(\theta(t)) \rangle}_r}{{\langle \cos(\theta(t)) \rangle}_r}\Bigg]" />
        
 - &Delta;&theta; is random number from uniform interval <img src="https://latex.codecogs.com/svg.image?\Big[&space;-&space;\frac{\eta}{2},&space;\frac{\eta}{2}&space;\Big]" title="\Big[ - \frac{\eta}{2}, \frac{\eta}{2} \Big]" />

   
