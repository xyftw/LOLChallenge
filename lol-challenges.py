import os, re
import requests, json
import argparse


requests.packages.urllib3.disable_warnings()

header = "LeagueOfLegendsClient/12.12.448.6653"
def printJSON(data):
	print(json.dumps(data, ensure_ascii=False, indent=4))
def getAuth(folder, sucPrint=True, errPrint=True):
	if os.path.isdir(folder):
		for file in sorted(os.listdir(folder),reverse=True):
			reLog = re.match(r'.+?_LeagueClientUx\.log', file)
			if reLog:
				try:
					with open("{}\\{}".format(folder,file), 'r', encoding="utf-8") as data:
						reAuth = re.search(r'(https://riot:.+?@127\.0\.0\.1:\d+?)/(index|bootstrap)\.html\"', data.read())
				except:
					with open("{}\\{}".format(folder,file), 'r') as data:
						reAuth = re.search(r'(https://riot:.+?@127\.0\.0\.1:\d+?)/(index|bootstrap)\.html\"', data.read())
				if reAuth:
					auth = reAuth.group(1).strip()
					print("已獲取AuthInfo：{}\n".format(auth)) if sucPrint else print(end="")
					return auth
	print("錯誤：無法從LOL安裝路徑獲取授權資訊，請嘗試輸入安裝路徑。") if errPrint else print(end="")
	return False
def getParser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--dir", "--folder", default="C:\\Garena\\Games\\32775\\Game\\Logs\\LeagueClient Logs")
	parser.add_argument("-t", "--token",  default="")
	return parser
def getChampDict(auth):
	# /lol-game-data/assets/v1/champion-icons/1.png
	# https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/1.png
	url = auth + "/lol-champions/v1/owned-champions-minimal"
	res = requests.get(url, verify=False).json()

	
	champDict = { int(champ['id']): [ champ['name'], champ['alias'] ] for champ in res }
	champDict[895] = ["淣菈" , "Nilah"]
	with open("champ.json", "w", encoding='utf-8') as f:
		json.dump(champDict, f, indent=4, ensure_ascii=False)
	roleDict = {'mage':[], 'fighter':[], 'tank':[], 'assassin':[], 'support':[], 'marksman':[]}
	for champ in res:
		for role in champ['roles']:
			roleDict[role].append(int(champ['id']))
	return champDict, roleDict
def getChallenges(auth):
	# /lol-game-data/assets/assets/challenges/config/303401/tokens/challenger.png
	# https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/challenges/config/303401/tokens/challenger.png
	url = auth + "/lol-challenges/v1/challenges/local-player"
	res = requests.get(url, verify=False).json()
	chalList = []
	targetList = ["availableIds", "description", "descriptionShort", "levelToIconPath", "name", "thresholds"]
	for chal in res:
		if chal['category'] == "TEAMWORK":
			#if chal['availableIds'] or chal['name'] == "同業俱樂部":
			if chal['availableIds']:
				chalList += [ {key: value for key, value in chal.items() if key in targetList} ]
			#if chal['name'] == "同業俱樂部":
			#	printJSON(chal)
	return chalList

def output2CSV():
	jsonData = []
	with open("challenge.tsv", "w", encoding='utf8') as data:
		for chal in chalList:
			description = chal['descriptionShort'].replace("<em>", "").replace("</em>", "")
			byEng = sorted(chal['availableIds'], key = lambda x: (champDict[x][1], x)) # 照英文排序
			tmpListCH = [ champDict[champ][0] for champ in byEng ]
			data.write(f"{chal['name']}\t{description}\t{len(byEng)}\t{','.join(tmpListCH)}\n")
			jsonData.append({'name':chal['name'], 'description':description, 'idList':byEng, 'ZHList':tmpListCH, 'icon':chal['levelToIconPath']['CHALLENGER'].lower()})
		for role in roleDict:
			byEng = sorted(roleDict[role], key = lambda x: (champDict[x][1], x)) # 照英文排序
			tmpListCH = [ champDict[champ][0] for champ in byEng ]
			data.write(f"{role}\t\t{len(byEng)}\t{','.join(tmpListCH)}\n")
			jsonData.append({'name':f"{role}", 'description':description, 'idList':byEng, 'ZHList':tmpListCH, 'icon':"/lol-game-data/assets/ASSETS/Challenges/Config/303408/Tokens/CHALLENGER.png".lower()})
	with open("data.json", "w", encoding='utf-8') as f:
		json.dump(jsonData, f, indent=4, ensure_ascii=False)
	
		
def main():
	global champDict, chalList, roleDict
	parser = getParser()
	args = parser.parse_args()
	auth = getAuth(args.dir)
	champDict, roleDict = getChampDict(auth)
	chalList = getChallenges(auth)
	output2CSV()




if __name__ == '__main__':
	main()
