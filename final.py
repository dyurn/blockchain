import requests
import datetime
import time as t
import sys
import matplotlib.pyplot as plt
import numpy as np
from functions import *

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
    blocks_info = []
    
    for day in range(days):
        day_time = current_time - datetime.timedelta(days=day)
        timestamp = int(day_time.timestamp() * 1000)
        blocks = get_blocks_for_day(timestamp)
        if blocks:
            blocks_info.extend([{'time': block['time'], 'hash': block['hash']} for block in blocks])
        print_progress_bar(day + 1, days, prefix='Progress:', suffix='Complete', length=50)   
    
    return blocks_info

if __name__ == "__main__":

    top = 3
    days = 30
    T = []

    blocks_info = get_blocks(days=days)
    block_times = [block['time'] for block in blocks_info]
    average = int(len(block_times)/days)
    print("Average blocks per day :", average)
    sorted_blocks = sorted(blocks_info, key=lambda x: x['time'])
    intervals = np.diff([block['time'] for block in sorted_blocks]) / 60  # minutes
    hashes = [block['hash'] for block in sorted_blocks[1:]]
    
    intervals_with_hashes = list(zip(intervals, hashes))
    intervals_with_hashes.sort(reverse=True, key=lambda x: x[0])
    longest_intervals = intervals_with_hashes[:top]
    
    daily_average = np.convolve(intervals, np.ones((average,))/average, mode='valid')

    plt.figure(figsize=(12, 8))
    plt.scatter(range(len(intervals)), intervals, color='blue', s=1, label='Block Time (minutes)')
    plt.plot(range(len(daily_average)), daily_average, color='black', label='Daily Average')
    plt.title(f'Bitcoin Block Times Over {days} Days')
    plt.xlabel('Block Number')
    plt.ylabel('Block Time (minutes)')
    plt.legend()
    plt.show()

    print(f"\nTop {top} blocks with the longest mining times:")
    for i, (interval, hash) in enumerate(longest_intervals, 1):
        print(f"{style.BRIGHT}{i}. Interval: {interval:.2f} minutes")
        block = get_block_info_from_api(hash)
        print_block_infos(block, mode=1)
        T.append(block)

    while(True):
        choice = input(f"Select a block to start navigation (1-{top}) or 'q' to quit: ")
        if choice.isdigit() and 1 <= int(choice) <= top:
            block_hash = T[int(choice) - 1]['Hash']
            navigate_blocks(block_hash)
        elif choice == 'q':
            break
        else:
            print(f"Invalid input, please enter a number between 1 and {top}, or 'q' to quit.")
        


    #print(get_block_info_from_api(get_latest_block_hash()))
    #print(longest_intervals)