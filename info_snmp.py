from pysnmp.hlapi import *
from datetime import datetime

# Configuration de l'agent SNMP
snmp_targets = ['192.168.56.106', '192.168.1.1']  # Ajoutez toutes les adresses IP cibles nécessaires
snmp_port = 161
snmp_community = 'public'

# Fonction pour effectuer la correspondance entre les OID et leurs significations
def map_oid_to_name(oid):
    oid_mappings = {
        '1.3.6.1.4.1.2021.10.1.3.3': 'CPU 15-Minute Load',
        '1.3.6.1.4.1.2021.4.11.0': 'Total RAM Free',
        '1.3.6.1.4.1.2021.9.1.7.1': 'Available space on the disk',
        '1.3.6.1.4.1.2021.4.5.0': 'Total RAM in machine'
        # Ajoutez d'autres correspondances OID -> Signification au besoin
    }

    return oid_mappings.get(oid, f"Signification non définie pour l'OID {oid}")

# Fonction pour envoyer une requête SNMP GET avec plusieurs OIDs
def snmp_get(oids, target_ip):
    # Initialiser une liste pour stocker les résultats de chaque OID
    results = []

    for oid in oids:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(snmp_community),
                   UdpTransportTarget((target_ip, snmp_port)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        )

        # Vérification des erreurs
        if errorIndication:
            print(f"Erreur d'indication pour {map_oid_to_name(oid)}: {errorIndication}")
        elif errorStatus:
            print(f"Erreur de statut pour {map_oid_to_name(oid)}: {errorStatus}")
        else:
            # Ajouter le résultat à la liste des résultats
            for varBind in varBinds:
                results.append((oid, map_oid_to_name(oid), varBind[0], varBind[1]))

    return results

# Fonction pour écrire les résultats dans un fichier HTML organisé par IP
def write_to_html(results_by_ip):
    with open("C:/Users/ilan.floch/Desktop/Serveur HTTP/www/page01.html", "a") as f:
        f.write("<html><head><title>SNMP Results</title></head><body>")
        for target_ip, results in results_by_ip.items():
            f.write(f"<h2>Results for {target_ip}</h2>")
            f.write("<ul>")
            for result in results:
                f.write(f"<li>{result[1]} ({result[0]}) = {result[3]}</li>")
            f.write("</ul>")
        f.write("</body></html>")

# Exemple d'utilisation avec plusieurs OIDs
if __name__ == "__main__":
    oids_to_get = [
        '1.3.6.1.4.1.2021.10.1.3.3',  # 15 minute load CPU
        '1.3.6.1.4.1.2021.4.11.0',
        '1.3.6.1.4.1.2021.4.5.0'    # list nic name
    ]

    results_by_ip = {}

    for target_ip in snmp_targets:
        results = snmp_get(oids_to_get, target_ip)
        results_by_ip[target_ip] = results

    write_to_html(results_by_ip)
