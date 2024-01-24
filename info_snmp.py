from pysnmp.hlapi import *

# Configuration de l'agent SNMP
snmp_target = '192.168.56.106'
snmp_port = 161
snmp_community = 'public'

# Fonction pour envoyer une requête SNMP GET
def snmp_get(oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(snmp_community),
               UdpTransportTarget((snmp_target, snmp_port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )
    # Vérification des erreurs
    if errorIndication:
        print(f"Erreur d'indication: {errorIndication}")
    elif errorStatus:
        print(f"Erreur de statut: {errorStatus}")
    else:
        # Affichage des résultats
        for varBind in varBinds:
            print(f"{varBind[0]} = {varBind[1]}")

# Exemple d'utilisation
if __name__ == "__main__":
    oid_to_get = '1.3.6.1.2.1.1.1.0'  # Exemple d'OID pour le nom du système
    snmp_get(oid_to_get)
