##Cette fois-ci il peut être intéressant de ne garder les avis que des personnes qui ont l'habitude
##d'émettre des sentiments partagés, i.e qui ont à peu près autant de tweets positifs que négatifs 
##sur leurs 10 derniers tweets (pour ne pas en récolter trop)

##On peut parcourir tous les tweets collectés, récupérer les id user
##Faire une requête de 10 tweets sur chaque id
##On range sous forme de dico clé: tweet en lien avec notre sujet et valeur: liste des 10 derniers tweets
##On transforme en un dico qui a les mêmes clés mais dont les valeurs sont une liste de scores de pos, neg
##Sur les 10 derniers tweets. Ceux qui ont un écart entre neg et pos supérieur à 1 sont exclus, on ne
##garde que la liste des tweets des autres.
##Il ne restera qu'à comparer avec le score sur l'ensemble des tweets

import tweepy
import pickle as pk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np

#On commmence par se connecter à l'api
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

#On fait une fonction qui lit tous les tweets en lien avec le sujet
def tweet_id(filepath):
    """
    Input: str
    Output: dict
    La fonction prend en argument le chemin du fichier dans lequel sont enregistrés les tweets en lien avec notre sujet
    et retourne un dictionnaire dont les clés sont les tweets et les valeurs sont les identifiants des utilisateurs
    qui ont posté les tweets
    """
    with open(filepath,'rb') as file:
        pickler=pk.Unpickler(file)
        liste=pickler.load()
        
    res={}
        
    for tweet in liste:
        res[tweet['text']]=tweet['user']['id']
        
    return res

#On veut une fonction qui prend en argument un user id et qui retourne les 10 derniers tweets de l'utilisateur 
#en question
def tweet_retrieval(dico,api):
    """
    Input: dict, tweepy api
    Output: dict
    La fonction prend en argument un dictionnaire dont les clés sont les tweets et les valeurs sont les 
    id des émetteurs des tweets, le second est l'api twitter à laquelle nous nous sommes connectés. 
    La fonction retourne le même dictionnaire sauf que les valeurs sont des listes des 10 derniers 
    tweets émis par l'utilisateur dont l'id était la valeur précédente.
    """
    
    for key in dico.keys():
        try:
            dico[key]=api.user_timeline(user_id=dico[key],count=10)
            dico[key]=[x.text for x in dico[key] if x.text[:2]!='RT']
        except tweepy.TweepError:
            None
        
    return dico

#Il faut ensuite une fonction qui fait l'analyse des sentiments exprimés dans les 10 derniers statuts
def user_analysis(dico):
    """
    Input: dict
    Ouput: dict
    La fonction prend en argument un dictionnaire dont les clés sont des tweets et les valeurs les listes
    des 10 derniers tweets émis par l'utilisateur qui a écrit le tweet de la clé.
    On retourne le dico avec les mêmes clés mais dont les valeurs sont des listes de deux flottants
    correspondant respectivement aux scores de positivités et de négativités moyens sur les 10 derniers 
    tweets.
    """
    sid=SentimentIntensityAnalyzer()
    
    for key in dico.keys():
        neg,pos=0.,0.
        for elem in dico[key]:
            neg+=sid.polarity_scores(elem)['neg']
            pos+=sid.polarity_scores(elem)['pos']
        if dico[key]!=[]:
            dico[key]=[neg/len(dico[key]),pos/len(dico[key])]
    return dico

def tweet_analysis(liste):
    """
    Input: list
    Output: list of 3 floats
    La fonction prend en argument une liste de tweets et retoune la liste des 3 scores de polarité
    à savoir neg, neu et pos.
    """
    sid=SentimentIntensityAnalyzer()
    neg,neu,pos=0.,0.,0.
    for tweet in liste:
        ss=sid.polarity_scores(tweet)
        neg+=ss['neg']
        neu+=ss['neu']
        pos+=ss['pos']
    if len(liste) != 0:
        neg,neu,pos=neg/len(liste),neu/len(liste), pos/len(liste)
    else:
        neg, neu, pos = 0, 0, 0
    
    return [neg, neu, pos]
        

#Il faut ensuite une fonction pour faire un affichage comparatif avec et sans cette purge
def combined_display_purge(filepath):
    """
    Input: str
    Output: pyplot histogram
    La fonction prend en argument le chemin au bout duquel se trouve le fichier contenant tous 
    les tweets. Elle retire les tweets d'utilisateurs biaisés selon les critères établis dans
    la fonction purge_biaised_users. Elle affiche l'histogramme comparant ces deux approches pour
    voir si les résultats varient beaucoup
    """
    api=connexion("../credentials/credentials.txt")
    dico=tweet_id(filepath)
    dico2=tweet_retrieval(dico,api)
    
    # On est contraint de prendre un dictionnaire de tweets plus petit pour ne pas faire trop
    # d'appels à l'API. Le programme aurait besoin d'être amélioré
    maxTweets = 90
    keysList = list(dico2.keys())
    smallerDico = []
    for i in range(min([maxTweets, len(keysList)])):
        if i % 30 == 0:
            print(dico2[keysList[i]], keysList[i])
        smallerDico.append((keysList[i], dico2[keysList[i]]))
    smallerDico = {cle: list(valeur) for cle, valeur in smallerDico}
    print(smallerDico)
    
    dico3=user_analysis(smallerDico)
    
    purged=[]
    for key in dico3.keys():
        if dico3[key]!=[] and abs(dico3[key][0]-dico3[key][1])<0.05:
            purged.append(key)
            
    every_tweet=tweet_analysis(list(dico3.keys()))
    purged=tweet_analysis(purged)
    
    #On créé la liste des étqiuettes des absisses
    liste_etiquettes=['negativité','neutralité','positivité'] 
      
    #On segmente les absisses
    liste_positions=np.arange(len(liste_etiquettes))
    
    #On détermine la largeur de la barre
    bar_width=0.20
    
    #On ajoute les barres
    plt.bar(liste_positions, purged, bar_width, color='pink')
    plt.bar(liste_positions+bar_width,every_tweet,bar_width,color='purple')
    
    #Etiquettes des absisses
    plt.xticks(liste_positions+bar_width*0.5, liste_etiquettes)
    
    #Absisses
    plt.xlabel('Sentiment', fontsize=10,color='blue')
    
    #Ordonnées
    plt.ylabel('Présence', fontsize=10,color='blue')
    
    #On ajoute la légende
    plt.legend(['Sans les biaisés','Tout le monde'])
    
    #Titre
    plt.title("Analyse de sentiment sur Tweeter \n selon qu'on retire les personnes biaisées ou non", fontsize=12, color='grey')
    plt.show()
    
    
# Attention, si la base de tweets est trop grande, le programme fait un trop grand nombre d'appels 
# à l'api et renvoit une erreur, ça vaut le coup de recréer un fichier avec moins de tweets et de le passer
# en argument de la fonction. Je n'avais pas eu le temps de développer un solution moins "bricolage"
 
cheminTweets = "../data/tweets/" + "exempleTweetsTransformes.txt" 
#cheminTweets = "../data/tweets/" + "cocaTweetsTransformes.txt"  

combined_display_purge(cheminTweets)

