# These collect information about the state of the system at each step.
# The @staticmethod decorator just means they don;t use any
# information about the Stats class to operate.


class Stats:
    @staticmethod
    def number_infected(model):
        return sum([a.state == "I" for a in model.schedule.agents])

    @staticmethod
    def number_susceptible(model):
        return sum([a.state == "S" for a in model.schedule.agents])

    @staticmethod
    def number_recovered(model):
        return sum([a.state == "R" for a in model.schedule.agents])

    @staticmethod
    def number_dead(model):
        return sum([a.state == "D" for a in model.schedule.agents])

    @staticmethod
    def mortality_rate(model):
        dead = Stats.number_dead(model)
        infected = Stats.number_infected(model)  # yes, this is right
        recovered = Stats.number_recovered(model)
        return dead / (dead + infected + recovered)
