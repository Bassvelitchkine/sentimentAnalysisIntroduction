# Analyse de sentiment sur Twitter

## Introduction

Pour beaucoup d'entreprises et de personnalités, il est de plus en plus pertinent de connaitre l'opinion des gens sur les réseaux sociaux. En effet, ce sont des lieux d'échange et d'interaction à l'intérieur desquels les gens peuvent avoir de l'influence les uns sur les autres. Peu importe que l'information diffusée ou relayée soit vraie ou fausse, l'important est qu'elle serve l'intérêt de l'entreprise ou de la personne qui cherche à analyser sa présence sur les réseaux.

Par ailleurs, les grands réseaux sociaux que nous connaissons regorgent de données. Il est possible de mener des analyses vraiment représentatives. C'est pour cette raison que nous avons trouvé particulièrement intéressant de faire ce travail introductif (ce n'est qu'une exploration du vaste sujet qu'est l'analyse de sentiments).

Enfin, nous avons choisi d'analyser les données de Twitter car leur API est régulièrement maintenue à jour et le module tweepy pour Python est particulièrement simple d'utilisation. Nous avons pu nous focaliser sur l'analyse pure sans perdre de temps sur la connexion à l'API.

## Pipeline

Le projet s'est découpé en trois grandes parties : 1. La collecte des tweets 2. La transformation des données brutes 3. L'analyse des données transformées

### Prerequisites

Avant de rentrer dans le vif du sujet, voici les modules Pyhton à installer, par exemple avec l'invite de commande Anaconda Prompt si vous utilisez la distribution Anaconda :

```
pip install tweepy
pip install numpy
pip install nltk
pip install matplotlib.pyplot
pip install time
pip install json
pip install csv
```

## Avant toute chose

Cloner le dossier git sur votre machine et... c'est tout !

Deux options s'offrent à vous : 1. Soit vous vous fichez de l'entreprise dont on fait l'analyse de sentiment et vous pouvez vous contenter de la section [`Commencer rapidement`](#Commencer rapidement) 2. Soit vous voulez choisir le sujet et vous devez suivre toute la pipeline du projet pas à pas [`Pas à pas`](#Pas à Pas)

### Commencer rapidement

Nous avons récolté des données sur Coca-Cola. Ce sont donc les résultats de Coca-Cola que vous oberverez.

- Rendez-vous dans le dossier analysis et ouvrez l'un des trois fichiers :
  - basicAnalysis.py 👉 on affiche simplement les scores de positivité, de neutralité et de négativité associés à Coca
  - withoutBiasedUsers.py 👉 on ne considère que les utilisateurs qui émettent des avis partagés pour exclure les haters et les early adopters
  - influencersAnalysis.py 👉 on veut voir à quel point l'avis des influenceurs et celui du "populas" sont corrélés.

Avant de lancer l'exécution, décommentez les lignes correspondant à Coca et décommentez les autres :

```python
# cheminTweets = "../data/tweets/" + "exempleTweetsTransformes.txt"
cheminTweets = "../data/tweets/" + "cocaTweetsTransformes.txt"
```

Vous devriez voir s'afficher des graphes très simples à lire.

### Pas à Pas

#### 1. Collecte

Rendez-vous dans le dossier collect. Ouvrez le seul fichier Python qu'il contient et donnez des valeurs cohérentes aux variables string du bas du fichier selon l'entreprise que vous étudiez :

```python
# Changer les valeurs d'exemple par ce que vous voulez
cheminFichierTweets = "../data/tweets/" + "exempleTweets.txt"
cheminFichierTweetsId = "../data/tweets/" + "exempleTweetsId.txt"
cheminCredentials = "../credentials/credentials.txt"
requete = "exemple"
```

Il ne vous reste plus qu'à exécuter le script et à en forcer l'arrêt (oui c'est maladroit) dès que vous pensez avoir récolté suffisamment de tweets. 1000 devraient suffire pour se faire une idée.

#### 2. Transformation

Comme à l'étape précédente, changez les valeurs des variables de manière adéquate :

```python
# Remplacer les exemples par les bonnes valeurs
cheminTweetsBruts = "../data/tweets/" + "exempleTweets.txt"   # Assurez-vous d'avoir bien écrit "*STOP*" à la fin de ce fichier après l'exécution du script
cheminTweetsTransformes = "../data/tweets/" + "exempleTweetsTransformes.txt"
cheminTweetsJson = "../data/tweets/" + "exempleTweetsJson.txt" # Assurez-vous d'avoir bien écrit "*STOP*" à la fin de ce fichier après l'exécution du script
```

Puis exécutez une seule fois le script.

#### 3. Analyse

Il ne vous reste plus qu'à faire la même chose que pour [`Commencer rapidement`](#Commencer rapidement) en changeant les valeurs des variables en bas des fichiers :

```python
cheminTweetsTransformes = "../data/tweets/" + "exempleTweetsTransformes.txt"
```

## Pistes d'exploration

La piste qui m'a semblé être la plus intéressante à explorer est celle des influenceurs. A savoir : comment leur avis impacte celui de la masse. Il s'agit de mêler des notions de propagation virale, de théorie des graphes et de traitement du langage naturel.

En effet, pour une entreprise, il est important de connaitre l'opinion que les gens ont d'elle mais également d'avoir des pistes d'améliorations, par exemple en ciblant certains utilisateurs influents pour des collaborations.

Les critères permettant d'évaluer "l'influence" dans un graphe sont nombreux : nombre d'arrêtes, k-core, etc. Mais à part le nombre d'arrêtes (i.e le nombre de followers ou d'abonnements), le calcul des autres critères dits de "centralité" nécessitent de connaitre toute la structure du graphe connexe contenant les utilisateurs dont on a prélevé les tweets. Nous sommes tellement connectés sur les réseaux sociaux qu'avec une poignées d'utilisateurs nous pourrions nous retrouver à devoir stocker le graphe complet de Twitter, qu'un petit ordinateur ne pourra pas analyser. Il faut trouver d'autres pistes pour aboutir à ces mesures.

## NDLR

La rédaction du code est assez maladroite, tout aurait pu être mieux fait mais j'ai travaillé en temps limité avec une équipe au niveau disparate. Je n'ai pas contre uploadé que mes contributions et mon code. Il faut davantage voir ce répo comme une introduction à un travail qui pourrait facilement être beaucoup plus poussé.

## Authors

- **Bastien Velitchkine** - _Initial work_ - [Bassvelitchkine](https://github.com/Bassvelitchkine)
