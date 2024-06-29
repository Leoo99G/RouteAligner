# Dataset number
dataset_number = 4

# 50 cities
cities = [
    "Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence",
    "Bari", "Catania", "Venice", "Verona", "Messina", "Padua", "Trieste", "Brescia",
    "Taranto", "Prato", "Reggio Calabria", "Modena", "Parma", "Reggio Emilia",
    "Perugia", "Livorno", "Cagliari", "Foggia", "Ravenna", "Rimini", "Salerno",
    "Ferrara", "Sassari", "Latina", "Giugliano in Campania", "Monza", "Syracuse",
    "Bergamo", "Pescara", "Trento", "Forlì", "Vicenza", "Terni", "Bolzano", "Novara",
    "Piacenza", "Ancona", "Andria", "Udine", "Arezzo", "Cesena", "Lecce", "Pesaro",
    "Barletta", "Alessandria", "La Spezia", "Pisa", "Catanzaro", "Cosenza", "Potenza",
    "Avellino", "Caserta", "Olbia", "Como", "Brindisi", "Grosseto", "Pistoia",
    "Pomezia", "Varese", "Asti", "Fiumicino", "Casoria", "Cinisello Balsamo",
    "Trapani", "Guidonia Montecelio", "Aversa", "Castellammare di Stabia", "Massa",
    "Carabanchel", "Cremona",
    "Molfetta", "Faenza", "Mazara del Vallo", "Biella", "Castelfranco Veneto",
    "Civitavecchia", "Acilia-Castel Fusano-Ostia Antica", "Rho", "Sesto San Giovanni",
    "Pordenone", "Gallarate", "Asti", "Legnano", "Busto Arsizio", "Fano"
]
print(len(cities))

cities_for_replacement = [
    "Baggio",
    "Carpi",
    "Cuneo",
    "Lucca",
    "Altamura",
    "Imola",
    "Aprilia"
]
print(len(cities_for_replacement))


merchandise_types = [
    "milk", "pens", "butter", "honey", "tomatoes", "eggs", "cheese", "bread",
    "apples", "chicken", "rice", "sugar", "coffee", "tea", "chocolate", "flour",
    "water", "juice", "wine", "beer", "toothpaste", "shampoo", "soap", "salt",
    "pepper", "cereals", "toilet paper", "garlic", "onions", "potatoes", "pasta",
    "canned beans", "olive oil", "ketchup", "mayonnaise", "mustard", "soda", "yogurt",
    "ice cream", "bananas", "orange juice", "lettuce", "carrots", "broccoli", "onions",
    "cucumbers", "bell peppers", "avocado"
]
print(len(merchandise_types))


ndrivers = 20
drivers = ['D' + str(i) for i in range(1, ndrivers+1)]
print(len(drivers))


# Set parameters to generate the routes (to understand what these parameters are,
# look at the documentation of the function generate_random_routes)
NUM_SROUTES = 100
MINNCITIES = 5
MAXNCITIES = 10
MAXNUMITEMS = 7
MAXQUANTITY = 30

AVERAGE_NUM_ACTUAL = 400
ST_DEV_ACTUAL = 20
P_CITIES_REPLACE = 0.8
P_MOD = 0.7
P_QUANT_CHANGE = 0.7
P_ADD = 0.6
P_REMOVE = 0.7

RANDOM_SEEDS = [993, 544, 285]
USE_REPLACEMENT_SET = True