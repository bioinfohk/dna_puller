from dna_puller.gen import GenType


class DataAddress:
    BASE_ADDRESS = 'ftp.ensembl.org/pub/release-98/fasta/'

    ADDRESSES = {
        GenType.DNA: '/dna/',
        GenType.CDNA: '/cdna/',
        GenType.CDS: '/cds/'
    }

    def __init__(self, species_name, type: GenType):
        self.species_name = species_name
        self.type = type

        self.address = DataAddress.BASE_ADDRESS + species_name + DataAddress.ADDRESSES[type]
