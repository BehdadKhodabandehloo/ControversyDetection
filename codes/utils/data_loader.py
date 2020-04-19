import bigjson
from bigjson.filereader import FileReader
import json

class Dataloader:
    def __init__(self, base_path):
        self.base_path = base_path
        self.dataset = None

    def load_files(self, file, size=None):
        self.bigjson_load(file, size=size)
        return self.dataset

    def bigjson_load(self, file, size=None):
        self.dataset = []
        with open('%s/%s.json' % (self.base_path, file), mode='rb') as outfile:
            if size is None:
                self.dataset = json.load(outfile)
            elif type(size) == int:
                temp = bigjson.load(outfile)
                count = 0
                while count != size:
                    self.dataset.append(temp[count].to_python())
                    count += 1


if __name__ == '__main__':
    file = 'baltimore_data'
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file, 1000)
    print(len(dataset))
    print(dataset[0])

