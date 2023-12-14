import scapy.all as scapy
import threading

#on definit le nombre de paquet que l'on veut analyser
scan_paquet = 10
thread_list = []

#capture de packet, et stockage du resultat dans le fichier packet.pcap
def scan(scan_paquet):
    packet = scapy.sniff(count=scan_paquet)
    #enregistre le scan dans le fichier pcap
    scapy.wrpcap("packet.pcap", packet)

#creation d'un nombre de thread egale au nombre de paquet analysé
for i in range(scan_paquet):
    #utilisation de l'objet threading.thread et ajout d'une virgule pour le mettre en tuple d'un element
    scan_thread = threading.Thread(target=scan, args=(scan_paquet,))
    thread_list.append(scan_thread)
    scan_thread.start()
#coordonne les threads
for thread in thread_list:
    thread.join()

#lecture du fichier pcap
result_scan = scapy.rdpcap("packet.pcap")

#utilisation d'un set au lieu d'une liste pour éviter les doublons
ip_unique = set()

#parcours du fichier pour extraire les IP unique
for packet in result_scan:
    #vérifie si le paquet récupéré est bien une IP
    if packet.haslayer(scapy.IP):
        #stockage de l'ip source et de l'ip destination
        ip_source = packet[scapy.IP].src
        ip_destination = packet[scapy.IP].dst
        #ajoute l'IP source et destination sous forme de tuple
        ip_unique.add((ip_source, ip_destination))

if not ip_unique:
    print("aucune ip unique")
else:
    #affichage des IP unique
    print("Liste des adresses IP unique :\n")
    for ip in ip_unique:
        print(f"IP source: {ip[0]} / IP destination: {ip[1]}")