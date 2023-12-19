import paramiko

def collect_remote_system_info(hostname, username, password, commands):
    try:
        # Établir la connexion SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Exécuter les commandes à distance
        collected_info = {}
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            result = stdout.read().decode('utf-8').strip()
            collected_info[command] = result

        return collected_info

    except Exception as e:
        print(f"Erreur lors de la connexion à la machine distante: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # Spécifiez les informations de la machine distante
    print("Assure toi que le ssh et bien ouvert du la machine cible")
    remote_hostname = input("IP de la machine cible ? ")
    remote_username = input("Entre un utilisateur ? ")
    remote_password = input("Entre un mot de passe ? ")

    # Liste des commandes à exécuter à distance
    remote_commands = ["uname -a", "df -h"]

    # Collecter les informations à distance
    remote_info = collect_remote_system_info(remote_hostname, remote_username, remote_password, remote_commands)

    # Afficher les informations collectées
    for command, result in remote_info.items():
        print(f"{command}:\n{result}")