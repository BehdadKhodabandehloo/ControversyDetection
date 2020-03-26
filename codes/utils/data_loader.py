import bigjson
from bigjson.filereader import FileReader


class Dataloader:
    def __init__(self, base_path):
        self.base_path = base_path
        self.datasets = {}

    def load_files(self, files, size=None):
        if type(files) == list:
            for file in files:
                self.bigjson_load(file, size)
        elif type(files) == str:
            self.bigjson_load(files, size=size)
        return self.datasets

    def bigjson_load(self, file, size=None):
        self.datasets[file] = []
        with open('%s/%s.json' % (self.base_path, file), mode='rb') as outfile:
            if size is None:
                file_reader = FileReader(file=outfile)
                self.datasets[file] = file_reader.read(read_all=True, to_python=True)
            elif type(size) == int:
                temp = bigjson.load(outfile)
                count = 0
                while count != size:
                    self.datasets[file].append(temp[count].to_python())
                    count += 1


if __name__ == '__main__':
    files = 'baltimore_data'
    dataloader = Dataloader('/root/tweets_dataset')
    datasets = dataloader.load_files(files, 1000)
    print(len(datasets['baltimore_data']))
    print(datasets['baltimore_data'][0])

