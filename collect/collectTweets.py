# Ce script permet de collecter des tweets en continu en réponse à une certaine requête (par exemple un nom d'entreprise)

import pickle as pk
import tweepy
import tweepy.api
import time
import json

#Connexion à l'API
def connexion(filepath):
    """
    Input: str
    Output: api tweepy
    La fonction prend en argument le chemin du fichier python au bout duquel se trouve le fichier 
    contenant les identifiants pour se connecter à l'api
    """
    with open(filepath,'rb') as file:
        pickler=pk.Unpickler(file)
        [consumer_key,consumer_secret,access_key,access_secret]=pickler.load()
        
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api=tweepy.API(auth)
    
    return api

# Une fonction qui permet de savoir si on a déjà collecté un tweet
def is_in_doc(doc,nb):
    with open(doc,"r") as document :
        req = document.readlines()
        for i in range(len(req)):
            if int(req[i]) == nb :
                return True
    return False

# Après s'être connecté, on veut pouvoir récupérer et enregistrer les tweets
def tweet_extraction(filepath1,filepath2,api,query):
    """
    Input: str, str, api tweepy, str
    Output: None
    La fonction enregistre les tweets dans le document dont le chemin est passé en premier argument
    et enregistre les identifiants dans le fichier passé en deuxième argument. Le troisième argument
    est l'api à partir de laquelle on récupère les tweets. Le dernier argument est la recherche effectuée
    sur les tweets
    """

    #ouverture des deux fichiers utiles : celui qui recense les tweets sous format json; celui qui recense les id pour ne pas avoir de doublons
    fichier = open(filepath1, "a")
    ident = open(filepath2,"a")
    
    #boucle de recherche avec gestion d'erreur : si trop de requêtes sont effectuées, le programme s'arrête pendant 15 minutes
    while True :
        try :
            #Recherche de Tweets
            max_tweets = 180
            public_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    
            for tweet in public_tweets:
                if tweet.lang == "en" and not is_in_doc(filepath2,tweet.id):
                    ident.write(str(tweet.id)+"\n")
                    json_str = json.dumps(tweet._json)
                    print(tweet.text)
                    fichier.write(json_str)
                    fichier.write("\n"+"\n")
                    
        except tweepy.TweepError as e:
            print(e.reason+"\n :"+"Pas trop de requêtes à la fois ! Il faut attendre 15 minutes...")
            time.sleep(900)

# Changer les valeurs d'exemple par ce que vous voulez
cheminFichierTweets = "../data/tweets/" + "exempleTweets.txt"
cheminFichierTweetsId = "../data/tweets/" + "exempleTweetsId.txt"
cheminCredentials = "../credentials/credentials.txt"
requete = "exemple"

# Lancer l'exécution de la ligne ci-dessous pour collecter des tweets

tweet_extraction(cheminFichierTweets, cheminFichierTweetsId, connexion(cheminCredentials), requete)

# Il faut forcer l'arrêt du programme pour arrêter la collecte : ce n'est pas optimal mais les fonctions de collecte 
# n'étaient pas censées être arrêtées pendant le projet. Nous devions récolter un maximum de tweets.




