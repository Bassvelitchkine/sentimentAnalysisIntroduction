import pickle as pk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt

#Cette fois-ci on veut utiliser un autre modèle qui est pré construit dans le module nltk

#On a besoin d'extraire nos tweets sous la forme d'une liste de string cette fois-ci
def extract_tweets(filepath):
    """
    Input: str
    Output: list of str
    La fonction retourne la liste des tweets qui ont été enregistrés dans le fichier qui se 
    trouve au bout du chemin passé en argument
    """
    tweets=[]
    with open(filepath,'rb') as file:
        pickler=pk.Unpickler(file)
        liste_tweets=pickler.load()
        
    for dico in liste_tweets:
        tweets.append(dico['text'])
        
    return tweets

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
        
    return [neg,neu,pos]

def tweet_statistics(tweets):
    """
    Input: list of str
    Output: list of float
    La fonction prend en argument les tweets qu'on a collectés. Elle retourne une liste contenant
    trois flottants qui correspondent aux sommes des scores de négativité, de neutralité et de 
    positivité de chaque tweet.
    """
    sid = SentimentIntensityAnalyzer()
    neg,neu,pos=0.,0.,0.
    
    for tweet in tweets:
        ss = sid.polarity_scores(tweet)
        neg+=ss['neg']
        neu+=ss['neu']
        pos+=ss['pos']
        
    return [neg,neu,pos]

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
    plt.title("Analyse de sentiments sur Twitter \n avec une fonction préconstruite de nltk", fontsize=12, color='grey')
    plt.show()
    
def combined_display(tweets):
    """
    Input: list of str
    Output: pyplot histogram
    La fonction prend en argument la liste de tous les tweets et affiche les scores de négativité,
    de neutralité et de positivité lorsqu'on tient compte ou non du score de "mélange" 
    comme pondération
    """
    ponder=tweet_statistics_ponder(tweets)
    regular=tweet_statistics(tweets)
    
    #On créé la liste des étqiuettes des absisses
    liste_etiquettes=['negativité','neutralité','positivité'] 
      
    #On segmente les absisses
    liste_positions=np.arange(len(liste_etiquettes))
    
    #On détermine la largeur de la barre
    bar_width=0.20
    
    #On ajoute les barres
    plt.bar(liste_positions, ponder, bar_width, color='pink')
    plt.bar(liste_positions+bar_width,regular,bar_width,color='purple')
    
    #Etiquettes des absisses
    plt.xticks(liste_positions+bar_width*0.5, liste_etiquettes)
    
    #Absisses
    plt.xlabel('Sentiment', fontsize=10,color='blue')
    
    #Ordonnées
    plt.ylabel('Présence', fontsize=10,color='blue')
    
    #On ajoute la légende
    plt.legend(['Avec pondération','Sans pondération'])
    
    #Titre
    plt.title("Analyse de sentiments sur Twitter \n avec une fonction préconstruite de nltk", fontsize=12, color='grey')
    plt.show()
    
cheminTweetsTransformes = "../data/tweets/" + "exempleTweetsTransformes.txt"
#cheminTweetsTransformes = "../data/tweets/" + "cocaTweetsTransformes.txt"

tweets=extract_tweets(cheminTweetsTransformes)
    
# Décommentez l'une des deux lignes ci-dessous pour afficher séparément les graphes avec et sans pondération    

#display_intensity(tweet_statistics_ponder(tweets))
#display_intensity(tweet_statistics(tweets))

combined_display(tweets)
        
    