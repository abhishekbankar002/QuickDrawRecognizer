import random
import numpy as np
import torch
import torch.optim as optim
from torch.nn import functional as F
from torch.utils.data import Dataset

import config
import customDataLoader
import CNN


def train(model, use_cuda, train_loader, optimizer, epoch):
	model.train()

	for batch_idx, (data, target) in enumerate(train_loader):

		if use_cuda:
			data, target = data.cuda(), target.cuda()

		optimizer.zero_grad()
		output = model(data)

		loss = F.cross_entropy(output, target)
		loss.backward()
		optimizer.step()

		if batch_idx % 100 == 0:
			print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
				epoch, batch_idx * len(data), len(train_loader.dataset),
				       100. * batch_idx / len(train_loader), loss.item()))


def test(model, use_cuda, test_loader):
	model.eval()

	test_loss = 0
	correct = 0

	with torch.no_grad():
		for data, target in test_loader:

			if use_cuda:
				data, target = data.cuda(), target.cuda()

			output = model(data)

			# test_loss += torch.sum((output - y_onehot) ** 2)
			test_loss += F.cross_entropy(output, target, reduction='sum')
			pred = output.argmax(dim=1, keepdim=True)

			correct += pred.eq(target.view_as(pred)).sum().item()

	test_loss /= len(test_loader.dataset)

	print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
		test_loss, correct, len(test_loader.dataset),
		100. * correct / len(test_loader.dataset)))


def seed(seed_value):
	torch.cuda.manual_seed_all(seed_value)
	torch.manual_seed(seed_value)
	torch.cuda.manual_seed(seed_value)
	np.random.seed(seed_value)
	random.seed(seed_value)
	torch.backends.cudnn.benchmark = False
	torch.backends.cudnn.deterministic = True


if __name__ == "__main__":

	use_cuda = True
	seed(config.seed)
	train_loader = torch.utils.data.DataLoader(customDataLoader.customDatasetClass(config.path + 'train'),
	                                           num_workers=config.numWorkers['train'], shuffle=True,
	                                           batch_size=config.batchSize['train'])
	test_loader = torch.utils.data.DataLoader(customDataLoader.customDatasetClass(config.path + 'test'),
	                                          num_workers=config.numWorkers['test'],
	                                          shuffle=False,
	                                          batch_size=config.batchSize['test'])
	model = CNN.Net()
	if use_cuda:
		model = model.cuda()

	optimizer = optim.Adam(model.parameters(), lr=config.lr)

	for epoch in range(1, config.epochs + 1):
		train(model, use_cuda, train_loader, optimizer, epoch)
		test(model, use_cuda, test_loader)

	torch.save(model.state_dict(), "quickdraw.pt")

	dummy_input = torch.rand(1, 1, 64, 64).cuda()
	torch.onnx.export(model, dummy_input, 'model.onnx', verbose=True, input_names=['data'], output_names=['output'])
	model.load_state_dict(torch.load('quickdraw.pt'))
