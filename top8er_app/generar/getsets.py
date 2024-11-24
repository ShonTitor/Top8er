import requests, json, os
from datetime import datetime
from django.conf import settings

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

def check_event(slug) :
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
    #print(event)
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
    print(url, slug, type(slug), org)
    try:
        response = requests.get(url, headers=headers)
        datos = json.loads(response.content)
    except Exception:
        print(response.content)
        return False
    
    if "tournament" in datos :
        return True
    else :
        return False

def get_tonamel_token(force_new=False) :
    global tonamel_token

    if not(tonamel_token is None or force_new):
        return tonamel_token

    if force_new:
        print("Renewing tonamel token")

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


if __name__ == "__main__":
    #from perro import generate_banner
    #slug = "tournament/genesis-7-1/event/ultimate-singles"
    #slug = "tournament/combo-breaker-2019/event/skullgirls-2nd-encore"
    #slug = "tournament/ceo-2019-fighting-game-championships/event/super-smash-bros-ultimate-singles"
    #slug = "tournament/bowser-castle-1/event/smash-ultimate-singles"
    slug = "tournament/frosty-faustings-xii-2020/event/under-night-in-birth-exe-late-st"

    print(check_event(slug))
    d = event_data(slug)
    print(d)
    #if d : generate_banner(d).show()

    #print(check_challonge(slug))
    #challonge_data(slug)

    #slug = "PnKAm"
    #print(check_tonamel(slug))
    #print(tonamel_data(slug))
