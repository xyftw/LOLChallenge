from pywebio import start_server, config, session
from pywebio.input import input, FLOAT
from pywebio.output import *
from pywebio.output import *

import json
from functools import partial

PORT = 8080

config(theme="sketchy", title="LOL Team Challenge Helper", description="英雄聯盟挑戰系統陣容小幫手",)

def printJSON(data):
	print(json.dumps(data, ensure_ascii=False, indent=4))

def main():
	with open("data.json", "r", encoding='utf-8') as f:
		chalList = json.load(f)
	with open("champ.json", "r", encoding='utf-8') as f:
		champDict = json.load(f, object_hook=lambda d: {int(k) if k.isdigit() else k: v for k, v in d.items()})
	chalNameList = [chal['name'] for chal in chalList]

	selectList = []

	isMobile = session.info.user_agent.is_mobile
	COLNUM = 2 if isMobile else 4

	def onSelect(action, choice):
		clear(scope='display')
		# 點擊反應
		if action == "select":
			if choice not in selectList:
				selectList.append(choice)
		if action == "remove":
			if choice in selectList:
				selectList.remove(choice)
		# 產生新的選單，並顯示
		putList = []
		for i in range(len(chalList)):
			if i % COLNUM ==0: curList = []
			if i in selectList:
				curList += [f"{chalList[i]['name']}{'' if chalList[i]['all5'] else '³'}", put_buttons([dict(label='✔', value='remove', color='dark')], onclick=partial(onSelect, choice=i), scope='select')]
			else:
				curList += [f"{chalList[i]['name']}{'' if chalList[i]['all5'] else '³'}", put_buttons([dict(label='✔', value='select', color='light')], onclick=partial(onSelect, choice=i), scope='select')]
			if i % COLNUM == COLNUM-1 or i==29: putList.append(curList)
		clear('select')
		put_table([['名稱', '選擇']*COLNUM]+putList, scope='select')
		# 產生交集列表
		if selectList:
			champSet, avaiSet= -1, -1
			for select in selectList:
				if champSet == -1: 
					champSet = set(chalList[select]['idList'])
				else:
					champSet = champSet & set(chalList[select]['idList'])
				if chalList[select]['all5']:
					if avaiSet == -1: 
						avaiSet = set(chalList[select]['idList'])
					else:
						avaiSet = avaiSet & set(chalList[select]['idList'])
			champList = sorted(list(champSet), key= lambda x: (champDict[x][1], x)) # 照英文排序
			champListZH = [ champDict[champ][0] for champ in champList ]
			if avaiSet != -1:
				avaiChampList = sorted(list(avaiSet), key= lambda x: (champDict[x][1], x)) # 照英文排序
				avaiChampListZH = [ champDict[champ][0] for champ in avaiChampList ]
			#put_text(f"{','.join(champListZH)}", scope="display")

		
		if selectList:
			for select in selectList:
				imageUrl = chalList[select]['icon'].replace("/lol-game-data/assets", "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default")
				put_image(imageUrl, scope='display', width= ("20%" if isMobile else "10%") )
			put_markdown(f"## 目前選擇：{'、'.join([chalList[i]['name'] for i in selectList])}", scope='display')
			put_markdown(f"### 完全符合「所有條件」的英雄({len(champListZH)})：`{','.join(champListZH)}`", scope='display')
			for champId in champList:
				put_image(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champId}.png", scope='display')
			if avaiSet != -1 and (champSet & avaiSet):
				put_markdown(f"### 符合「必選條件」的英雄({len(avaiChampListZH)})：`{','.join(avaiChampListZH)}`", scope='display')
				for champId in avaiChampList:
					put_image(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champId}.png", scope='display')


		if len(selectList) > 1:
			countDict = {key: [] for key in champDict.keys()}
			selectCnt = 0
			for select in selectList:
				if not chalList[select]['all5']:
					tmpSet = avaiSet & set(chalList[select]['idList']) if avaiSet != -1 else set(chalList[select]['idList'])
					tmpList = sorted(list(tmpSet), key= lambda x: (champDict[x][1], x)) # 照英文排序
					tmpListZH = [ champDict[champ][0] for champ in tmpList ]
					put_markdown(f"### `{chalList[select]['name']}` 需要從以下{len(tmpListZH)}英雄中選擇至少3個英雄：`{','.join(tmpListZH)}`", scope='display')
					for champId in tmpList:
						countDict[champId].append(chalList[select]['name'])
						#put_image(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champId}.png", scope='display')
					selectCnt += 1
			availDict = {count: [] for count in range(selectCnt-1, 1, -1)}
			for champId in countDict:
				if len(countDict[champId]) in availDict.keys():
					availDict[len(countDict[champId])].append(champId)
			for availCnt in availDict:
				tmpList = sorted(list(availDict[availCnt]), key= lambda x: (champDict[x][1], x)) # 照英文排序
				tmpListZH = [ champDict[champ][0] for champ in tmpList ]
				if len(tmpList):
					put_markdown(f"### 以下{len(tmpList)}個英雄符合{selectCnt}個「可選條件」中的{availCnt}個條件，推薦使用：`{','.join(tmpListZH)}`", scope='display')
					for champId in tmpList:
						put_image(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champId}.png", scope='display')


	putList = []
	for i in range(len(chalList)):
		if i % COLNUM ==0: curList = []
		curList += [f"{chalList[i]['name']}{'' if chalList[i]['all5'] else '³'}", put_buttons([dict(label='✔', value='select', color='light')], onclick=partial(onSelect, choice=i))]
		if i % COLNUM == COLNUM-1 or i==29: putList.append(curList)
	clear()
	put_scope('select')
	put_table([['名稱', '選擇']*COLNUM]+putList, scope='select')
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