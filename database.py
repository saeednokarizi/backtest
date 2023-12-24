import h5py
import os

class Hdf5Client:
    def __init__(self, exchange: str):
        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.hf = h5py.File(f"{directory}/{exchange}.h5", 'a')
        self.hf.flush()