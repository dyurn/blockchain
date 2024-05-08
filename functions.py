import requests
import datetime
import time as t
import sys

class fg:
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    RESET   = '\033[39m'

class style:
    BRIGHT    = '\033[1m'
    DIM       = '\033[2m'
    NORMAL    = '\033[22m'
    RESET_ALL = '\033[0m'

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Affiche une barre de progression dans la console.
    Args:
    - iteration : itération actuelle
    - total : nombre total d'itérations
    - prefix : préfixe de la barre
    - suffix : suffixe de la barre
    - decimals : nombre de décimales dans le pourcentage
    - length : longueur caractéristique de la barre de chargement
    - fill : caractère de remplissage de la barre
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + f'{fg.RED}_{fg.RESET}' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} {fg.GREEN}{bar}{fg.RESET} {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total: 
        print()

def get_blocks_for_day(timestamp):
    """Récupère les blocs pour un jour spécifique donné par un timestamp."""
    url = f"https://blockchain.info/blocks/{timestamp}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_blocks(days):
    """Récupère les blocs pour les 30 derniers jours."""
    current_time = datetime.datetime.now()
    block_times = []
    
    for day in range(days):

        day_time = current_time - datetime.timedelta(days=day)

        timestamp = int(day_time.timestamp() * 1000)
        blocks = get_blocks_for_day(timestamp)
        if blocks:
            block_times.extend([block['time'] for block in blocks])

        print_progress_bar(day + 1, days, prefix='Progress:', suffix='Complete', length=50)   
    
    return block_times

def remains_time(sec):
    sec = int(sec)
    m = int(sec/60)
    h = int(m/60)
    sec = sec%60
    m2 = m%60
    d = int(h/24)
    h2 = h%24
    if d >= 1: return f"{d} days {h2} hours {m2} mins {sec} secs"
    elif h >= 1: return f"{h} hours {m2} mins {sec} secs"
    elif m >= 1: return f"{m} mins {sec} secs"
    else: return f"{sec} secs"

