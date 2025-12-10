import numpy as np
import cv2
from tools.scale_bar import add_scale_bar
from tools.scanner import scan_and_save_images
import matplotlib.pyplot as plt
from matplotlib import patheffects


def main():
    points = np.load("temp/point_matrix_cut_y.npy")
    points1 = points[:, [0, 2]]
    points2 = points[:, [3, 5]]
    
    line_len = np.sum((points1 - points2) ** 2, axis=1)
    
    xmin = np.float64(-6286.746784151837)# np.min(np.column_stack((points1[:, 0], points2[:, 0])))
    xmax = np.float64(11319.462734331075)# np.max(np.column_stack((points1[:, 0], points2[:, 0])))
    ymin = np.min(np.column_stack((points1[:, 1], points2[:, 1])))
    ymax = np.max(np.column_stack((points1[:, 1], points2[:, 1])))
    
    height, width = int((ymax - ymin) / 2), int((xmax - xmin) / 2)
    bbox = (xmin, xmax, ymin, ymax)
    
    # Создание нулевого изображения (чёрный фон)
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Отрисовка линий
    for p1, p2 in zip(points1, points2):
        # Нормализация и сдвиг координат
        x1 = int((p1[0] - xmin) / (xmax - xmin) * (width - 1))
        y1 = int((p1[1] - ymin) / (ymax - ymin) * (height - 1))
        x2 = int((p2[0] - xmin) / (xmax - xmin) * (width - 1))
        y2 = int((p2[1] - ymin) / (ymax - ymin) * (height - 1))
        
        # Отрисовка линии (белый цвет, толщина 1)
        cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 11)
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    ax.imshow(image, extent=bbox, origin='upper')#
    ax.invert_yaxis()
    
    ax.tick_params(
        axis='y', direction='in', pad=-20, length=5, colors='white', labelcolor='black',
        labelleft=True,
        labelrotation=90
    )
    for label in ax.get_yticklabels():
        label.set_ha('center')
        label.set_va('center')
        label.set_path_effects([patheffects.withStroke(linewidth=3, foreground='white')])
    ax.xaxis.set_visible(False)
    ax.get_yticklabels()[0].set_visible(False)
    ax.get_yticklabels()[-1].set_visible(False)
    plt.savefig("pictures/127.5.png", bbox_inches='tight', pad_inches=0, dpi=300)
    plt.show()
    
    

if __name__ == '__main__':
    main()