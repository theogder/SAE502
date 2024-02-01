import paramiko

def collect_remote_system_info(hostname, username, password, commands, log_file_path):
    try:
        # Établir la connexion SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Exécuter les commandes à distance
        collected_info = {}
        for command in commands:
            result = execute_command(client, command)
            collected_info[command] = result

        # Récupérer des fichiers de log
        log_contents = get_log_files(client)

        # Copier le contenu des fichiers de log dans un fichier local
        save_log_to_file(log_contents, log_file_path)

        return collected_info

    except Exception as e:
        print(f"Erreur lors de la connexion à la machine distante: {e}")
    finally:
        client.close()

def execute_command(client, command):
    # Fonction pour exécuter une commande à distance
    stdin, stdout, stderr = client.exec_command(command)
    result = stdout.read().decode('utf-8').strip()
    return result

def get_log_files(client):
    # Fonction pour récupérer le contenu des fichiers de log
    log_files = ["/var/log/syslog", "/var/log/auth.log"]  # Ajoutez d'autres fichiers au besoin
    log_contents = {}

    for log_file in log_files:
        result = execute_command(client, f"cat {log_file}")
        log_contents[log_file] = result

    return log_contents

def save_log_to_file(log_contents, log_file_path):
    # Fonction pour copier le contenu des fichiers de log dans un fichier local
    with open(log_file_path, "w") as local_log_file:
        for log_file, content in log_contents.items():
            local_log_file.write(f"=== {log_file} ===\n{content}\n\n")

if __name__ == "__main__":
    print("Assurez-vous que le SSH est bien ouvert sur la machine cible.")
    remote_hostname = input("Entrez l'IP de la machine cible: ")
    remote_username = input("Entrez le nom d'utilisateur: ")
    remote_password = input("Entrez le mot de passe: ")

    # Liste des commandes à exécuter à distance
    remote_commands = ["uname -a", "df -h"]

    # Chemin du fichier local pour sauvegarder les fichiers de log
    log_file_path = "logs_from_remote.txt"

    # Collecter les informations à distance et sauvegarder les fichiers de log
    remote_info = collect_remote_system_info(remote_hostname, remote_username, remote_password, remote_commands, log_file_path)

    # Afficher les informations collectées
    for command, result in remote_info.items():
        print(f"{command}:\n{result}")

    print(f"Les fichiers de log ont été sauvegardés dans {log_file_path}")