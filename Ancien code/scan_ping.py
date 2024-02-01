import subprocess
import time
import os

def nmap_host_discovery(ip_range):
    command = f'nmap -sn {ip_range}'
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution de Nmap : {e}"

def create_log_folder():
    # Vérifier si le dossier de logs existe, sinon le créer
    log_folder = "logs_scan_reseau"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

def run_nmap_periodically(ip_range, interval_minutes):
    create_log_folder()
    scan_count = 1

    while True:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_filename = f"logs_scan_reseau/scan_reseau_{scan_count}_{timestamp}.txt"
        
        print(f"Exécution de Nmap sur le réseau à {time.ctime()}")

        # Exécution de Nmap et sauvegarde dans le fichier de log
        discovery_result = nmap_host_discovery(ip_range)
        with open(log_filename, "w") as log_file:
            log_file.write(discovery_result)

        print(f"Résultats enregistrés dans : {log_filename}")

        # Attendre le prochain intervalle (30 minutes)
        time.sleep(interval_minutes * 60)

        # Incrémenter le compteur de scans
        scan_count += 1

if __name__ == "__main__":
    ip_range = "192.168.1.1-255"
    interval_minutes = 30

    run_nmap_periodically(ip_range, interval_minutes)