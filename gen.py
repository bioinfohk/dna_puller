class Gen:
    def __init__(self, type, sequence, data_object):
        self.type = type
        self.sequence = sequence
        self.data_object = data_object

class GenType:
    CDNA = 'cdna'
    DNA = 'dna'
    CDS = 'cds'

class DnaType:
    dna = '.dna.'
    dna_sm = '.dna_sm.'
    dna_rm = '.dna_rm.'
