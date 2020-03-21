# virussim
A agent based model of virus transmission based on COVID-19 using the mesa framework

THE IDEA
Based on an idea by Andre Vacha, COVID-19 has very different mortality rates for
people of different ages, but China is known for having a weird population pyramid. So,
we wrote this model to expiriment with other countries with different age distributions,
such as the United States. Although we collaborated on the whole program, he mostly 
worked on the visualizations and the web scaper, and I mostly worked on the backend.

Note: This isn't intended to make actual predictions about the world or anything, it's 
just a thought expiriment. Please don't sue me.


HOW TO USE
Go to the run.py file and play with the parameters. The program will output a visualization
of the final results of the run.


THE MODEL
The model initializes by pulling demographic data for the target country, and generating
populations of agents of different ages, such that the proportions of each age slice are
the same in the model as in the real country. Then, the agents are each placed on a grid
(size can be cahnged) with preferential assignment to populated spaces, creating a 
reslisticish distribution of ages and population centers.

Every turn, the agents either move in a random direction (50% probability) or go to their
starting position (50% probability). This assures that the distributions remain constant.
Then, an agent infects other agents on the same space with some probability. This probability
is set as a function of the reproduciton number, which is a parameter of the run.

Infected agents have a chance of dying or recovering each turn, which is set as a function of
their age. The mortality numbers for the different age brackets are based on this article:


RESULTS
We observed two main things runnignt he model. First, despite all of the functionaity we added
to make the model more realistic, the behavior of the susceptible, infected, and recovered 
populations still looked roughly like the output of simpler, container-based models such as the
SIR. So, none of the added functionality did not result in system wide emergent behavior.

Second, infection rates reamined very low for realistic values of reproduciton number. The 
population tended to achieve herd immunity much more quickly than other people have predicted 
for the virus. I am not sure what this means. Maybe there is a bug.
