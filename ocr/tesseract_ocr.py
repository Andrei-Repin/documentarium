import pytesseract
from typing import Dict, List, Tuple

def get_ocr_text(image, settings):
    """
    Распознаёт текст на изображении с помощью Tesseract OCR.

    Args:
        image (numpy.ndarray): Входное изображение
        settings (dict): Настройки обработки, включая язык
        
    Returns:
        str: Распознанный текст
    """
    lang_option = settings.get('OCR_LANGUAGE', 'auto').lower()

    lang_map = {
        'rus': 'rus',
        'deu': 'deu',
        'lav': 'lav',
        'auto': 'rus+deu+lav'
    }

    lang = lang_map.get(lang_option, 'rus+deu+lav')

    custom_config = r'--oem 3 --psm 6'
    ocr_data = pytesseract.image_to_data(
        image, lang=lang, config=custom_config, output_type=pytesseract.Output.DICT
    )

    lines = {}
    n = len(ocr_data['text'])

    for i in range(n):
        text = ocr_data['text'][i].strip()
        if text and int(ocr_data['conf'][i]) > 50:
            key = (ocr_data['block_num'][i], ocr_data['par_num'][i], ocr_data['line_num'][i])
            lines.setdefault(key, []).append(text)

    sorted_lines = [' '.join(lines[k]) for k in sorted(lines.keys()) if lines[k]]
    return '\n'.join(sorted_lines)
