# Dataset number
dataset_number = 1


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
    "Carpi", "Cuneo", "Lucca", "Altamura", "Imola", "Aprilia", "Carabanchel", "Cremona",
    "Molfetta", "Faenza", "Baggio", "Mazara del Vallo", "Biella", "Castelfranco Veneto",
    "Civitavecchia", "Acilia-Castel Fusano-Ostia Antica", "Rho", "Sesto San Giovanni",
    "Pordenone", "Gallarate", "Asti", "Legnano", "Busto Arsizio", "Fano"
]
print('Number of cities: ', len(cities))


cities_for_replacement = None


merchandise_types = [
    "milk", "pens", "butter", "honey", "tomatoes", "eggs", "cheese", "bread",
    "apples", "chicken", "rice", "sugar", "coffee", "tea", "chocolate", "flour",
    "water", "juice", "wine", "beer", "toothpaste", "shampoo", "soap", "salt",
    "pepper", "cereals", "toilet paper", "garlic", "onions", "potatoes", "pasta",
    "canned beans", "olive oil", "ketchup", "mayonnaise", "mustard", "soda", "yogurt",
    "ice cream", "bananas", "orange juice", "lettuce", "carrots", "broccoli", "onions",
    "cucumbers", "bell peppers", "avocado"
]

print('Number of merchandise types: ', len(merchandise_types))

ndrivers = 30
drivers = ['D' + str(i) for i in range(1, ndrivers+1)]
print('Number of drivers: ', len(drivers))


# Set parameters to generate the routes (to understand what these parameters are,
# look at the documentation of the function generate_random_routes)

# Standard routes
NUM_SROUTES = 100  # Number of SRs
MINNCITIES = 3  # Min number of cities in a SR
MAXNCITIES = 6  # Max number of cities in a SR
MAXNUMITEMS = 10  # Max number of items in a SR trip
MAXQUANTITY = 30  # Max quantity for merchandise items

# Actual routes
AVERAGE_NUM_ACTUAL = 400  # Average number of ARs to generate for each SR
ST_DEV_ACTUAL = 20  # Standard deviation for the number of ARs to generate for each SR
P_CITIES_REPLACE = 0.2  # Percentage of cities to replace in the actual routes
P_MOD = 0.5  # Percentage of merchandise items to modify
P_QUANT_CHANGE = 0.5  # Percentage of items that have their quantity adjusted (among the ones to modify)
P_ADD = 0.2  # Probability of adding a city from an AR
P_REMOVE = 0.2  # Probability of removing a city from an AR

RANDOM_SEEDS = [6, 9, 86]
USE_REPLACEMENT_SET = False
