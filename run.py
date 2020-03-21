from world import World
from countrycodes import country_codes
from scraper import DataGetter
from visualize import Visualize

# interesting parameters to play with
country_code = country_codes['United States']  # change this and see what happens

scale = 1000  # scales the input population to this size

max_number_runs = 50  # the model will terminate after this many runs even if it hasn't finished. Necessary in case
# herd immunity develops.
reproduction_number = 10


# parameters with mostly technical applications

world_size = (10, 10)  # bigger world runs faster, but less happens
max_contacts_per_day = 10


# run model
print("getting data...")
scraper = DataGetter(country_code=country_code)

print("generating model...")
model = World(scraper.get_data(scale=scale), rnumber=reproduction_number, world_size=world_size,
              contacts=max_contacts_per_day)

print("running model...")
model.run(max_times=max_number_runs)

print("creating visualizations...")
draw = Visualize()
draw.draw_everything(model)
