import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from sympy import true

from .scale_bar import add_scale_bar
import cv2
from matplotlib import patheffects


def scan_and_save_images(image: np.ndarray,
                         step: int = 10000,
                         bbox: tuple = (-1, 1, -1, 1),
                         output_dir: str = "pictures",
                         prefix: str = "test_2_") -> int:
    """
    Сканирует изображение по шагам по ширине, применяет размерную линейку к сегментам и сохраняет файлы
    с использованием Matplotlib для отображения и сохранения.

    :param image: Исходное изображение (np.ndarray, формат BGR).
    :param bbox: (xmin, xmax, ymin, ymax) — полный диапазон для всего изображения.
    :param step: Размер сегмента по ширине в пикселях.
    :param output_dir: Директория для сохранения.
    :param prefix: Префикс имени файлов.
    :return: Количество сохранённых файлов.
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Изображение должно быть в формате BGR с тремя каналами.")
    
    height, width = image.shape[:2]
    num_segments = (width + step - 1) // step  # Округление вверх для остатка
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    saved_count = 0
    
    xmin, xmax, ymin, ymax = bbox  # Разбор полного bbox
    delta_x = xmax - xmin  # Полный диапазон X
    
    for i in range(num_segments):
        print(i)
        start_col = i * step
        end_col = min((i + 1) * step, width)
        segment = image[:, start_col:end_col]
        
        if segment.shape[1] == 0:
            break
        # segment = add_scale_bar(segment, left_margin_percent=0.1)
        segment = cv2.cvtColor(segment, cv2.COLOR_BGR2RGB)
        
        # Расчёт extent для сегмента с X, увеличивающейся вправо
        start_frac = start_col / width
        end_frac = end_col / width
        x_left = xmin + start_frac * delta_x  # X левой границы (меньшее значение)
        x_right = xmin + end_frac * delta_x  # X правой границы (большее значение)
        segment_extent = (int(x_left / 1000), int(x_right / 1000), int(ymax / 1000), int(ymin / 1000))
        
        # Сохранение
        filename = f"{prefix}{i + 1}.png"
        filepath = output_path / filename
        #save_matplotlib(segment, segment_extent, filepath)
        save_original(segment, filepath)
        saved_count += 1
    return saved_count


def save_original(segment, filepath):
    cv2.imwrite(str(filepath), segment)

def save_matplotlib(segment, segment_extent, filepath):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    ax.imshow(segment, extent=segment_extent, origin='upper')
    
    ax.tick_params(
        axis='x', direction='in', pad=-20, length=5, colors='white', labelcolor='black',
        labelbottom=True
    )
    for label in ax.get_xticklabels():
        label.set_ha('center')
        label.set_va('center')
        label.set_path_effects([patheffects.withStroke(linewidth=3, foreground='white')])
    ax.yaxis.set_visible(False)
    ax.get_xticklabels()[0].set_visible(False)
    ax.get_xticklabels()[-1].set_visible(False)
    
    try:
        plt.savefig(str(filepath), bbox_inches='tight', pad_inches=0, dpi=300)
    except Exception as e:
        print(f"Ошибка сохранения {filename}: {e}")
    finally:
        plt.close(fig)  # Освобождение ресурсов
    return true