import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt



def main():
    headers = load_headers()

    data_path = Path(".") / "data/CSAF_M1.focmec_pub"
    df = pd.read_csv(data_path, sep=" ", names=headers)
    lat = df["latitude"].to_numpy()
    lon = df["longitude"].to_numpy()
    depth = df["depth"].to_numpy()
    #
    strike = df["strike"].to_numpy()
    dip = df["dip"].to_numpy()
    rake = df["rake"].to_numpy()

    # Выбираем 5 случайных индексов
    random_indices = np.random.choice(len(df), size=5, replace=False)
    # Рисуем все три вектора
    # ax.quiver(lon[i], lat[i], depth[i], dx_strike, dy_strike, dz_strike,
    #           color='blue', label='Strike' if i == 0 else "", length=vector_length)

    print(strike)
    exit()
    lat = lat[random_indices]
    lon = lon[random_indices]
    depth = depth[random_indices]
    #
    strike = strike[random_indices]
    dip = dip[random_indices]
    rake = rake[random_indices]



    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(lon, lat, depth,
                         c=depth, cmap='viridis', s=20, alpha=0.7)

    plt.show()


def load_headers():
    with open("data/headers.txt", 'r', encoding='utf-8') as f:
        headers = [line.strip().split(' ', 1)[1] for line in f]
    return headers

if __name__ == '__main__':
    main()

