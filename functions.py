import requests
import datetime
import time as t
import sys
import matplotlib.pyplot as plt

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

def get_latest_block_hash():
    url = "https://blockchain.info/latestblock"
    
    try:
        response = requests.get(url)
        latest_block_data = response.json()
        
        latest_block_hash = latest_block_data['hash']
        return latest_block_hash
    
    except Exception as e:
        return f"Erreur lors de la récupération du hash du dernier bloc : {str(e)}"

def get_block_info_from_api(block_hash):
    url = f"https://blockchain.info/rawblock/{block_hash}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Error fetching block information: HTTP {response.status_code}"

        block_data = response.json()
        prev_block_hash = block_data.get('prev_block', None)
        next_block_hash = block_data.get('next_block', [None])[0] if block_data.get('next_block') else None
        nb_transactions = block_data.get('n_tx', 0)
        block_height = block_data.get('height', None)
        miner_fees_btc = block_data.get('fee', 0) / 1e8
        block_size = block_data.get('size', None)
        block_time = block_data.get('time', None)
        block_version = block_data.get('ver', None)
        block_weight = block_data.get('weight', None)

        # Creating a dictionary with the extracted information
        block_info = {
            "Hash": block_data['hash'],
            "Previous_Hash": prev_block_hash,
            "Next_Hash": next_block_hash,
            "NbTransactions": nb_transactions,
            "Height": block_height,
            "Fees": miner_fees_btc,
            "Size": block_size,
            "Time": block_time,
            "Version": block_version,
            "Weight": block_weight
        }

        return block_info

    except Exception as e:
        return f"Error fetching block information: {str(e)}"
    
def print_block_infos(block, mode):
    print(f"\t{style.BRIGHT}{fg.CYAN}Block: {block['Hash']}")
    print(f"\t{style.BRIGHT}{fg.MAGENTA}Height: {block['Height']}")
    print(f"\t{style.BRIGHT}{fg.GREEN}Number of transactions: {block['NbTransactions']}") 
    print(f"\t{style.BRIGHT}{fg.YELLOW}Miner Fees (BTC): {block['Fees']}{style.RESET_ALL}")
    if not mode == 2 : print('\n')
    if mode == 2:
        print(f"\tTime: {block['Time']}")
        print(f"\tPrevious hash: {block['Previous_Hash']}")
        print(f"\tNext hash: {block['Next_Hash']}")
        print(f"\tSize: {block['Size']}")
        print(f"\tWeight: {block['Weight']}")
        print(f"\tVersion: {block['Version']}{style.RESET_ALL}\n")
    
def get_block_by_height(height):
    url = f"https://blockchain.info/block-height/{height}?format=json"
    
    try:
        response = requests.get(url)
        data = response.json()
        # La hauteur peut correspondre à plusieurs blocs si des branches de la blockchain existent. Prenez le bloc principal.
        block_hash = data['blocks'][0]['hash']  # Prendre le hash du premier bloc, qui est normalement le bloc principal
        return get_block_info_from_api(block_hash)
    except Exception as e:
        return f"Erreur lors de la récupération du hash du bloc : {str(e)}"

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

def navigate_blocks(start_hash):
    """Permet à l'utilisateur de naviguer entre les blocs et de sélectionner des blocs pour une analyse ultérieure."""
    current_hash = start_hash
    selected_blocks = []  # Liste pour stocker les blocs sélectionnés

    while True:
        block_info = get_block_info_from_api(current_hash)
        if block_info:
            print_block_infos(block_info, mode=2)
            command = input("Enter '+' to go to the next block, '-' for the previous block, 's' to select this block for analysis, 'a' for automatic analysis (from n-5 to n+5), 'q' to quit (will start analysis): ")
            if command == '+':
                if 'Next_Hash' in block_info and block_info['Next_Hash']:
                    current_hash = block_info['Next_Hash']
                else:
                    print("No further blocks available.")
            elif command == '-':
                if 'Previous_Hash' in block_info and block_info['Previous_Hash']:
                    current_hash = block_info['Previous_Hash']
                else:
                    print("This is the first block available.")
            elif command == 'a':
                selected_blocks.append(block_info)
                print("Preparing automatic analysis...")
                for i in range(1, 6):
                    if 'Previous_Hash' in block_info and block_info['Previous_Hash']:
                        print_progress_bar(i, 5, prefix='Loading previous blocks:', suffix='Complete', length=50)
                        current_hash = block_info['Previous_Hash']
                        block_info = get_block_info_from_api(current_hash)
                        selected_blocks.append(block_info)
                    else:
                        print("No more previous blocks to load.")
                        break
                current_hash = selected_blocks[0]['Hash']  # reset to the initial hash
                block_info = get_block_info_from_api(current_hash)
                for i in range(1, 6):
                    if 'Next_Hash' in block_info and block_info['Next_Hash']:
                        print_progress_bar(i, 5, prefix='Loading next blocks:', suffix='Complete', length=50)
                        current_hash = block_info['Next_Hash']
                        block_info = get_block_info_from_api(current_hash)
                        selected_blocks.append(block_info)
                    else:
                        print("No more next blocks to load.")
                        break
                print("Analysis is ready.")
                visualize_block_data(selected_blocks)
                current_hash = selected_blocks[0]['Hash']  # reset to the initial hash
                selected_blocks = []
            elif command == 's':
                selected_blocks.append(block_info)
                print("Block selected for analysis.")
            elif command == 'q':
                print("Exiting block navigation.")
                break
            else:
                print("Invalid command, please use '+', '-', 's', 'a', or 'q'.")
        else:
            print("Failed to retrieve block information.")
            break

    if selected_blocks != []: visualize_block_data(selected_blocks)

def visualize_block_data(blocks):
    """Visualise plusieurs aspects des blocs sélectionnés."""
    heights = [block['Height'] for block in blocks]
    fees = [block['Fees'] for block in blocks]
    sizes = [block['Size'] for block in blocks]
    transactions = [block['NbTransactions'] for block in blocks]
    times = [block['Time'] for block in blocks]

    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    highlight_color = 'magenta'  # Couleur pour le premier bloc

    # Frais de Minage
    axs[0, 0].scatter(heights[1:], fees[1:], color='red')  # autres blocs en rouge
    axs[0, 0].scatter(heights[0], fees[0], color=highlight_color, label='Potential Selfish Attack', edgecolors='black')  # premier bloc en magenta
    axs[0, 0].set_title('Mining Fees (BTC) vs. Block Height')
    axs[0, 0].set_xlabel('Block Height')
    axs[0, 0].set_ylabel('Mining Fees (BTC)')
    axs[0, 0].legend()

    # Taille des Blocs
    axs[0, 1].scatter(heights[1:], sizes[1:], color='blue')
    axs[0, 1].scatter(heights[0], sizes[0], color=highlight_color, edgecolors='black')
    axs[0, 1].set_title('Block Size vs. Block Height')
    axs[0, 1].set_xlabel('Block Height')
    axs[0, 1].set_ylabel('Block Size (Bytes)')

    # Nombre de Transactions
    axs[1, 0].scatter(heights[1:], transactions[1:], color='green')
    axs[1, 0].scatter(heights[0], transactions[0], color=highlight_color, edgecolors='black')
    axs[1, 0].set_title('Number of Transactions vs. Block Height')
    axs[1, 0].set_xlabel('Block Height')
    axs[1, 0].set_ylabel('Number of Transactions')


    # Nombre de Transaction vs Frais de Minage
    axs[1, 1].scatter(transactions[1:], fees[1:], color='purple')
    axs[1, 1].scatter(transactions[0], fees[0], color=highlight_color, edgecolors='black')
    axs[1, 1].set_title('Number of Transactions vs. Mining Fees')
    axs[1, 1].set_xlabel('Mining Fees')
    axs[1, 1].set_ylabel('Number of Transactions')


    plt.tight_layout()
    plt.show()

def analyze_surrounding_blocks(block_hash):
    """Analyse les blocs de N-5 à N+5 autour du bloc spécifié."""
    initial_block = get_block_info_from_api(block_hash)
    if isinstance(initial_block, str):  # Vérification si l'appel API a échoué.
        print(initial_block)
        return

    block_height = initial_block['Height']
    start_height = block_height - 5
    end_height = block_height + 5

    blocks = []
    for height in range(start_height, end_height + 1):
        block = get_block_by_height(height)
        if isinstance(block, str):  # Vérification si l'appel API a échoué pour un bloc spécifique.
            print(block)
            continue
        blocks.append(block)

    visualize_block_data(blocks)