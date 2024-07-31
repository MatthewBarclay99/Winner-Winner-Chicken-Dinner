import requests
from datetime import datetime

baseURL = {'baseball':"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=",
           'hockey':"https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard?dates=",
           'soccer':"https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard?dates="}



cfa_text = "Free Chic-fil-a sandwich! Open the app before midnight."

def scoreAtLeast(teamData,score, dummy):
    return int(teamData.get('score'))>=score

def winGame(teamData,dummy, dummy2):
    return bool(teamData.get('winner'))

def shutout(dummy, dummy2, oppData):
    return int(oppData.get('score'))==0

Angels = {'ID':"3",
          'sport':"baseball",
          'rewards':[{'rewardFUN':scoreAtLeast,
                    'minScore':7,
                    'homeReq':True,
                    'reward_text':cfa_text},
                    {'rewardFUN':shutout,
                    'homeReq':False,
                    'reward_text':"Free 6in pizza from Mountain Mike's"}
                    ]
          }
Dodgers = {'ID':"19",
           'sport':"baseball",
           'rewards':[{'rewardFUN':winGame,
                    'homeReq':True,
                    'reward_text':"$5 Panda Express plate! Use promo code 'DODGERSWIN'"}
                    ]
          }
Ducks =   {'ID':"134846",
           'sport':"hockey",
         'rewards':[{'rewardFUN':scoreAtLeast,
                    'minScore':5,
                    'homeReq':True,
                    'reward_text':cfa_text}
                    ]
         }
LAFC = {'ID':"136050",
        'sport':"soccer",
        'rewards':[{'rewardFUN':winGame,
                    'homeReq':True,
                    'reward_text':cfa_text}
                    ]
        }


def get_league_scores_today(baseURL, date):
    request = requests.get(baseURL+date)
    return request.json().get('events')




def find_team_result(league_results, team_id):
    found = False
    team = ""
    opponent = ""
    for i, event_dict in enumerate(league_results):
        for j, competition_dict in enumerate(event_dict.get('competitions')):
            for k, competitors_dict in enumerate(competition_dict.get('competitors')):
                if(competitors_dict.get('id')==team_id):
                    found=True
                    team=competitors_dict
                else:
                    opponent=competitors_dict
            if found:
                break
        if found:
            break
    return team, opponent



def get_API(teamID, sport):
    API_URL = baseURL.get(sport)
    today = '20240725'#datetime.today().strftime('%Y%m%d')
    league_scores = get_league_scores_today(API_URL, today)
    return find_team_result(league_scores, teamID)


def printRewards(rewardDict):
    todays_rewards = []
    rewardCounter=0
    for team in rewardDict:
        teamData, opponentData = get_API(team.get('ID'), team.get('sport'))
        if(teamData!=""):
            for reward_i in team.get('rewards'):
                if(reward_i.get('rewardFUN')(teamData,reward_i.get('minScore'),opponentData)):
                    if(reward_i.get('homeReq') & bool(teamData.get('homeAway')!="home")):
                        break
                    todays_rewards.append(reward_i.get('reward_text'))
                    rewardCounter+=1
    print("Today you have " + str(rewardCounter) + " rewards available to redeem:")
    for text in todays_rewards: 
        print(text)

rewards = [Angels,Dodgers,Ducks,LAFC]
printRewards(rewards)





