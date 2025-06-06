import re

def split_entries(text: str) -> list:
    """Splits text into entries based on pattern: case number at the beginning of a line."""
    # Using regex to extract blocks starting with a number
    pattern = r'(?=(?:^|\n)\d{1,3}\.\s)'
    entries = re.split(pattern, text)
    # Remove empty entries and trim
    return [e.strip() for e in entries if e.strip()]

def remove_artifacts(text: str) -> str:
    # Removing single garbage characters
    return re.sub(r'(?<=\s)[|©®¤](?=\s)|^[|©®¤]$', '', text, flags=re.MULTILINE)

def merge_hyphenated_words(text: str) -> str:
    # Merging words split with hyphens
    return re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

def merge_wrapped_lines(text: str) -> str:
    lines = text.splitlines()
    merged_lines = []

    for line in lines:
        stripped = line.lstrip()
        if not merged_lines:
            merged_lines.append(line)
        elif stripped and stripped[0].isdigit():
            # If first visible character is a digit - start new line
            merged_lines.append(line)
        else:
            # Otherwise merge with previous line
            merged_lines[-1] += ' ' + line.strip()

    return '\n'.join(merged_lines)

# Common OCR error fixes
OCR_FIXES = {
    ' Ф Ф Ф ': '',
    ' .': '.',
    ' ,': ',',
    '  ': ' ',
    '..': '.',
    '. . .': '...',
    ' . .': '...',
}

def apply_ocr_fixes(text: str) -> str:
    for wrong, correct in OCR_FIXES.items():
        text = text.replace(wrong, correct)
    return text

def final_trim_and_normalize(text: str) -> str:
    # Normalizing spaces, removing empty lines, normalizing line breaks
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    return text.strip()

def clean_text(text: str) -> str:
    # Global text cleaning
    text = remove_artifacts(text)
    text = merge_hyphenated_words(text)
    text = merge_wrapped_lines(text)
    text = apply_ocr_fixes(text)
    text = final_trim_and_normalize(text)

    # After cleaning - split into entries
    entries = split_entries(text)
    return '\n'.join(entries)