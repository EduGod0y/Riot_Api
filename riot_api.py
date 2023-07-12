import requests
import time
import pandas as pd


#api_key = 'RGAPI-b0ff987d-2e81-46f1-9a41-f5251765bbe7'

#summoner_name = 'Armstr0ng'

def get_puuid(summoner_name, api_key):
  api_url = ("https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name  )
  api_url = api_url + '?api_key=' + api_key
  resp = requests.get(api_url)
  player_info = resp.json()
  puuid = player_info['puuid']
  Level = player_info['summonerLevel']
  return puuid




def get_matches(puuid, count,api_key, summoner_name):
  puuid = get_puuid(summoner_name,api_key)
  api_url = (
      "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids" + "?type=ranked&" + "start=0&" + "count=" + str(count) + '&api_key=' + api_key)

  resp = requests.get(api_url)
  matches = resp.json()
  return matches

def get_match_data(match_id,  api_key):
  api_url = ('https://americas.api.riotgames.com/lol/match/v5/matches/' +  match_id + '?api_key=' + api_key)

  #while True:
  resp = requests.get(api_url)

    #if resp.status_code == 429:
      #print('Sleeping')
      #time.sleep(10)
      #continue


  data = resp.json()
  return data

def dados(puuid, match_data):

  dict = {}

  part_index = match_data['metadata']['participants'].index(puuid)

  champ = match_data['info']['participants'][part_index]['championName']
  dict['champ'] = champ

  kills = match_data['info']['participants'][part_index]['kills']
  dict['kills'] = kills

  deaths = match_data['info']['participants'][part_index]['deaths']
  if deaths == 0:
    deaths = 1
  dict['deaths'] = deaths

  assists = match_data['info']['participants'][part_index]['assists']
  dict['assists'] = assists

  kda = (kills + assists)/deaths
  kda = round(kda,2)
  dict['kda'] = kda


  win = match_data['info']['participants'][part_index]['win']
  if win == True:
    win = 'Victory'
  if win == False:
    win = 'Defeat'

  dict['win'] = win


  return  dict



def get_stats(summoner_name, api_key):
  puuid = get_puuid(summoner_name, api_key)
  matches = get_matches( puuid,'50',api_key,summoner_name)


  campeao = []
  kills = []
  deaths = []
  assists = []
  kda = []
  ganhador = []
  imagens = []


  for match_id in matches:
    match_data = get_match_data(match_id,  api_key)
    campeao.append(dados(puuid, match_data)['champ'])
    kills.append(dados(puuid, match_data)['kills'])
    deaths.append(dados(puuid, match_data)['deaths'])
    assists.append(dados(puuid, match_data)['assists'])
    kda.append(dados(puuid, match_data)['kda'])
    ganhador.append(dados(puuid, match_data)['win'])
  

  table = {'Champion': campeao, 'Kills': kills, 'Assists': assists, 'Deaths': deaths, 'KDA':kda, 'Win':ganhador}
  df = pd.DataFrame(data=table)
  df2 = df.groupby('Champion')['KDA'].mean().round(2).to_frame().sort_values(by='KDA')
  df3 = df.groupby('Champion').size().sort_values(ascending=True).to_frame()

  win = ganhador.count('Victory')
  defeat = ganhador.count('Defeat')

  winrate = (win/(win+defeat))*100

  return df


#for champ in df.champion:
 # win = ganhador.count('Victory')
  #defeat = ganhador.count('Defeat')

  #winrate = (win/(win+defeat))*100

  #print(str(winrate)+'%')

#image = requests.get('http://ddragon.leagueoflegends.com/cdn/13.13.1/img/champion/Aatrox.png')

#fp = Image.open(image)
#display.display(fp)