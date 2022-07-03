import json

with open("data.json", "r", encoding='utf-8') as f:
	chalList = json.load(f)
	
def printJSON(data):
	print(json.dumps(data, ensure_ascii=False, indent=4))

for chal in chalList:
	if '3' in chal['description']:
		printJSON(chal)
