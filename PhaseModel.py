from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import ContinuousSpace
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
Radius = 1.0  # interaction radius between agents
L = 5  # Grid Size
Velocity = 0.3
Steps = 50  # time steps
Agents = 300
Eta = 0.1  # Noise
AnimationSpeed = 350  # higher for slower

X = np.zeros(shape=(Steps, Agents))
Y = np.zeros(shape=(Steps, Agents))
LeaderX =np.zeros(shape=(Steps, 1))
LeaderY =np.zeros(shape=(Steps, 1))
Theta = np.zeros(shape=(Steps, Agents))

class PhaseAgent(Agent):
    def __init__(self, unique_id, model, velocity=0.0, position=0.0, theta=0.0, x=0.0, y=0.0,leader=False):
        super().__init__(unique_id, model)
        self.velocity = velocity
        # self.pos = pos
        self.theta = theta
        self.position = position
        self.x = x
        self.y = y
        self.leader = leader
        self.neighbors = None
        pass

    def getdelTheta(self):
        return np.random.uniform(-Eta / 2.0, Eta / 2.0)

    def step(self):
        self.x = self.position * np.cos(self.theta)
        self.y = self.position * np.sin(self.theta)
        self.position = self.position + self.velocity
        if not self.leader:
            self.neighbors = []
            self.neighbors = self.model.grid.get_neighbors(self.pos, Radius, include_center=True)
            R = len(self.neighbors)
            if R > 0:  # got neighbor(s)
                sinSum = 0
                cosSum = 0

                for neighbor in self.neighbors:
                    sinSum = sinSum + np.sin(neighbor.theta)
                    cosSum = cosSum + np.cos(neighbor.theta)
                self.theta = np.arctan2(sinSum / R, cosSum / R)
            self.theta = self.theta + self.getdelTheta()
        # if self.leader:
        #     self.psi = np.arctan2(self.y,self.x)

    def advance(self):

        if self.model.grid.out_of_bounds((self.x, self.y)):
            self.x, self.y = self.model.grid.torus_adj((self.x, self.y))
        # print("ID: ", self.unique_id," x ",self.x," y ",self.y," psi ",self.psi)
        self.model.grid.move_agent(self, (self.x, self.y))


class PhaseModel(Model):
    def __init__(self, N, grid_x, grid_y, createLeader=False):
        self.numAgents = N
        self.grid = ContinuousSpace(grid_x / 2, grid_y / 2, True, -grid_x / 2,
                                    -grid_y / 2)  # Agent may occupy any space in  X,Y and may overlap
        self.schedule = SimultaneousActivation(self)  # all agents updates together
        self.leader = None
        # create agents
        for i in range(self.numAgents):
            # random return 1.0 scaling to need
            # formula random*(High-Low)+ Low
            x = np.random.random() * (grid_x) - grid_x / 2
            y = np.random.random() * (grid_y) - grid_y / 2
            position = np.sqrt(np.power(x, 2) + np.power(y, 2)) 
            theta = np.arctan2(y, x)
            a = PhaseAgent(i, self, Velocity, position, theta,False)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)
        # create Leader
        if createLeader:
            x = np.random.random() * (grid_x) - grid_x / 2
            y = np.random.random() * (grid_y) - grid_y / 2
            position = np.sqrt(np.power(x, 2) + np.power(y, 2))
            theta = np.arctan2(y, x)
            leader = PhaseAgent(i, self, Velocity, position, theta, True)
            self.grid.place_agent(leader, (x, y))
            self.schedule.add(leader)
            self.leader = leader #keep a reference

    def step(self):
        self.schedule.step()
        pass


fig, ax = plt.subplots(figsize=(L, L))
ax.set(xlim=(-L / 2, L / 2), ylim=(-L / 2, L / 2))
time_text = ax.text(0.05, 0.95, '', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)


def animate(i):
    # y_i = Y[i,::3]
    # scat.set_offsets(np.c_[LeaderX[i, :], LeaderY[i, :]]) # just for leader
    scat.set_offsets(np.c_[X[i, :], Y[i, :]])
    time_text.set_text('L= %.1d; Agents = %.1d; Noise = %.2f; step = %.1d' % (L, Agents, Eta, i))
    return scat, time_text,


if __name__ == '__main__':
    model = PhaseModel(Agents, L, L,False)
    meanTheta0 = np.mean([a.theta for a in model.schedule.agents if not a.leader])
    print("Mean ",meanTheta0)
    if model.leader:
        ThetaLeaderStart = model.leader.theta
        print("Leader Theta",ThetaLeaderStart)
    for i in range(Steps):
        model.step()
        agent_x = [a.x for a in model.schedule.agents]
        X[i, :] = agent_x
        # LeaderX[i] = model.leader.x
        # LeaderY[i] = model.leader.y
        agent_y = [a.y for a in model.schedule.agents]
        Y[i, :] = agent_y
        Theta[i,:] = [a.theta for a in model.schedule.agents]
    #scat = ax.scatter(X, Y, marker="x", alpha=0.5)
    scat = ax.scatter(LeaderX, LeaderY, marker="x", alpha=0.5)
    anim = FuncAnimation(fig, animate, interval=AnimationSpeed, frames=Steps)

    plt.draw()
    print("starting animation")
    plt.show()
    plt.cla()
    linestyles = ['-', '--', '-.', ':']
    for j in range(Agents):
        plt.plot(range(0, Steps,1), Theta[:, j], linestyle=linestyles[random.randint(0,3)])

    meanTheta0 = [meanTheta0]*Steps
    if model.leader:
        print("Leader Theta End", model.leader.theta)
        ThetaLeaderStart = [ThetaLeaderStart]*Steps
        ThetaLeaderEnd = [model.leader.theta]*Steps
        plt.plot(range(0, Steps, 1), ThetaLeaderEnd, linestyle='-.', linewidth=5, color='blue')
        # plt.plot(range(0, Steps, 1), ThetaLeaderStart, linestyle=':', linewidth=5, color='brown')

    # plt.plot(range(0, Steps,1), meanTheta0, linestyle=':', linewidth=5,color ='black')
    print("Mean end", np.mean([a.theta for a in model.schedule.agents if not a.leader]))
    plt.show()
    print("done")
