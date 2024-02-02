import subprocess
import sys

def install_snmp_client():
    try:
        # Vérifier si le package 'snmp' est déjà installé
        check_installed_command = "dpkg -l | grep -E '^ii' | grep snmp"
        check_installed_process = subprocess.run(check_installed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if check_installed_process.returncode == 0:
            print("Le client SNMP est déjà installé.")
            return

        # Installer le package 'snmp'
        install_command = "sudo apt-get update && sudo apt-get install -y snmp"
        install_process = subprocess.run(install_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if install_process.returncode == 0:
            print("Le client SNMP a été installé avec succès.")
        else:
            print("Erreur lors de l'installation du client SNMP:")
            print(install_process.stderr.decode('utf-8'))
            
        # Modifier le fichier snmpd.conf
        modify_snmpd_conf()
        
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")

if __name__ == "__main__":
    if sys.platform != 'linux':
        print("Ce script est conçu pour les systèmes basés sur Linux.")
        sys.exit(1)

def modify_snmpd_conf():
    try:
        # Chemin du fichier snmpd.conf
        snmpd_conf_path = "/etc/snmp/snmpd.conf"

        # Nouveau contenu à ajouter
        new_content = """
# SECTION: System Information Setup
sysLocation    Sitting on the Dock of the Bay
sysContact     Me <me@example.org>
sysServices    72

# SECTION: Agent Operating Mode
master  agentx
agentaddress udp:161

# SECTION: Access Control Setup
view all included .1
rocommunity6 public default -V all
rocommunity public default -V all
rouser authPrivUser authpriv -V all
"""

        # Supprimer et recréer le fichier snmpd.conf
        with open(snmpd_conf_path, 'w') as file:
            file.write(new_content)

        print("Le fichier snmpd.conf a été modifié avec succès.")

    except Exception as e:
        print(f"Une erreur s'est produite lors de la modification de snmpd.conf: {str(e)}")

    
    install_snmp_client()
# Copyright © 2024 Groupe ILAN. Tous droits réservés.
