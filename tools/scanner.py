import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from .scale_bar import add_scale_bar
import cv2
from matplotlib import patheffects

def scan_and_save_images(image: np.ndarray,
                         step: int = 10000,
                         bbox: tuple = (-1, 1, -1, 1),
                         output_dir: str = "pictures",
                         prefix: str = "test_2_") -> int:
    """
    Сканирует изображение по шагам, применяет размерную линейку к сегментам и сохраняет файлы
    с использованием Matplotlib для отображения и сохранения.

    :param image: Исходное изображение (np.ndarray, формат BGR).
    :param bbox: (xmin, xmax, ymin, ymax) — полный диапазон для всего изображения.
    :param step: Размер сегмента по высоте в пикселях.
    :param output_dir: Директория для сохранения.
    :param prefix: Префикс имени файлов.
    :return: Количество сохранённых файлов.
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Изображение должно быть в формате BGR с тремя каналами.")
    
    height, width = image.shape[:2]
    num_segments = (height + step - 1) // step  # Округление вверх для остатка
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    saved_count = 0
    
    xmin, xmax, ymin, ymax = bbox  # Разбор полного bbox
    delta_y = ymax - ymin  # Полный диапазон Y
    
    for i in range(num_segments):
        print(i)
        start_row = i * step
        end_row = min((i + 1) * step, height)
        segment = image[start_row:end_row, :]
        
        if segment.shape[0] == 0:
            break
        # segment = add_scale_bar(segment, left_margin_percent=0.1)
        segment = cv2.cvtColor(segment, cv2.COLOR_BGR2RGB)
        
        # Расчёт extent для сегмента с Y, увеличивающейся вниз
        start_frac = start_row / height
        end_frac = end_row / height
        y_top = ymin + start_frac * delta_y  # Y верхней границы (меньшее значение)
        y_bottom = ymin + end_frac * delta_y  # Y нижней границы (большее значение)
        segment_extent = (int(xmin / 1000), int(xmax / 1000), int(y_bottom / 1000), int(y_top / 1000))
        
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        ax.imshow(segment, extent=segment_extent, origin='upper')
        
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
        # Сохранение
        filename = f"{prefix}{i + 1}.png"
        filepath = output_path / filename
        try:
            plt.savefig(str(filepath), bbox_inches='tight', pad_inches=0, dpi=300)
            saved_count += 1
        except Exception as e:
            print(f"Ошибка сохранения {filename}: {e}")
        finally:
            plt.close(fig)  # Освобождение ресурсов
    
    return saved_count