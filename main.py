from pywebio import start_server
from pywebio.input import input, FLOAT
from pywebio.output import *

import json
from functools import partial

PORT = 8080

def printJSON(data):
	print(json.dumps(data, ensure_ascii=False, indent=4))

def main():
	with open("data.json", "r", encoding='utf-8') as f:
		chalList = json.load(f)
	with open("champ.json", "r", encoding='utf-8') as f:
		champDict = json.load(f, object_hook=lambda d: {int(k) if k.isdigit() else k: v for k, v in d.items()})
	chalNameList = [chal['name'] for chal in chalList]

	selectList = []
	def onSelect(action, choice):
		clear(scope='display')
		if action == "select":
			if choice not in selectList:
				selectList.append(choice)
		if action == "remove":
			if choice in selectList:
				selectList.remove(choice)
		if selectList:
			champSet= {}
			for select in selectList:
				if not champSet: 
					champSet = set(chalList[select]['idList'])
				else:
					champSet = champSet & set(chalList[select]['idList'])
			champList = sorted(list(champSet), key= lambda x: (champDict[x][1], x)) # 照英文排序
			champListZH = [ champDict[champ][0] for champ in champList ]

	#put_text("You click %s button ar row %s" % (action, choice), scope='display')
		put_text(f"目前選擇：{'、'.join([chalList[i]['name'] for i in selectList])}", scope='display')
		if selectList:
			put_text(f"可用英雄({len(champListZH)})：{','.join(champListZH)}", scope='display')

	putList = []
	for i in range(len(chalList)):
		if i % 3 ==0: curList = []
		curList += [chalList[i]['name'], put_buttons([dict(label='✔', value='select', color='light'), dict(label='❌', value='remove', color='light')], onclick=partial(onSelect, choice=i))]
		if i % 3 == 2: putList.append(curList)
	clear()

	put_table([['名稱', '動作', '名稱', '動作', '名稱', '動作']]+putList)
	put_scope('display')

if __name__ == '__main__':
	import argparse
	from pywebio.platform.tornado_http import start_server as start_http_server
	from pywebio import start_server as start_ws_server

	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--port", type=int, default=8080)
	parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
	args = parser.parse_args()

	if args.http:
		start_http_server(main, port=args.port)
	else:
		# Since some cloud server may close idle connections (such as heroku),
		# use `websocket_ping_interval` to  keep the connection alive
		start_ws_server(main, port=args.port, websocket_ping_interval=30)
	#start_server(main)