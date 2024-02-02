from flask import Flask, render_template, request, jsonify
from pysnmp.hlapi import *
import paramiko

app = Flask(__name__)

# Configuration de l'agent SNMP
snmp_port = 161
snmp_community = 'public'

# Configuration SSH
ssh_username = 'user'
ssh_password = 'bonjour'
ssh_port = 22

# Fonction pour effectuer la correspondance entre les OID et leurs significations
def map_oid_to_name(oid):
    oid_mappings = {
        '1.3.6.1.4.1.2021.10.1.3.3': 'CPU 15-Minute Load',
        '1.3.6.1.4.1.2021.4.11.0': 'Total RAM Free',
        '1.3.6.1.4.1.2021.4.5.0': 'Total RAM in machine'
        # Ajoutez d'autres correspondances OID -> Signification au besoin
    }

    return oid_mappings.get(oid, f"Signification non définie pour l'OID {oid}")

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
                results.append({
                    'oid': str(oid),
                    'name': map_oid_to_name(oid),
                    'value': str(varBind[1])
                })

    return results

def ssh_execute_command(target_ip, command):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        ssh.connect(target_ip, port=ssh_port, username=ssh_username, password=ssh_password)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Get the command output
        output = stdout.read().decode('utf-8')

        return output

    finally:
        # Close the SSH connection
        ssh.close()

# Route pour servir la page HTML
@app.route('/')
def index():
    additional_text = "Ceci est un texte supplémentaire à afficher dans la page."
    return render_template('page01.html', additional_text=additional_text)

# Route pour gérer le balayage SNMP
@app.route('/scan', methods=['POST'])
def scan():
    target_ip = request.json.get('ipAddress')
    oids_to_get = [
        '1.3.6.1.4.1.2021.10.1.3.3',
        '1.3.6.1.4.1.2021.4.11.0',
        '1.3.6.1.4.1.2021.4.5.0'
    ]

    results = snmp_get(oids_to_get, target_ip)
    print(results)

    return jsonify({target_ip: results})

# Route pour gérer la commande SSH
@app.route('/ssh', methods=['POST'])
def execute_ssh_command():
    target_ip = request.json.get('ipAddress')
    ssh_command_output = ssh_execute_command(target_ip, 'ls')  # Exemple avec la commande 'ls'
    print(ssh_command_output)

    return jsonify({'ssh_command_output': ssh_command_output})

if __name__ == '__main__':
    app.run(debug=True)
