import numpy as np
import cv2
from tools.scale_bar import add_scale_bar
from tools.scanner import scan_and_save_images


def main():
    points = np.load("temp/point_matrix.npy").astype(np.float64)
    points1: np.ndarray = points[:,0:2]
    points2: np.ndarray = points[:,3:5]
    line_len = np.sum((points1 - points2)**2, axis=1)

    xmin: float = np.min(np.column_stack((points1[:, 0], points2[:,0])))
    xmax: float = np.max(np.column_stack((points1[:, 0], points2[:,0])))
    ymin: float = np.min(np.column_stack((points1[:, 1], points2[:, 1])))
    ymax: float = np.max(np.column_stack((points1[:, 1], points2[:, 1])))
    
    scale = 0.25
    height, width = int((ymax - ymin)*scale), int((xmax - xmin)*scale)
    bbox = (xmin, xmax, ymin, ymax)
    
    #
    
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
        cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), int(10*scale+1))
    
    from pyrocksegmentation.basic_segmentator import Segmentator
    from pyrocksegmentation import Extractor
    
    image1d,_,_ = cv2.split(image)
    segmentator = Segmentator(image1d)
    market_image = segmentator.run(extend=False)
    stat_shapes = Extractor(market_image).extruct()
    
    np.save('./temp/stat_shapes.npy', stat_shapes)
    
    #image = segmentator.get_segment_image()
    #print(image.shape)
    #scan_and_save_images(image, step=5000, bbox=bbox)
    


#def y_line(image, y_target):
#     y_target = 127500
#     if ymin <= y_target <= ymax:
#         y_img = int((y_target - ymin) / (ymax - ymin) * (height - 1))
#         # Отрисовка красной горизонтальной линии (от левого до правого края)
#         cv2.line(image, (0, y_img), (width - 1, y_img), (0, 0, 255), 11)
#     else:
#         print("Предупреждение: y=127500 выходит за пределы bounding box по y.")

if __name__ == '__main__':
    main()