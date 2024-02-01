import json        
 
fichier_json = open('Inventaire-main\Inventaire_Donnees.json', 'r', encoding="utf-8")  
 
def valeur_total(fichier_json):
    """
    valeur_total est une fonction qui calcul la sommes des prix de tous les éléments dans la base de donnée json

    Arg: fichierjson
    Return : prixtotal de tout les
    """
    with fichier_json as fichier:
        data = json.load(fichier)      # load décode un fichier json
        prixtotal=0
        for article in data:
                prixtotal += article["price"]*article["amount"]
        print(prixtotal)