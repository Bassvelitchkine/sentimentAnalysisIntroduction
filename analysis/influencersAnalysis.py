#Le but de se fichier est de combiner l'analyse des graphes à l'analyse de sentiments
#En effet, l'objectif est de déterminer quel est le sentiment général d'un groupe d'utilisateurs
#qui comptabilisent les plus hauts scores selon certains critères de centralité: nombre de followers, k-core, etc.

#Je pensais pouvoir inclure plusieurs critères de centralité mais en fait c'est très compliqué car il faut 
#une vue d'ensemble du graphe et de toutes les connexions ou alors d'un sous graphe qui contient tous
#les émetteurs des tweets collectés. Il y a de fortes chances pour qu'on fasse le tour de la Terre de 
#cette façon, donc mauvaise idée... On ne peut garder que le nombre de followers comme critère de centralité

#Pour valider l'approche, il faut collecter des tweets, regarder le sentiment sur l'ensemble des tweets,
#et le comparer au sentiment prédits sur les utilisateurs les plus influents selon ces critères uniquement


##INSTRUCTION

#Pour faire tourner ce code on a seulement besoin d'avoir le fichier twitt.txt dans le même dossier
#twitt.txt contient les tweets que nous avons collectés au format json

import pickle as pk
import numpy as np
import matplotlib.pyplot as plt
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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


def load_tweets(filepath):
    """
    Input: str
    Output: list of tweets
    La fonction prend en argument le chemin au bout duquel se trouve le fichier qui contient les 
    tweets collectés et retourne l'objet dans lequel se trouvent les tweets
    """
    
    with open(filepath,'rb') as file:
        pickler=pk.Unpickler(file)
        tweets=pickler.load()
        
    return tweets

#La première mesure de centralité que nous allons utiliser est le nombre de followers
#On va d'abord construire une liste de tuple (nombre de followers de l'émetteur, tweet)
    
def build_tuples(tweets):
    """
    Input: list of dict
    Output: list of tuples (int,str)
    La fonction prend en argument une liste de tweets (avec toutes les infos liées au tweet dans un
    dictionnaire). On veut créer la liste des tuples (nombre de followers de l'émetteur, texte du 
    tweet) triée par ordre décroissant du nombre de followers
    """
    res=[]
    for tweet in tweets:
        res.append((tweet['user']['followers_count'],tweet['text']))
    return sorted(res,key=lambda tup: tup[0],reverse=True)

def extract_best_tweets(tweets):
    """
    Input: list of dict
    Output: list of str
    La fonction prend en argument la liste des tweets collectés sous leur forme originelle avant
    de retourner les 50 tweets émanants des utilisateurs avec le plus grand nombre de 
    followers
    """
    list_tuples=build_tuples(tweets)
    res=[]
    for i in range(min(100, len(list_tuples))):
        res.append(list_tuples[i][1])
    return res

def tweet_statistics_ponder(tweets):
    """
    Input: list of str
    Output: list of float
    La fonction prend en argument les tweets qu'on a collectés. Elle retourne une liste contenant
    trois flottants qui correspondent aux sommes des scores de négativité, de neutralité et de 
    positivité pondérés par le score de "mélange" de chaque tweet.
    """
    sid = SentimentIntensityAnalyzer()
    neg,neu,pos=0.,0.,0.
    
    for tweet in tweets:
        ss = sid.polarity_scores(tweet)
        r=ss['compound']
        if r<0:
            r=1
        neg+=ss['neg']*r
        neu+=ss['neu']*r
        pos+=ss['pos']*r
    
    if neg + neu + pos > 0:
        norm=(1/(neg+neu+pos))
        return [neg*norm,neu*norm,pos*norm]
    else:
        return [0, 0, 0]

def every_tweet(tweets):
    """
    Input: list of dict
    Output: list of str
    La fonction prend en argument la liste de tous les tweets et des informations qui 
    leur sont rattachées pour retourner la liste des textes des tweets
    """
    res=[]
    for tweet in tweets:
        res.append(tweet['text'])
    return res
    
def display_intensity(liste):
    """
    Input: list of floats
    Output: pyplot histogram
    La fonction prend en argument les valeurs de négativité de neutralité et de positivité
    qui ont été attribué à chaque tweet et retourne l'histogramme
    """    
    #On créé la liste des étqiuettes des absisses
    liste_etiquettes=['negativité','neutralité','positivité'] 
      
    #On segmente les absisses
    liste_positions=np.arange(len(liste_etiquettes))
    
    #On détermine la largeur de la barre
    bar_width=0.30
    
    #On ajoute les barres
    plt.bar(liste_positions, liste, bar_width, color='pink')
    
    #Etiquettes des absisses
    plt.xticks(liste_positions, liste_etiquettes)
    
    #Absisses
    plt.xlabel('Sentiment', fontsize=10,color='blue')
    
    #Ordonnées
    plt.ylabel('Présence', fontsize=10,color='blue')
    
    #Titre
    plt.title("Sentiment analysis of the #metoo hashtag on Twitter \n according to a built-in intensity analyzer", fontsize=12, color='grey')
    plt.show()

def combined_display_followers(filepath):
    """
    Input: str
    Output: pyplot histogram
    La fonction prend en argument le chemin au bout duquel se trouve le fichier contenant tous 
    les tweets. Elle fait l'analyse de sentiment de tous les tweets et des 100 tweets des utilisateurs
    avec le plus de followers seulement. Elle affiche l'histogramme comparant ces deux approches pour
    voir si on n'est pas trop loin de la réalité
    """
    best=tweet_statistics_ponder(extract_best_tweets(retrieve_tweets(filepath)))
    everyone=tweet_statistics_ponder(every_tweet(retrieve_tweets(filepath)))
    
    #On créé la liste des étqiuettes des absisses
    liste_etiquettes=['negativité','neutralité','positivité'] 
      
    #On segmente les absisses
    liste_positions=np.arange(len(liste_etiquettes))
    
    #On détermine la largeur de la barre
    bar_width=0.20
    
    #On ajoute les barres
    plt.bar(liste_positions, best, bar_width, color='pink')
    plt.bar(liste_positions+bar_width,everyone,bar_width,color='purple')
    
    #Etiquettes des absisses
    plt.xticks(liste_positions+bar_width*0.5, liste_etiquettes)
    
    #Absisses
    plt.xlabel('Sentiment', fontsize=10,color='blue')
    
    #Ordonnées
    plt.ylabel('Présence', fontsize=10,color='blue')
    
    #On ajoute la légende
    plt.legend(['Les (au plus 100) meilleurs','Tout le monde'])
    
    #Titre
    plt.title("Analyse de sentiment selon qu'on considère \n les utilisateurs les plus influents ou non", fontsize=12, color='grey')
    plt.show()
    
    
    
cheminTweetsJson = "../data/tweets/" + "exempleTweetsJson.txt" # Attention à ce qu'il y ait bien *STOP* à la fin du fichier
#cheminTweetsJson = "../data/tweets/" + "cocaTweetsJson.txt" # Attention à ce qu'il y ait bien *STOP* à la fin du fichier


# Décommentez l'une des lignes ci-dessous pour n'afficher que les tweets des personnes avec le plus de followers
# Ou alors tous les tweets sans filtrer les utilisateurs les moins influents

#display_intensity(tweet_statistics_ponder(extract_best_tweets(retrieve_tweets(cheminTweets)))
#display_intensity(tweet_statistics_ponder(every_tweet(retrieve_tweets(cheminTweets))))
    
combined_display_followers(cheminTweetsJson)





    
