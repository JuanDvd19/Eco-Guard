class Animal:
    def __init__(self, name, species, zone):
        self.name = name
        self.species = species
        self.zone = zone


    def summary(self):
        return f"{self.name} ({self.species}) - Zona: {self.zone.name}"