import sys,platform,subprocess,argparse


#fonction pour simplifier l'utilisation de subprocess.run
def subproc(arg):
    try:
        result = subprocess.run([arg], shell=True, capture_output=True, text=True)
        return result
    except Exception as e:
        print(f"Error: {e}")


#fonction pour afficher l'aider en cas de -h / --help lors de l'execution du code
def help():
    parser = argparse.ArgumentParser(description="Ce programme à pour but de récupérer votre ip et la stocker dans un fichier \n Il suffit uniquement d\'utiliser la commande : python exercice1.py")
    parser.parse_args()




help()
#stockage du nom du system dans la variable
os_name = platform.system()
#variable qui permet la vérificaiton de la présence d'une carte réseau activé
ip_found = False
#si je suis sous Linux
if os_name == "Linux":
    try:
        print("Actuellement sous l'OS Linux\n")

        #execution de la commande, création du ficher, et écriture du résultat de la commande dans le fichier.
        result = subproc("ifconfig")
        with open('ip.txt','w') as fic:
            fic.write(result.stdout)
        print("Fichier écrit sous le nom 'ip.txt'\n")
                        
        
        #execution de la commande ls
        result = subproc("ls")
        print("Voici la list des fichiers de votre répertoire : \n\n %s \n" %(result.stdout))
        
        #lecture du fichier ip.txt
        print("Contenu du fichier créer (ip.txt) :")      
        with open('ip.txt','r') as fic: 
            ls = fic.read()
            if not "inet ":
                print("[ERREUR] Affichage du contenu impossible, aucune information concernant votre ip, vérifiez la carte réseaux de votre ordinateur. \n")
            else:
                print(ls)
        
        #boucle pour afficher toutes les IPV4 récupérer
        print('ip récupérés :')
        #on vérifie si la carte réseau de l'ordinateur est activé
        for i in ls.splitlines():
            if "inet " in i:
                ip_found = True
                print(i)

        #si il n'a pas trouvé "d'inet" dans le fichier, alors la carte réseaux de l'ordinateur est désactivé
        if not ip_found:
            print("Vérifier la carte réseaux de votre ordinateur")
    except Exception as e:
        print(f"Error: {e}")
        




if os_name == "Windows":
    try:
    #je suis sous Windows

        print("Actuellement sous l'OS Windows.\n")
        
        #execution de la commande, création du ficher, et écriture du résultat de la commande dans le fichier.
        result = subproc("ipconfig") 
        with open('ip.txt','w') as fic:
            fic.write(result.stdout)
        print("Fichier écrit sous le nom 'ip.txt\n")
                
        #execution de la commande ls             
        result = subproc("dir")
        print("Voici la list des fichiers de votre répertoire : \n\n %s \n" %(result.stdout))
        
        
        #lecture du fichier ip.txt
        print("Contenu du fichier créer (ip.txt) :")
        with open('ip.txt','r') as fic: 
            ls = fic.read()
            if not "IPv4":
                print("[ERREUR] Affichage du contenu impossible, aucune information concernant votre ip, vérifiez la carte réseaux de votre ordinateur. \n")
            else:
                print(ls)
            
            
        #boucle pour afficher tout les IPv4 récupéré 
        print('IP récupérées :')
        for i in ls.splitlines():
            if "IPv4" in i:
                ip_found = True
                print(i)

        #si il n'a pas trouvé "d'ipv4" dans le fichier, alors la carte réseaux de l'ordinateur est désactivé
        if not ip_found:
            print("Vérifier la carte réseaux de votre ordinateur")

    except Exception as e:
        print(f"Error: {e}")
else:
    #dans le cas où l'utilisateur n'est ni sur windows, ni linux
    print("Ce system d'exploitation n'est pas pris en compte.")
    