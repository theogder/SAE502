from pysnmp.hlapi import *

# Configuration de l'agent SNMP
snmp_target = '192.168.56.106'
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
def snmp_get(oids):
    # Initialiser une liste pour stocker les résultats de chaque OID
    results = []

    for oid in oids:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(snmp_community),
                   UdpTransportTarget((snmp_target, snmp_port)),
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

    # Affichage des résultats
    for result in results:
        print(f"{result[1]} ({result[0]}) = {result[3]}")

# Exemple d'utilisation avec plusieurs OIDs
if __name__ == "__main__":
    oids_to_get = [
        '1.3.6.1.4.1.2021.10.1.3.3',  # 15 minute load CPU
        '1.3.6.1.4.1.2021.4.11.0',
        '1.3.6.1.4.1.2021.4.5.0'    # list nic name
    ]
    snmp_get(oids_to_get)
