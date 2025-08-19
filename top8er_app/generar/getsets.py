import requests
import json
import time

from datetime import datetime
from django.conf import settings
from django.core.cache import cache

from thefuzz import process

from top8er_app.cached_functions import get_sgg_char_data, game_data_from_json

# Cosas de smash gg
authToken = settings.START_GG_API_KEY
apiVersion = 'alpha'
url = 'https://api.smash.gg/gql/' + apiVersion
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + authToken
           }

# Cosas de challonge
challonge_key = settings.CHALLONGE_API_KEY

# Cosas de tonamel
tonamel_credentials = settings.TONAMEL_API_KEY
tonamel_token = None

def check_event(slug):
    query = '''
    query SetsQuery($slug: String) {
        event(slug: $slug) {
          numEntrants
        }
    }
    '''
    payload = {"query" : query, "variables" : {"slug" : slug}}
    response = requests.post(url=url, headers=headers, json=payload)
    event = json.loads(response.content)["data"]["event"]
    if event :
        if event["numEntrants"] >= 8 :
            return True
    else :
        return False

def check_challonge(slug, org=None) :
    headers = { 'User-Agent': 'Top8er' }
    if org is not None:
        slug = org+"-"+slug
    url = "https://api.challonge.com/v1/tournaments/" + slug + ".json?api_key=" + challonge_key + "&include_participants=1"
    try:
        response = requests.get(url, headers=headers)
        datos = json.loads(response.content)
    except Exception:
        return False
    
    if "tournament" in datos :
        return True
    else :
        return False

def get_tonamel_token(force_new=False) :
    global tonamel_token

    if not(tonamel_token is None or force_new):
        return tonamel_token

    headers = {
                "Authorization": f"Basic {tonamel_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
    data = {
                "redirect_uri": "https://127.0.0.1?grant_type=authorization_code",
                "grant_type": "client_credentials"
            }

    r = requests.post("https://op.tonamel.com/oauth2/token",
                    headers=headers, data=data)

    access_token = json.loads(r.content)['access_token']
    tonamel_token = access_token
    return access_token

def check_tonamel(competition_id) :
    access_token = get_tonamel_token()

    headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
    url = f"https://op.tonamel.com/api/v1/competition_result/{competition_id}"

    r = requests.get(url, headers=headers)
    
    if r.status_code == 401:
        access_token = get_tonamel_token(force_new=True)
        headers["Authorization"] = f"Bearer {access_token}"
        r = requests.get(url, headers=headers)
                        
    return r.status_code == 200

def tonamel_data(competition_id) :
    access_token = get_tonamel_token()

    headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }

    r = requests.get(f"https://op.tonamel.com/api/v1/competition_result/{competition_id}",
                    headers=headers)
    data = json.loads(r.content)
    players = [
        {
            "tag" : p['participant'].get('entry_name', p['participant']['player_name']),
            "char" : ("Random", 0),
            "twitter" : "",
            "secondaries" : []
        }
        for p in data["places"]
    ]

    datos = {
        "players" : players,
        "toptext" : "",
        "bottomtext" : "",
        "url" : f"https://tonamel.com/competition/{competition_id}",
        "game" : "idk"
        }
    return datos

def event_query(slug) :
    query = '''
    query SetsQuery($slug: String) {
        event(slug: $slug) {
          id
          name
          numEntrants
          state
          startAt
          videogame {id}
          tournament { name city slug shortSlug}

          standings(query: {
            page: 1
            perPage: 8
            sortBy: "standing"
          }){
            nodes{
              placement
              entrant{
                name
                participants {
                  user {
                    authorizations(types:TWITTER) {
                      externalUsername
                    }
                  }
                }
              }
            }
          }
        
          sets(page: 1, perPage: 11, sortType: RECENT) {
            nodes {
              games {
                selections {
                  entrant {name}
                  selectionValue
                }
              }
            } 
          }
        }
    	}
    '''
    payload = {"query" : query, "variables" : {"slug" : slug}}
    response = requests.post(url=url, headers=headers, json=payload)
    return json.loads(response.content)

def event_data(slug) :
    freq = {}
    data = event_query(slug)
    data = data["data"]
    try :
        if data["event"] is None : return None
        char_data = json.loads(requests.get(url="https://api.smash.gg/characters").content)
        for node in data["event"]["sets"]['nodes'] :
            if node["games"] is None : continue
            for game in node["games"] :
                if game["selections"] :
                    for selection in game["selections"] :
                        player = selection["entrant"]["name"]
                        char = selection["selectionValue"]
                        if player in freq :
                            if char in freq[player] :
                                freq[player][char] += 1
                            else :
                                freq[player][char] = 1
                        else :
                            freq[player] = {char : 1}

        most = {}
        search = set()
        for player, chars in freq.items() :
            chargg = -1
            freqgg = -1
            for char, f in chars.items() :
                if f > freqgg :
                    freqgg = f
                    chargg = char
            most[player] = chargg
            search.add(chargg)

        char_names = {}
        for c in char_data["entities"]["character"] :
            if c["id"] in search :
                char_names[c["id"]] = c["name"]
        char_names[-1] = "Random"

        vaina = {p:char_names[i] for p,i in most.items()}
    except :
        vaina = {}
    players = []
    for p in data["event"]["standings"]["nodes"] :
                name = p["entrant"]["name"]
                if not name in vaina  :
                    vaina[name] = "Random"
                twi = None
                P = p["entrant"]["participants"]
                if len(p["entrant"]["participants"]) == 1 :
                    if P[0]["user"] and P[0]["user"]["authorizations"] :
                        twi = "@"+P[0]["user"]["authorizations"][0]["externalUsername"]
                char = vaina[name].replace(".", "")
                if char == "Pokemon Trainer" : char = "Pokémon Trainer"
                if char == "Ori" : char = "Ori and Sein"
                if char == "Erika Wagner" : char = "Wagner"
                players.append({"tag" : name,
                               "char" : (char, 0),
                                "twitter" : twi,
                                "secondaries" : []
                               })
    event = data["event"]
    gid = int(event["videogame"]["id"])
    if gid in [1,2,3,4,5,1386] : game = "ssbu"
    else : game = "roa"
    btext = []
    if event["startAt"] :
        fecha = datetime.fromtimestamp(event["startAt"])
        fecha = fecha.strftime("%y/%m/%d")
        btext.append(fecha)
    if event["tournament"]["city"] :
        ciudad = event["tournament"]["city"]
        btext.append(ciudad)
    btext.append(str(event["numEntrants"])+" Participants")
    btext = " - ".join(btext)
    ttexts = [event["tournament"]["name"], " - " + event["name"], " - Top 8"]
    ttext = ""

    
    for t in ttexts  :
        if len(ttext) + len(t) < 50 :
            ttext += t
    if event["tournament"]["shortSlug"] :
        link = "https://start.gg/"+event["tournament"]["shortSlug"]
    else :
        link = "start.gg/"+event["tournament"]["slug"]

    datos = {
        "players" : players,
        "toptext" : ttext,
        "bottomtext" : btext,
        "url" : link,
        "game" : game
        }
    return datos

def challonge_data(slug, org=None) :
    headers = { 'User-Agent': 'Top8er' }
    if org:
        slug = f'{org}-{slug}'
    url = "https://api.challonge.com/v1/tournaments/"+slug+".json?api_key="+challonge_key+"&include_participants=1"
    response = requests.get(url, headers=headers)
    datos = json.loads(response.content)
    if "tournament" in datos :
        datos = datos["tournament"]
    else :
        return False

    
    players = [p["participant"] for p in datos["participants"]]
    npart = len(players)
    players = [(p["final_rank"], p["name"])
               for p in players]
    if all(not p[0] is None for p in players) :
        players.sort()
    players = [p[1] for p in players[:8]]
    players = [{"tag" : p,
               "char" : ("Random", 0),
               "twitter" : "",
               "secondaries" : []
               } for p in players]
    ttext = datos["name"] + " - Top 8"

    if "complete_at" in datos :
        btext = " - ".join([datos["completed_at"][:10].replace('-','/'), str(npart)+" participants"])
    else :
        btext = str(npart)+" participants"
    url_torneo = datos['full_challonge_url']
    
    datos = {
        "players" : players,
        "toptext" : ttext,
        "bottomtext" : btext,
        "url" : url_torneo,
        "game" : "idk"
        }
    return datos

def check_sgg(slug) :
    query = '''
    query CompletedQuery($slug: String) {
        event(slug: $slug) {
          numEntrants
          state
        }
    }
    '''
    payload = {"query" : query, "variables" : {"slug" : slug}}
    response = requests.post(url=url, headers=headers, json=payload)
    event = json.loads(response.content)["data"]["event"]
    if event is None :
      return None
    if event["numEntrants"] \
       and event["numEntrants"] > 0 \
       and event["state"] == "COMPLETED" :
            return True
    else :
        return False

def sgg_query(slug) :
    query = '''
    query StandingsQuery($slug: String) {
      event(slug: $slug) {
        id
        name
        numEntrants
        state
        startAt
        videogame {
          id
        }
        tournament {
          name
          countryCode
          slug
          shortSlug
          city
          images {
            type
            url
          }
        }
        standings(query: {page: 1, perPage: 16, sortBy: "standing"}) {
          nodes {
            placement
            entrant {
              name
              participants {
                user {
                  discriminator
                  authorizations(types: TWITTER) {
                    externalUsername
                  }
                }
              }
            }
          }
        }
      }
    }
    '''
    payload = {"query" : query, "variables" : {"slug" : slug}}
    response = requests.post(url=url, headers=headers, json=payload)
    return json.loads(response.content)

def sgg_sets_query(slug) :
    query = '''
    query SetsQuery($slug: String, $page: Int) {
      event(slug: $slug) {
        sets(page: $page, perPage: 50, sortType: MAGIC) {
          nodes {
            games {
              selections {
                entrant {
                  name
                }
                selectionValue
              }
            }
          }
        }
      }
    }
    '''
    sets = []
    page = 1
    max_page = 3
    while True:
        payload = {"query" : query, "variables" : {"slug" : slug, "page": page}}
        response = requests.post(url=url, headers=headers, json=payload)
        data = json.loads(response.content)
        new_sets = data["data"]["event"]["sets"]["nodes"]
        if len(new_sets) == 0:
            break
        sets += new_sets
        page += 1
        if page > max_page:
            break
        time.sleep(1)

    return sets

def sgg_char_freq(sets, gameId):
    char_dict = get_sgg_char_data().get(gameId, {})

    freq = {}

    for node in sets:
        if node["games"] is None : continue
        for game in node["games"] :
            if game["selections"] :
                for selection in game["selections"] :
                    player = selection["entrant"]["name"]
                    char = selection["selectionValue"]
                    if player in freq :
                        if char in freq[player] :
                            freq[player][char] += 1
                        else :
                            freq[player][char] = 1
                    else :
                        freq[player] = {char : 1}
    return {
      key:sorted([(v, char_dict.get(gameId, {}).get(k, k)) for k,v in value.items()], reverse=True)
      for key, value in freq.items()
    }

def sgg_data(slug, game=None):
    if game:
        game_data = game_data_from_json(game)

    character_data = get_sgg_char_data()

    data = sgg_query(slug)
    data = data["data"]
    sets = sgg_sets_query(slug)
    gameId = data["event"]["videogame"]["id"]

    char_freq = sgg_char_freq(sets, gameId)

    players = []
    for p in data["event"]["standings"]["nodes"] :
      name = p["entrant"]["name"]
      twi = None
      position = p["placement"]
      tag = name
      if " | " in tag:
          tag = tag.split(" | ")[-1]

      P = p["entrant"]["participants"]

      if not twi and len(p["entrant"]["participants"]) == 1 :
        if P[0]["user"] and P[0]["user"]["authorizations"] :
          twi = "@"+P[0]["user"]["authorizations"][0]["externalUsername"]

      if not twi:
          twi = ""
      
      char_id = char_freq.get(name, [(0, None)])[0][1]
      char = character_data.get(gameId, {}).get(char_id)

      possible_chars = list(game_data["characters"]) if game else []
      if game and char is not None and char not in possible_chars and len(possible_chars) > 0:
          print("toca fuzzy con el personaje", char)
          p = process.extract(char, possible_chars, limit=1)
          print(f"{char} => {p[0][0]}")
          char = p[0][0]
          
      if len(possible_chars) == 0:
          char = None

      if char is not None:
          char = (char, 0)
              
      if game and type(char) is tuple and char[0] not in possible_chars and len(possible_chars) > 0:
          print("toca fuzzy con el personaje parte 2", char[0])
          p = process.extract(char[0], possible_chars, limit=1)
          print(f"{char[0]} => {p[0][0]}")
          char = (p[0][0], char[1])

      players.append({
        "tag" : name,
        "twitter" : twi,
        "position": position,
        "char": char
      })

    event = data["event"]
    if event["tournament"]["countryCode"] :
        country = event["tournament"]["countryCode"]
    else : country = None
    name = event["tournament"]["name"] + " - " + event["name"]

    if event["tournament"]["shortSlug"] :
        link = "https://www.start.gg/"+event["tournament"]["shortSlug"]
    else :
        link = "https://www.start.gg/"+event["tournament"]["slug"]

    ttext = f"{event['tournament']['name']} - {event['name']}"
    btext = []
    if event["startAt"] :
        fecha = datetime.fromtimestamp(event["startAt"])
        fecha = fecha.strftime("%Y/%m/%d")
        btext.append(fecha)
    if event["tournament"]["city"] :
        ciudad = event["tournament"]["city"]
        btext.append(ciudad)
    btext.append(str(event["numEntrants"])+" Participantes")
    btext = " - ".join(btext)

    datos = {
        "players" : players,
        "name" : name,
        "url" : link,
        "country" : country,
        "participants_number": event["numEntrants"],
        "toptext": ttext,
        "bottomtext": btext,
        "gameId": gameId
        }
    return datos