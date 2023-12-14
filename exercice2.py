import subprocess,platform,os
from subprocess import check_output

#stockage du nom du system
os_name = platform.system()
#fonction pour simplifier l'utilisation de subprocess.run

def subproc(arg):
    try:
        result = subprocess.run(arg, shell=True, capture_output=True, text=True)
        return result
    except Exception as e:
        print(f"Error: {e}")
        
def IpWindows():
    print("Actuellement sous l'OS Windows\n")
    print("Liste de vos cartes réseau :")

    #lance la commande ipconfig pour afficher les cartes réseaux et stock la sortie
    output = check_output('ipconfig', text=True)

    #divise la sortie en ligne
    result = output.splitlines()
    
    #liste où la liste des carte seront stocké
    network_list = []
    subnet_mask = ""
    #variable pour sortir de la boucle
    j = False
    #variable pour incrémenter l'affichage des cartes réseaus
    line_number = 1

    for line in result:
        if "Carte" in line:
            #stockage du nom de la carte, la partie gauche qui précède le séparateur ':'
            current_network = line.split(":")[0]

        if "IPv4" in line:
            #stockage de l'ip, la partie droite
            ip_address = line.split(":")[1].strip()
            
            #stock, ajoute à la liste et affiche  les informations de la carte
            info_carte = f"Carte {line_number}: Nom de la carte : {current_network}, Adresse IP : {ip_address}"
            network_list.append(info_carte)
            print(info_carte)
            line_number += 1

    choix = input("Choisir le numéro de la carte réseau qui doit être utilisé ('q' pour quitter) : ")

    choix_ip = input("Ping les machines sur le réseau ? (y ou n) : ")
    carte_selectionne = None

    while not j:
        if choix == "q":
            j = True
            print("Programme fermé.")
        else:
            try:
                #cast du choix en int
                choix = int(choix)
                #verification si le numéro de carte est valide
                if choix <= len(network_list):
                    #évite que l'utilisateur choisisse l'index
                    carte_selectionne = network_list[choix - 1]
                    #stockage dans ip, la partie droite apres "Adress IP : "
                    ip = carte_selectionne.split("Adresse IP : ")[1]

                    print(f"Carte selectionné : \n{carte_selectionne}\n")
                    
                    if choix_ip == 'y':
                        #divise l'ip en tableau
                        ip_early_tab = ip.split(".")
                        #je stock l'index 0 et 1 du tableau (de l'ip) dans ip early
                        ip_early = ip_early_tab[0] + "." + ip_early_tab[1]
                        print("Ping en cours, le ping peut durer plusieurs minutes. Tout les résultats seront stocké dans le fichier result_scan.txt.")

                        i = 0
                        while i != 255:
                            j = 40
                            while j != 255:
                                #stockage dans hostname le réseaux a ping a chaque tour de boucle
                                hostname = f"{ip_early}.{i}.{j}"
                                
                                try:
                                    result = subproc(f"ping {hostname} -n 1")
                                    with open("result_scan.txt", "a+") as file:
                                        file.write(f"{result}\n")
                                except Exception as e:
                                    print(f"Erreur lors du ping de {hostname}: {e}")
                                
                                j = j + 1

                            i = i + 1

                        print("Le scan est dans le fichier : ip_online.txt")
                    else:
                        print("Programme fermé.")
                        j = True
                else:
                    print("Numéro de carte réseau invalide. Veuillez choisir un numéro valide.")
            except Exception as e:
                print(f"Erreur : {e}")
                



def IpLinux():
    print("Actuellement sous l'OS Linux")
    #liste où sera stocker les cartes réseaux
    network_list = []
    #variable pour incrémenter les numeros de carte réseau
    line_numberL = 1
    
    
    #lance la commande ifconfig et stock la sortie
    output = subprocess.check_output(['ifconfig'], text=True)

    #sépare les cartes réseaux sur une ligne et la stock dans la liste
    part = output.strip().split('\n')
    h = False
    #dump(part)
    for section in part:
        if 'inet ' in section:
            #divise le resultat sous forme de ligne, et stock chaque ligne dans la list
            lines = section.strip().split('\n')
            #dump(lines)
            for line in lines:
                if 'inet ' in line:
                    #sépare chaque mot 
                    index = line.split()
                    #dump(index)
                    #selection du deuxieme element
                    ip_address = index[1]
                    
                    #ajout des informations de la carte réseaux dans la list network_list
                    info_carte = f'{ip_address}'
                    network_list.append(info_carte)
    #affiche la liste des cartes réseau actives
    print("Liste de vos cartes réseau actives :")
    for network in network_list:
        print(f"Carte {line_numberL}: {network}")
        #incrémente a chaque tour, le numéro de la carte réseau
        line_numberL += 1

    #sélection de la carte réseau
    while not h:
        choix = input("Choisir le numéro de la carte réseau qui doit être utilisé ('q' pour quitter) : ")
        choix_ip = input("Ping les machines sur le réseau ? (y ou n) : ")
        if choix_ip == 'y':       
            choix = int(choix) - 1
            #stockage du choix de l'utilisateur dans ip
            ip = network_list[choix] 
            
            #divise l'ip en tableau
            ip_early_tab = ip.split(".")
            #je stock l'index 0 et 1 du tableau (de l'ip) dans ip early
            ip_early = ip_early_tab[0] + "." + ip_early_tab[1]
            print("Ping en cours, le ping peut durer plusieurs minutes. Tout les résultats seront stocké dans le fichier result_scan.txt.")

            i = 0
            while i != 255:
                j = 0
                while j != 255:
                    #stockage dans hostname le réseaux a ping a chaque tour de boucle
                    hostname = f"{ip_early}.{i}.{j}"
                    
                    try:
                        result = subproc(f"ping {hostname} -c 1")
                        with open("result_scan.txt", "a+") as file:
                            file.write(f"{result}\n")
                    except Exception as e:
                        print(f"Erreur lors du ping de {hostname}: {e}")
                    j = j + 1
                i = i + 1

            print("Le scan est dans le fichier : result_scan.txt")
        if choix == "q":
            print("Programme fermé.")
            h = True
        try:
            #cast le choix utilisateur en int
            choix = int(choix)
            #vérification si le numéro de carte est valide
            if choix <= len(network_list):
                #évite que l'utilisateur choisisse l'index
                #dump(network_list)
                choix = network_list[choix - 1]
                #on sélectionne l'ip
                ip = choix.split()[0]
                print(f"Carte selectionné : {choix}")
                try:
                    result = subprocess.check_output(commande, shell=True, text=True)
                    with open("ip_online.txt", "w") as file:
                        file.write(result)
                        print("Le scan est dans le fichier : ip_online.txt")
                        h = True
                except Exception as e:
                    print(f"{e}")
                    h = True
                else:
                    print("Numéro de carte réseau invalide. Veuillez choisir un numéro valide.")
        except Exception as e:
            print(f"Erreur : {e}")
    
            
            

#si l'utilisateur est sur linux
if os_name == "Linux":
    IpLinux()
#si l'utilisateur est sur windows 
if os_name == "Windows":
    IpWindows()
