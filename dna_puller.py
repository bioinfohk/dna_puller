import requests, sys
from ftplib import FTP
from dna_puller.parser import Parser
import os, shutil
import gzip
import json, time


class DnaPuller:
    def __init__(self, species, jsons = True, remove_data = True, types = ['dna', 'cdna', 'cds']):
        self.species = species
        self.types = types
        self.data = {}
        self.jsons = jsons
        self.remove_data = remove_data

    def download_and_parse_data(self):
        for speciess in self.species:
            os.mkdir(speciess)
            self.data[speciess] = {}
            for type in self.types:
                ftp = FTP('ftp.ensembl.org')
                ftp.login()
                print('getting ' + type + ' for ' + speciess)
                self.data[speciess][type] = {}
                
                dirs = self.ftp_cwd(speciess.lower(), type)
                print(dirs)
                
                ftp.cwd(self.ftp_cwd(speciess.lower(), type))

                self.filenames = []
                ftp.retrlines('NLST', callback=self.validate_name)
                
                if len(self.filenames) == 0:
                  ftp.retrlines('NLST', callback=self.validate_name_toplevel)

                os.mkdir(speciess + '/' + type)
                for filename in self.filenames:
                    print('download file: ' + filename)
                    file_path = os.path.join(speciess, type, filename)
                    fasta_path = os.path.join(speciess, type, filename[0:-3])
                    with open(file_path, 'wb') as file:
                        ftp.retrbinary('RETR ' + filename, file.write, 102400)
                    handle = gzip.open(file_path)
                    with open(fasta_path, 'wb') as out:
                        for line in handle:
                            out.write(line)
                    self.data[speciess][type].update(Parser.parse_file(fasta_path))
            if self.jsons:        
              json_path = os.path.join('jsons' ,speciess + '.json')
              print('creating ' + json_path)
              with open(json_path, 'w') as fp:
                json.dump(self.data[speciess], fp)
            if self.remove_data:    
              print('removing ' + os.path.join(speciess))  
              shutil.rmtree(os.path.join(speciess))
            ftp.quit()
            time.sleep(5)        
              
     
    def ftp_cwd(self, species, type):
        return '/pub/release-98/fasta/' + species + '/' + type + '/'

    def validate_name(self, name):
        for type in self.types:
            if ('.' + type + '.' in name) and ('.toplevel.' not in name) and ('.nonchromosomal.' not in name) and ('.MT.' not in name) and ('.abinitio.' not in name) and ('.alt.' not in name):
                self.filenames.append(name)
              
    def validate_name_toplevel(self, name):
        for type in self.types:
            if ('.' + type + '.' in name) and ('.toplevel.' in name) and ('.nonchromosomal.' not in name) and ('.MT.' not in name) and ('.abinitio.' not in name)and ('.alt.' not in name):
                self.filenames.append(name)          

    @staticmethod
    def get_species(klass_species):
        url_names = []
        server = "https://rest.ensembl.org"
        ext = "/info/genomes/taxonomy/"+ klass_species +"?"

        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        for json_data in r.json():
            url_names.append(json_data['url_name'])

        return url_names
      
