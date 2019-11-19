class Genome:
    def __init__(self):
        self._gens = {}
        self._gens['dna'] = []
        self._gens['cdna'] = []
        self._gens['cds'] = []

    def add_gen(self, gen):
        self._gens[gen.type].append(gen)
