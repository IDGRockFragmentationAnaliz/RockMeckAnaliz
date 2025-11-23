import numpy as np
import cv2
from pathlib import Path
from .scale_bar import add_scale_bar

def scan_and_save_images(image: np.ndarray, step: int = 10000, output_dir: str = "pictures",
                         prefix: str = "test_2_") -> int:
    """
    Сканирует изображение по шагам, применяет размерную линейку к сегментам и сохраняет файлы.

    :param image: Исходное изображение (np.ndarray, формат BGR).
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
    
    for i in range(num_segments):
        start_row = i * step
        end_row = min((i + 1) * step, height)
        segment = image[start_row:end_row, :]
        
        if segment.shape[0] == 0:
            break
        
        # Применение размерной линейки
        segment_with_scale = add_scale_bar(segment, left_margin_percent=0.1)
        
        # Сохранение
        filename = f"{prefix}{i + 1}.png"
        filepath = output_path / filename
        success = cv2.imwrite(str(filepath), segment_with_scale)
        
        if success:
            saved_count += 1
        else:
            print(f"Ошибка сохранения: {filename}")
    
    return saved_count