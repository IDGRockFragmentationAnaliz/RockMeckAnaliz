import numpy as np
import matplotlib.pyplot as plt
from pyrockstats.distrebutions import lognorm
from pyrockstats import ecdf

def main():
    x = np.load('./temp/stat_shapes.npy')
    
    # Исключение максимального значения
    max_val = np.max(x)
    x_filtered = x[x < max_val]
    
    # Вычисление минимума и максимума отфильтрованных данных
    xmin = np.min(x_filtered)
    xmax = np.max(x_filtered)
    
    # Создание логарифмических бинов (50 бинов для детализации)
    bins = np.logspace(np.log10(xmin), np.log10(xmax), num=20)
    
    # Фиттинг логнормального распределения на отфильтрованных данных
    theta = lognorm.fit(x_filtered, xmin=xmin, xmax=xmax)
    dist = lognorm(*theta)
    
    # Вычисление PDF на центрах бинов
    bin_centers = (bins[:-1] + bins[1:]) / 2
    pdf = dist.pdf(bin_centers)
    cdf = dist.cdf(bin_centers)
    values, e_freq = ecdf(x_filtered)
    
    # Построение графика
    fig = plt.figure(figsize=(8, 8))
    ax = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]
    ax[0].hist(x_filtered, bins=bins, density=True, alpha=0.6, color='blue', label='Гистограмма')
    ax[0].plot(bin_centers, pdf, 'r-', linewidth=2, label='PDF логнормального распределения')
    ax[0].set_xscale('log')
    ax[0].set_xlabel('Значения (лог масштаб)')
    ax[0].set_ylabel('Плотность')
    ax[0].legend()
    
    ax[1].plot(values, e_freq, label='ecdf')
    ax[1].plot(bin_centers, cdf, label='lognorm')
    ax[1].set_xscale('log')
    ax[1].legend()
    plt.show()


# Вызов функции (если требуется)
if __name__ == "__main__":
    main()