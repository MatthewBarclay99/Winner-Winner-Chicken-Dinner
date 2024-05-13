import requests
from datetime import datetime

baseURL = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id="

def scoreAtLeast(teamData,score):
    return int(teamData.get('intHomeScore'))>=score

def winGame(teamData,dummy):
    return (int(teamData.get('intHomeScore'))>=int(teamData.get('intAwayScore')))

Angels = {'ID':"135258",
          'rewards':[{'rewardFUN':scoreAtLeast,
          'minScore':7,
          'reward_text':"Free Chic-fil-a sandwich!"}]
          }
Dodgers = {'ID':"135272",
          'rewards':[{'rewardFUN':winGame,
          'reward_text':"$5 Panda Express plate! Use promo code 'DODGERSWIN'"}]
          }
Ducks =   {'ID':"134846",
         'rewards':[{'rewardFUN':scoreAtLeast,
         'minScore':5,
         'reward_text':"Free Chic-fil-a sandwich!"}]
         }
LAFC = {'ID':"136050",
        'rewards':[{'rewardFUN':winGame,
        'reward_text':"Free Chic-fil-a sandwich!"}]
        }



def get_API(baseURL, teamID):
    request = requests.get(baseURL+teamID)
    #print(request.status_code)
    teamData = request.json().get('results')
    #must be home team
    if(teamData[0].get('idHomeTeam')!=teamID):
        return ""
    #must be today's game
    if(teamData[0]!=datetime.today().strftime('%Y-%m-%d')):
        return ""  
    return teamData[0]

def printRewards(rewardDict):
    todays_rewards = []
    rewardCounter=0
    for team in rewardDict:
        teamData = get_API(baseURL,team.get('ID'))
        if(teamData!=""):
            for reward_i in team.get('rewards'):
                if(reward_i.get('rewardFUN')(teamData,reward_i.get('minScore'))):
                    todays_rewards.append(reward_i.get('reward_text'))
                    rewardCounter+=1
    print("Today you have " + str(rewardCounter) + " rewards available to redeem:")
    for text in todays_rewards: 
        print(text)

rewards = [Angels,Dodgers,Ducks,LAFC]
printRewards(rewards)
