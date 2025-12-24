import numpy as np
import matplotlib.pyplot as plt
from pyrockstats.distrebutions import lognorm, paretoexp, weibull
from pyrockstats import ecdf

def main():
    x = np.load('./temp/stat_shapes.npy')
    x = x/16
    # Исключение максимального значения
    max_val = np.max(x)
    x_filtered = x[x < max_val]
    x_filtered = x_filtered[x_filtered > 11**2]
    
    
    
    # Вычисление минимума и максимума отфильтрованных данных
    xmin = np.min(x_filtered)
    xmax = np.max(x_filtered)
    
    # Создание логарифмических бинов (50 бинов для детализации)
    bins = np.logspace(np.log10(xmin), np.log10(xmax), num=10)
    
    model = {"pareto": paretoexp, "lognorm": lognorm, "weibull": weibull}
    
    # Фиттинг логнормального распределения на отфильтрованных данных
    
    
    # Вычисление PDF на центрах бинов
    bin_centers = (bins[:-1] + bins[1:]) / 2
    pdf1, cdf1 = get_stats(model["lognorm"], x_filtered, xmin, xmax, bin_centers)
    pdf2, cdf2 = get_stats(model["pareto"], x_filtered, xmin, xmax, bin_centers)
    pdf3, cdf3 = get_stats(model["weibull"], x_filtered, xmin, xmax, bin_centers)
    
    values, e_freq = ecdf(x_filtered)
    
    # Построение графика
    fig = plt.figure(figsize=(8, 8))
    ax = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]
    ax[0].hist(x_filtered, bins=bins, density=True, alpha=0.6, color='blue', label='Гистограмма')
    ax[0].plot(bin_centers, pdf1, linewidth=2, label='PDF lognorm', color='blue')
    ax[0].plot(bin_centers, pdf2, linewidth=2, label='PDF power', color='r')
    ax[0].plot(bin_centers, pdf3, linewidth=2, label='PDF weibull', color='g')
    ax[0].set_xscale('log')
    ax[0].set_xlabel('м')
    ax[0].set_ylabel('Плотность')
    ax[0].legend()
    
    ax[1].plot(values, e_freq, label='ecdf', color='black')
    ax[1].plot(bin_centers, cdf1, label='cdf lognorm', color='blue')
    ax[1].plot(bin_centers, cdf2, label='cdf lognorm', color="r")
    ax[1].plot(bin_centers, cdf3, label='cdf weibull', color="g")
    ax[1].set_xscale('log')
    ax[1].legend()
    plt.show()


def get_stats(model, x, xmin, xmax, bin_centers):
    theta = model.fit(x, xmin=xmin, xmax=xmax)
    dist = model(*theta)
    
    pdf = dist.pdf(bin_centers)
    cdf = dist.cdf(bin_centers)
    
    return pdf, cdf

# Вызов функции (если требуется)
if __name__ == "__main__":
    main()