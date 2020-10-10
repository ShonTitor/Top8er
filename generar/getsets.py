import requests, json, os
from datetime import datetime

# Cosas de smash gg
path = os.path.realpath(__file__)
path= os.path.abspath(os.path.join(path, os.pardir))
f = open(os.path.join(path, "smashgg.apikey"), "r")
authToken = f.read()
f.close()
apiVersion = 'alpha'
url = 'https://api.smash.gg/gql/' + apiVersion
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer '+authToken
           }
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
    if event :
        if event["numEntrants"] >= 8 :
            return True
    else :
        return False

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
    #print(data)
    data = data["data"]
    if data["event"] is None : return None
    char_data = json.loads(requests.get(url="https://api.smash.gg/characters").content)
    for node in data["event"]["sets"]['nodes'] :
        if node["games"] is None : continue
        for game in node["games"] :
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
                players.append({"tag" : name,
                               "char" : (char, 0),
                                "twitter" : twi,
                                "secondaries" : []
                               })
    event = data["event"]
    btext = []
    if event["startAt"] :
        fecha = datetime.fromtimestamp(event["startAt"])
        fecha = fecha.strftime("%m/%d/%y")
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
        link = "https://smash.gg/"+event["tournament"]["shortSlug"]
    else :
        link = "smash.gg/"+event["tournament"]["slug"]

    datos = {
        "players" : players,
        "toptext" : ttext,
        "bottomtext" : btext,
        "url" : link
        }
    return datos


if __name__ == "__main__":
    from perro import generate_banner
    slug = "tournament/genesis-7-1/event/ultimate-singles"
    #slug = "tournament/ceo-2019-fighting-game-championships/event/super-smash-bros-ultimate-singles"
    #slug = "tournament/bowser-castle-1/event/smash-ultimate-singles"
    #slug = "https://smash.gg/tournament/genesis-7-1/event/ultimate-singles/brackets/719802/1162721"

    print(check_event(slug))
    d = event_data(slug)
    print(d)
    if d : generate_banner(d).show()
