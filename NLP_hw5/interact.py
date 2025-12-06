import torch
import torch.nn.functional as F
from torch.optim import AdamW
from torch.utils.data import Dataset, TensorDataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM

device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = AutoTokenizer.from_pretrained("./theTunedModel")
model = AutoModelForCausalLM.from_pretrained("./theTunedModel")
model.to(device)

model.eval()

print('##################################')
print("enter text for prompt")
print("'.x' to quit")
print("'.t [number]' to change temp")
print("'.k [number]' to change top k")
print("'.l [number]' to change generated # of tokens")

temp = 5
k= 50
length = 150
print(f'temp = {temp}')
print(f'k = {k}')
print(f'generated length = {length}')
print('##################################')
while(True):

	cmd = input("$: ").strip()
	if cmd == '.x':
		break
	elif cmd[0:2] == '.t':
		temp = float(cmd.split()[1])
		print(f'temp = {temp}')
	elif cmd[0:2] == '.k':
		k = int(cmd.split()[1])
		print(f'k = {k}')
	elif cmd[0:2] == '.l':
		length = int(cmd.split()[1])
		print(f'generated length = {length}')

	else:
		encoded = tokenizer(cmd, return_tensors='pt')
		encoded = encoded.to(device)

		for n in range(length):
			out = model(**encoded)
			nextLogits = out.logits[0,-1,:] #must be squoozen or dived into to access logits
			values, indices = torch.topk(nextLogits, k=k,dim=0)
			
			values = values/temp
			probs = F.softmax(values,dim=0)
			i = torch.multinomial(probs,1,replacement=False)
			nextEncoded = indices[i]
			
			#add on new token
			inputs = encoded['input_ids']
			att = encoded['attention_mask']
			newToken = torch.tensor([[nextEncoded]],device=inputs.device)
			newMaskElem = torch.tensor([[1]],device=att.device)

			newInputs = torch.cat([inputs,newToken],dim=1)
			newAtt = torch.cat([att,newMaskElem],dim=1)
			
			#update encoded
			encoded['input_ids'] = newInputs
			encoded['attention_mask'] = newAtt
			print('---------------------------------------')
			print(tokenizer.decode(encoded['input_ids'][0]))
		












