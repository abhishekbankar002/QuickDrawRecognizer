import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
path = 'GoogleDataImages_'
lr = 1e-03

seed = 0
epochs = 5

batchSize = {
	'train': 50,
	'test': 10
}

numWorkers = {
	'train': 3,
	'test': 3
}
