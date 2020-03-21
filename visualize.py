from collector import Stats

import matplotlib.pyplot as plt
import seaborn as sns


class Visualize:
    @staticmethod
    def age_pyr(model):
        df = model.df

        # Draw Plot
        # fig = plt.figure(figsize=(13,10), dpi= 40)
        sns.set_palette("GnBu_d")
        sns.barplot(x='M', y='Age', data=df, order=df.Age[::-1], label='Males', color=sns.color_palette("GnBu_d")[1])
        sns.barplot(x='F', y='Age', data=df, order=df.Age[::-1], label='Females', color=sns.color_palette("GnBu_d")[2])
        sns.despine(left=True, bottom=True)

        # Makeup
        plt.xlabel("$Population Count$")
        plt.ylabel("Demographic")
        plt.yticks(fontsize=12)
        plt.title("Population Pyramid", fontsize=22)
        plt.legend()

    @staticmethod
    def containers(model):
        # plot S, I, R, and D in a line plot
        model_data = model.datacollector.get_model_vars_dataframe()
        for col in model_data.columns:
            plt.plot(model_data[col], label=col)
        plt.title("Progress of the Virus over Time")
        plt.ylabel("People")
        plt.xlabel("Time")
        plt.legend()

    @staticmethod
    def mortality_pie(model):
        # plot the mortality rate in a pir chart
        m_rate = Stats.mortality_rate(model)
        plt.title("Virus Mortality")
        sns.set_palette("GnBu_d")
        plt.pie([m_rate, 1 - m_rate], labels=['Dead (' + str(round(m_rate * 100, 1)) + '%)',
                                              "Recovered (" + str(round((1 - m_rate) * 100, 1)) + "%)"],
                explode=[0.1, 0])

    def draw_everything(self, model):
        plt.figure(figsize=[40, 10], dpi=40)
        plt.subplot(1, 3, 1)

        self.age_pyr(model)
        plt.subplot(1, 3, 2)

        self.containers(model)
        plt.subplot(1, 3, 3)

        self.mortality_pie(model)
        plt.show()
