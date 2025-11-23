import numpy as np
import cv2


def add_scale_bar(image: np.ndarray, scale_length: int = None, position: tuple[int, int] = None,
                  line_thickness: int = None, text_size: float = None, text_thickness: int = None,
                  left_margin_percent: float = 0.05, top_margin_percent: float = 0.01) -> np.ndarray:
    """
    Добавляет размерную линейку с подписью на изображение, автоматически адаптируясь к его размеру.
    Текст занимает ровно 5% от высоты изображения. Линия отображается как прямоугольная полоса без искажений.

    :param image: Входное изображение (np.ndarray, формат BGR).
    :param scale_length: Длина линейки в пикселях (и метрах). Если None, автоматически 10% ширины.
    :param position: Координаты (x, y) начала линейки. Если None, верхний левый угол с отступами.
    :param line_thickness: Толщина линии. Если None, автоматически пропорционально высоте текста.
    :param text_size: Размер шрифта подписи. Если None, автоматически для 5% высоты.
    :param text_thickness: Толщина текста. Если None, автоматически пропорционально высоте текста.
    :param left_margin_percent: Процент отступа слева и справа от ширины (по умолчанию 0.05).
    :param top_margin_percent: Процент отступа сверху от высоты (по умолчанию 0.01).
    :return: Модифицированное изображение (np.ndarray).
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Изображение должно быть в формате BGR с тремя каналами.")
    
    height, width = image.shape[:2]
    
    # Автоматическая длина линейки
    if scale_length is None:
        scale_length = max(10, int(width * 0.1))
    
    # Целевая высота текста (5% от высоты изображения)
    target_text_height = int(0.05 * height)
    
    # Подготовка текста
    text = f"{scale_length} m"
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Начальная оценка размера текста
    initial_text_size = max(0.5, height / 2000.0)
    initial_text_thickness = max(1, int(initial_text_size))
    
    # Измерение фактической высоты при начальной оценке
    (text_width, text_height), _ = cv2.getTextSize(text, font, initial_text_size, initial_text_thickness)
    
    # Корректировка размера текста для точной высоты
    if text_height > 0:
        scale_factor = target_text_height / text_height
        text_size = initial_text_size * scale_factor
    else:
        text_size = initial_text_size
    
    # Финальная толщина текста (пропорционально высоте)
    if text_thickness is None:
        text_thickness = max(1, int(target_text_height / 10))
    
    # Пересчёт размеров с финальным text_size
    (text_width, text_height), _ = cv2.getTextSize(text, font, text_size, text_thickness)
    
    # Толщина линии (пропорционально высоте текста)
    if line_thickness is None:
        line_thickness = max(1, int(text_height / 5))
    
    # Автоматическая позиция с процентными отступами
    if position is None:
        left_margin = int(left_margin_percent * width)
        top_margin = int(top_margin_percent * height)
        x_start = left_margin
        y_start = top_margin + int(0.1 * text_height) + line_thickness // 2  # Центрирование толщины
    else:
        x_start, y_start = position
    
    # Корректировка длины с учетом правого отступа
    right_margin = int(left_margin_percent * width)
    x_end = min(x_start + scale_length, width - right_margin)
    scale_length = x_end - x_start
    y_end = y_start
    
    # Копирование изображения
    result = image.copy()
    
    # Отрисовка линии как прямоугольной полосы (без закруглений)
    y_line_top = y_start - line_thickness // 2
    y_line_bottom = y_start + line_thickness // 2 + 1  # +1 для полного покрытия
    cv2.rectangle(result, (x_start, y_line_top), (x_end, y_line_bottom), (255, 255, 255), -1)
    
    # Позиция текста (строго центрирована под линией)
    text_x = x_start + (scale_length - text_width) // 2
    text_y = y_end + text_height + int(0.1 * text_height)  # Отступ под линией
    
    # Отрисовка текста
    cv2.putText(result, text, (text_x, text_y), font, text_size, (255, 255, 255), text_thickness)
    
    return result