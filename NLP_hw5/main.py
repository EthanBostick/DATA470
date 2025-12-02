from tqdm import tqdm
import torch
import torch.nn.functional as F
from torch.optim import AdamW
from torch.utils.data import Dataset, TensorDataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
import sys
import time

#import other files
from prep import *

#helper functions#
def iter_encode_chunks(tokenizer, text, chunk_chars=2000):
	for i in range(0, len(text), chunk_chars):
		piece = text[i:i+chunk_chars]
		toks = tokenizer.encode(piece, add_special_tokens=False)
		yield toks

def datanize(encoded,k):
	inputs = encoded[:-1].unfold(0,k,k)
	targets = encoded[1:].unfold(0,k,k)

	return TensorDataset(inputs,targets)
##################


#variable settings#
device = 'cuda' if torch.cuda.is_available() else 'cpu'
batchSize = int(sys.argv[2]) if len(sys.argv)>2 else (2 if device=='cpu' else 16)
eta = float(sys.argv[3]) if len(sys.argv)>3 else 0.0005
epochs = int(sys.argv[4]) if len(sys.argv)>4 else 99999999
blockSize = int(sys.argv[5]) if len(sys.argv)>5 else 128

###################

#show vars
print(f'utilizing {device}')
print(f'batch size = {batchSize}')
print(f'eta = {eta}')
print(f'epochs = {epochs}')
print(f'block size = {blockSize}')

#get tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
model.to(device)

#attempt to grab corp from args
if len(sys.argv) <=1:
	print('no corpus path given')
	sys.exit()
else:
	path = sys.argv[1]	

try:
	print(f'loading corpus from "{path}"')
	with open(path, "r", encoding="utf-8") as f:
		text = f.read()
	print('--success--')
except(Exception):
	print(f'load from "{path}" failed')
	sys.exit()

#tokenize
encoded = []
for chunk in tqdm(iter_encode_chunks(tokenizer, text),total=len(text)//2000+1,desc="tokenizing"):
    encoded.extend(chunk)
encoded = torch.tensor(encoded, dtype=torch.long)		

#split (input,target) dataset
ds = datanize(encoded,blockSize)

loader = DataLoader(ds,batch_size=batchSize,shuffle=True) #data loader stuff
optimizer = AdamW(model.parameters(),eta) #optimizer

#training loopy
model.train()
for ep in range(epochs):
	for ins, tars in tqdm(loader,desc=f"Epoch {ep+1}",leave=False):
		ins = ins.to(device)
		tars = tars.to(device)	

		#zero
		optimizer.zero_grad()

		out = model(ins,labels=tars)
		loss = out.loss
		loss.backward()
		optimizer.step()

model.save_pretrained()
tokenizer.save_pretrained()

