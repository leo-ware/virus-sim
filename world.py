from collector import Stats
from person import Person

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class World(Model):

    def __init__(self, df, world_size=(10, 10), rnumber=2.28, duration=7, contacts=10):

        # r number: https://www.ijidonline.com/article/S1201-9712(20)30091-6/fulltext

        self.rnumber = rnumber
        self.duration = duration
        self.contacts = contacts
        self.infection_rate = self.rnumber / (self.duration * self.contacts)

        self.df = df  # contains information to initialize the system
        self.world_size = world_size
        self.which_one = "ABM"  # as opposed to SIR
        self.containers = ['S0', 'I0', 'R0', 'D0']

        self.schedule = RandomActivation(self)  # mesa does not support simultaneous
        # activation of units, but random works
        self.grid = MultiGrid(*world_size, True)  # agents exist on a grid
        self.running = True  # needed for internal mesa stuff
        self.done = False

        # create agents
        i = 0  # will create a unique identifier for each agent

        # for each population slice and container, make agents to meet specifications
        for pop_slice, *other in self.df.iterrows():
            for container in self.containers:
                for _ in range(int(self.df.loc[pop_slice, container])):
                    a = Person(unique_id=i, model=self, pop_slice=pop_slice, state=container[0], infection_rate=
                    self.infection_rate, mortality_rate=self.df.loc[pop_slice, 'mortality_rate'])
                    self.schedule.add(a)
                    i += 1

        # add agents to map
        self.placed_places = []
        for agent in self.schedule.agents:
            # possibility 1: place the agent randomly
            if self.random.random() < 0.1 or len(self.placed_places) < 1:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))
                agent.home = (x, y)
                self.placed_places.append((x, y))
            # possibility 2: place the agent randomly with preference
            # for occupied squares
            else:
                pos = self.random.choice(self.placed_places)
                self.grid.place_agent(agent, pos)
                agent.home = pos
                self.placed_places.append(pos)

        # initialize data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Susceptible": lambda x: Stats.number_susceptible(self),
                "Infected": lambda x: Stats.number_infected(self),
                "Recovered": lambda x: Stats.number_recovered(self),
                "Dead": lambda x: Stats.number_dead(self)
            },
            agent_reporters={"State": "state"}
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        if not Stats.number_susceptible(self) and not Stats.number_infected(self):
            self.done = True

    def run(self, max_times=float('inf')):
        runs = 0
        while not self.done:
            if runs >= max_times:
                break
            self.step()
            runs += 1
