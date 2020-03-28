import pickle as pk
import json

# Les tweets enregistrés contiennent des données qui ne sont pas pertinentes pour notre analyse
# On ne va garder que les attributs qui sont suceptibles de nous intéresser pour alléger les fichiers manipulés


def retrieve_tweets(filepath):
    """
    Input: str
    Output: list of dict
    La fonction prend le chemin du fichier contenant les tweets au format json en argument et retourne 
    une liste de dictionnaires des tweets en ne gardant que les attributs qui nous intéressent
    parmi les tweets.
    """
    attributs=['created_at','id','text','user','coordinates','quoted_status','retweeted_status','quote_count','retweet_count','reply_count','favorite_count']
    tweets=[]
    with open(filepath,'r') as file:
        ligne=file.readline()
        while ligne!="*STOP*":
            if ligne.replace(" ","") not in ["","\n"]:
                try:
                    json_token=json.loads(ligne.rstrip('\n'))
                    dico={}
                    for cle in json_token.keys():
                        if cle in attributs:
                            dico[cle]=json_token[cle]                    
                    tweets.append(dico)
                except json.JSONDecodeError:
                    None
            ligne=file.readline()
    return tweets

def save_tweets(liste_tweets,filepath):
    """
    Input: list of dict, str
    Output: None
    La fonction enregistre la liste contenant les dictionnaires des tweets dans un document .txt
    qui se trouve au bout du chemin spécifié en second argument
    """
    with open(filepath,'wb') as file:
        mon_pickler=pk.Pickler(file)
        mon_pickler.dump(liste_tweets)
        
def save_tweets_json(liste_tweets,filepath):
    """
    Input: list of dict, str
    Output: None
    La fonction enregistre la liste contenant les dictionnaires des tweets dans un document .txt
    qui se trouve au bout du chemin spécifié en second argument
    """
    with open(filepath,'a') as file:
        for tweet in liste_tweets:
            jsonString = json.dumps(tweet)
            file.write(jsonString)
            file.write("\n\n")

      
# Remplacer les exemples par les bonnes valeurs
cheminTweetsBruts = "../data/tweets/" + "exempleTweets.txt"   # Assurez-vous d'avoir bien écrit "*STOP*" à la fin de ce fichier après l'exécution du script
cheminTweetsTransformes = "../data/tweets/" + "exempleTweetsTransformes.txt"
cheminTweetsJson = "../data/tweets/" + "exempleTweetsJson.txt" # Assurez-vous d'avoir bien écrit "*STOP*" à la fin de ce fichier après l'exécution du script

# Il ne suffit d'exécuter ce fichier qu'une seule fois pour que la transformation opère
save_tweets(retrieve_tweets(cheminTweetsBruts), cheminTweetsTransformes)
save_tweets_json(retrieve_tweets(cheminTweetsBruts), cheminTweetsJson)     
    
        
    
    





