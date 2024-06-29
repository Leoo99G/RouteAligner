# I generate 50 standard routes and for each SR I generate around 150 actual routes.
# Here I use 50 cities to create the standard routes and the initial actual routes.
# Then I have a separate , smaller list of cities that I use to modify the actual routes
# and induce some repetitions (frequent modifications).

# Dataset number
dataset_number = 2

# 50 cities
cities = [
    "Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence",
    "Bari", "Catania", "Venice", "Verona", "Messina", "Padua", "Trieste", "Brescia",
    "Taranto", "Prato", "Reggio Calabria", "Modena", "Parma", "Reggio Emilia",
    "Perugia", "Livorno", "Cagliari", "Foggia", "Ravenna", "Rimini", "Salerno",
    "Ferrara"
]
print('Number of cities: ',len(cities))

cities_for_replacement = [
    "Baggio", "Baggio", "Baggio", "Baggio", "Baggio", "Baggio",
    "Carpi","Carpi","Carpi","Carpi",
    "Cuneo", "Cuneo",
    "Lucca",
    "Altamura",
    "Imola",
    "Aprilia",
    "Cremona",
    "Molfetta",
    "Faenza"
]
print('Number of cities for replacement: ',len(cities_for_replacement))


merchandise_types = [
    "milk", "pens", "butter", "honey", "tomatoes", "eggs", "cheese", "bread",
    "apples", "chicken", "rice", "sugar", "coffee", "tea", "chocolate", "flour",
    "water", "juice", "wine", "beer", "toothpaste", "shampoo", "soap", "salt",
    "pepper", "cereals", "toilet paper", "garlic", "onions", "potatoes", "pasta",
    "canned beans", "olive oil", "ketchup", "mayonnaise", "mustard", "soda", "yogurt",
    "ice cream", "bananas", "orange juice", "lettuce", "carrots", "broccoli", "onions",
    "cucumbers", "bell peppers", "avocado"
]
print('Number of merchandise types: ',len(merchandise_types))

ndrivers = 20
drivers = ['D' + str(i) for i in range(1, ndrivers+1)]
print('Number of drivers: ',len(drivers))


# Set parameters to generate the routes (to understand what these parameters are,
# look at the documentation of the function generate_random_routes)
NUM_SROUTES = 100
MINNCITIES = 3
MAXNCITIES = 6
MAXNUMITEMS = 8
MAXQUANTITY = 30

AVERAGE_NUM_ACTUAL = 400
ST_DEV_ACTUAL = 20
P_CITIES_REPLACE = 0.6
P_MOD = 0.5
P_QUANT_CHANGE = 0.5
P_ADD = 0.4
P_REMOVE = 0.4

RANDOM_SEEDS = [5, 367, 9827]
USE_REPLACEMENT_SET = True
