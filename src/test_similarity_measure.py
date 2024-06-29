from similarity import similarity_sr_ar

st_route = {"id": "s1",
            "route": [
                {
                    "from": "Livorno",
                    "to": "Verona",
                    "merchandise": {
                        "chocolate": 11,
                        "cereals": 8,
                    }
                },
                {
                    "from": "Verona",
                    "to": "Foggia",
                    "merchandise": {
                        "beer": 29,
                        "canned beans": 29,
                        "toothpaste": 30,
                    }
                },
                {
                    "from": "Foggia",
                    "to": "Cuneo",
                    "merchandise": {
                        "beer": 29,
                        "canned beans": 29,
                        "toothpaste": 30,
                    }
                }

            ]
            }

ac_route = {"id": "s1",
            "route": [
                {
                    "from": "Livorno",
                    "to": "Verona",
                    "merchandise": {
                        "chocolate": 11,
                        "cereals": 8,
                    }
                },
                {
                    "from": "Verona",
                    "to": "Roma",
                    "merchandise": {
                        "beer": 29,
                        "canned beans": 29,
                        "toothpaste": 30,
                    }
                },
                {
                    "from": "Roma",
                    "to": "Foggia",
                    "merchandise": {
                        "beer": 28,
                        "canned beans": 28,
                        "toothpaste": 29,
                    }
                },
                {
                    "from": "Bari",
                    "to": "Foggia",
                    "merchandise": {
                        "water": 28,
                        "canned beans": 10,
                        "hot water": 29,
                    }
                }


            ]
            }

print(similarity_sr_ar(st_route, ac_route, w1=0.5))

