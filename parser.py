from Bio.SeqIO.FastaIO import FastaIterator

class Parser:
  
  @staticmethod
  def parse_file(file_path):
    records_letters = {}
    with open(file_path) as in_handle:
        for record in FastaIterator(in_handle):
            records_letters[record.id] = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'Y': 0, 'M': 0, 'S': 0, 'R': 0, 'W': 0,
                                          'K': 0, 'N': 0, 'D': 0, 'B': 0, 'H': 0, 'V': 0, 'all': 0}
            for letter in record.seq:
                records_letters[record.id][letter] += 1
                records_letters[record.id]['all'] += 1
    return records_letters
