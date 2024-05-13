#Chicken Tracker
import requests
baseURL = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id="
AngelsID = "135258"
DodgersID = "135272"
request = requests.get(baseURL+AngelsID)
AngelsData = request.json().get('results')
#print(request.status_code)
AngelsData[0].get('idHomeTeam')



def get_API(baseURL, teamID):
    request = requests.get(baseURL+teamID)
    #print(request.status_code)
    teamData = request.json().get('results')
    if(teamData[0].get('idHomeTeam')!=teamID):
        return ""

    #for game in teamData:
        
    return teamData[0]

AngelsData = get_API(baseURL, AngelsID)
print(int(AngelsData.get('intHomeScore'))>=7)
DodgersData = get_API(baseURL,DodgersID)
print(int(DodgersData.get('intHomeScore'))>=int(DodgersData.get('intAwayScore')))