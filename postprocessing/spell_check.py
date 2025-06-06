import re
import logging
from pathlib import Path
from typing import Tuple, List
from spylls.hunspell import Dictionary
from pymorphy2 import MorphAnalyzer

class SpellCorrector:
    def __init__(self, dict_dir: str, custom_dict_path: str = None, log_path: str = 'spell_log.txt'):
        self.dictionary = Dictionary.from_files(str(Path(dict_dir) / 'ru_RU'))

        self.morph = MorphAnalyzer()

        self.custom_words = set()
        custom_dir = Path(custom_dict_path) if custom_dict_path else None
        
        if custom_dir and custom_dir.exists():
            for file in custom_dir.glob("*.txt"):
                with file.open(encoding='utf-8') as f:
                    words = {line.strip().lower() for line in f if line.strip()}
                    self.custom_words.update(words)
        else:
            print(f"[!] Custom dictionaries directory not found: {custom_dict_path}")

        self.logger = logging.getLogger('SpellChecker')
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            fh = logging.FileHandler(log_path, mode='w', encoding='utf-8')
            fh.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(fh)

    def check_and_correct_spelling(self, text: str) -> Tuple[str, List[str]]:
        def replace_word(match):
            word = match.group(0)
            stripped = word.strip(".,!?–—\":;()[]«»").lower()
            if not stripped.isalpha():
                return word  # Skip numbers, symbols, etc.
        
            # Check against custom dictionaries
            if stripped in self.custom_words:
                return word
        
            # Check word forms using pymorphy2
            parsed = self.morph.parse(stripped)
            if parsed and any(p.normal_form in self.custom_words for p in parsed):
                return word
        
            # Check in main Hunspell dictionary
            if self.dictionary.lookup(stripped):
                return word
        
            # Correct if word is unknown
            suggestions = list(self.dictionary.suggest(stripped))
            if suggestions:
                suggestion = suggestions[0]
                corrected = re.sub(stripped, suggestion, word, flags=re.IGNORECASE)
                self.logger.info(f'Correction: "{word}" → "{corrected}", Suggestions: {suggestions}')
                return corrected
            else:
                self.logger.info(f'Unknown word: "{word}" (cleaned: "{stripped}"), Suggestions: []')
                return word
    
        corrected_text = re.sub(r'\b[\w\-]+\b', replace_word, text)
        return corrected_text, []  # can return list of differences if needed

def correct_spelling(text: str, settings: dict) -> Tuple[str, List[str]]:
    """
    Applies spell checking and correction using provided settings.

    Args:
        text (str): The text to check.
        settings (dict): Configuration dictionary with keys:
            - 'HUNSPELL_DICT_PATH'
            - 'CUSTOM_DICTIONARIES_DIR'
            - 'SPELLCHECK_LOG_PATH'

    Returns:
        Tuple[str, List[str]]: Corrected text and empty list (for compatibility).
    """
    corrector = SpellCorrector(
        dict_dir=settings.get('HUNSPELL_DICT_PATH', 'resources/dictionaries/ru_RU'),
        custom_dict_path=settings.get('CUSTOM_DICTIONARIES_DIR'),
        log_path=settings.get('SPELLCHECK_LOG_PATH', 'logs/spell_log.txt')
    )
    return corrector.check_and_correct_spelling(text)