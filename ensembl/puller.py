from dna_puller.gen import GenType

class Puller:
    def __init__(self, species, type: GenType):
        self.species = []
        self.add_species(species)
        self.type = type

    def add_species(self, species):
        for speciess in species:
            self.species.append(speciess)
