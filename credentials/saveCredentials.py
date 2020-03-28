import pickle

# Remplacer les valeurs de chaque variable avec les clés et token de votre compte développeur 
# cf. README.me

API_key="" 
API_secret_key="" 
access_token="" 
access_token_secret="" 

res=[API_key,API_secret_key,access_token,access_token_secret]

def save_cred(filepath):
    """
    Input: str
    Output: None
    La fonction permet d'enregistrer les différents identifiants et mdp qui permettent de se connecter à 
    l'api twitter
    """
    with open(filepath,'wb') as file:
        pickler=pickle.Pickler(file)
        pickler.dump(res)
        

# Exécuter une seule fois ce programme python.
# Il sauvegardera la liste de vos identifiants en données binaires dans le même dossier.
# Toutes les fonctions de collecte de tweets y feront ensuite appel.
save_cred("./credentials.txt")        