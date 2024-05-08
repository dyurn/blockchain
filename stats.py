import matplotlib.pyplot as plt
import numpy as np
from functions import *

if __name__ == "__main__":

    days = 30
    block_times = get_blocks(days=days)
    average = int(len(block_times)/days)
    print("Average blocks per day :", average)
    intervals = np.diff(sorted(block_times)) / 60  # minutes

    daily_average = np.convolve(intervals, np.ones((average,))/average, mode='valid')

    plt.figure(figsize=(12, 8))
    plt.scatter(range(len(intervals)), intervals, color='blue', s=1, label='Block Time (minutes)')
    plt.plot(range(len(daily_average)), daily_average, color='black', label='Daily Average')
    plt.title(f'Bitcoin Block Times Over {days} Days')
    plt.xlabel('Block Number')
    plt.ylabel('Block Time (minutes)')
    plt.legend()
    plt.show()
