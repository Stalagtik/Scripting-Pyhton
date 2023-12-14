import scapy.all as scapy


#scan (count= 5, 5 paquet a scanner)
scan = scapy.sniff(count=5)

#enregistre le scan dans le fichier pcap
scapy.wrpcap("packet.pcap", scan)

#lecture du fichier pcap
result_scan = scapy.rdpcap("packet.pcap")

#utilisation d'un set au lieu d'une liste pour éviter les doublons
ip_unique = set()

#parcoure le fichier pour extraire les IP unique
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
