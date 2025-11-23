import numpy as np
import cv2
from tools.scale_bar import add_scale_bar
from tools.scanner import scan_and_save_images


def main():
    points = np.load("temp/point_matrix.npy")
    points1 = points[:,0:2]
    points2 = points[:,3:5]
    line_len = np.sum((points1 - points2)**2, axis=1)
    
    xmin = np.min(np.column_stack((points1[:, 0], points2[:,0])))
    xmax = np.max(np.column_stack((points1[:, 0], points2[:,0])))
    ymin = np.min(np.column_stack((points1[:, 1], points2[:, 1])))
    ymax = np.max(np.column_stack((points1[:, 1], points2[:, 1])))
    
    height, width = int((ymax - ymin)/2), int((xmax - xmin)/2)
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
    
    scan_and_save_images(image, bbox=bbox)



if __name__ == '__main__':
    main()