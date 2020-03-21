from mesa import Agent


class Person(Agent):
    def __init__(self, unique_id, model, pop_slice, state, infection_rate, mortality_rate):
        super().__init__(unique_id, model)  # let's the agent use the methods of the parent,
        # mesa class, very important

        self.pop_slice = pop_slice  # which segment of the population I belong to
        self.state = state  # sick, healthy, etc
        self.infection_rate = infection_rate  # based on the population standards
        self.mortality_rate = mortality_rate / 100

        # the virus takes 10-14 days to develop symtopms and be capable of infecting others.
        # I use latency to control this time
        self.latency = self.random.randint(0, 14)
        self.home = None  # this will be set to the agents original position when
        # when we place it on the map

        # things the agent does each turn
        self.actions = ['move', 'decrease_latency', 'infect_others', 'exit']

    # Similar to the NetLogo virus model, we a modeling the agents as moving
    # randomly around a grid. Only, there is a 50% chance each turn they will move
    # back to their original positions. This means that, like the in real life,
    # the virus needs to spread from location to location by infecting new people,
    # not by relying on a single rouge infectee

    def move(self):
        if self.random.random() < 0.5:
            # move randomly
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=False,  # agents can't move diagonally
                include_center=True  # agents can not move
            )
            new_position = self.random.choice(possible_steps)  # a random legal move
        else:
            # move home
            new_position = self.home
        self.model.grid.move_agent(self, new_position)

    # The complicated method on line three calls is a call to a mesa
    # method that finds all the other people on the same space on the
    # grid. Then, if the agent is susceptible, we roll a die to infect.

    def infect_others(self):
        if self.state == "I":
            attempted_transmissions = 0
            for other_agent in self.model.grid.get_cell_list_contents([self.pos]):
                attempted_transmissions += 1
                if attempted_transmissions > self.model.contacts:
                    break
                elif other_agent.state == "S":
                    if self.random.random() < other_agent.infection_rate:
                        other_agent.state = "I"
                        other_agent.latency = self.random.randint(10, 14)

    def exit(self):
        if self.state == "I" and self.latency == 0:
            if self.random.random() <= (1 / self.model.duration):
                if self.random.random() <= self.mortality_rate:
                    self.state = "D"
                else:
                    self.state = "R"

    def decrease_latency(self):
        if self.latency > 0:
            self.latency -= 1

    # To step, the agent goes through all of its actions, shuffles them,
    # and runs them. The shuffling is important here, because we are
    # modeling the porbablilitis as independant (with the different functions)
    # when the actual data we are basing them on takes them as mutually exclusive
    # If we didn't shuffle, the sim would be biased towards the one it ran first.

    def step(self):
        if not self.state == "D":
            for action in self.actions:
                eval("self." + action + "()")