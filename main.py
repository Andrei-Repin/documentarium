import os
import difflib
import html
from utils.file_utils import recognize_ready_images, process_images_from_folder
from config.settings import settings
from postprocessing.text_cleanup import clean_text
from postprocessing.spell_check import correct_spelling
from postprocessing.structure_parser import format_text_to_table, format_as_tsv

# Ensure output directory exists
os.makedirs(settings['OUTPUT_DIR'], exist_ok=True)

if __name__ == "__main__":
    if settings.get('SKIP_PREPROCESSING'):
        recognize_ready_images(settings)
    else:
        process_images_from_folder(
            input_folder=settings['INPUT_FOLDER'],
            processed_folder=settings['PROCESSED_FOLDER'],
            output_text_file=os.path.join(settings['OUTPUT_DIR'], 'recognized_text.txt'),
            settings=settings
        )

    # Load OCR text
    recognized_text_path = os.path.join(settings['OUTPUT_DIR'], 'recognized_text.txt')
    with open(recognized_text_path, encoding='utf-8') as f:
        raw_text = f.read()

    if settings.get('ENABLE_POSTPROCESSING'):
        # === Stage 1: Text cleaning ===
        cleaned = clean_text(raw_text)
        cleaned_path = os.path.join(settings['OUTPUT_DIR'], 'cleaned_text.txt')
        with open(cleaned_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        # === Stage 2: Spell checking ===
        corrected, _ = correct_spelling(cleaned, settings)
        corrected_path = os.path.join(settings['OUTPUT_DIR'], 'spell_checked_text.txt')
        with open(corrected_path, 'w', encoding='utf-8') as f:
            f.write(corrected)

        # === Stage 3: Change comparison (HTML) ===
        cleaned_lines = cleaned.splitlines()
        corrected_lines = corrected.splitlines()
        
        diff_html = ['<html><head><meta charset="utf-8"><style>',
                     'body { font-family: monospace; background: #fdfdfd; }',
                     '.diff { white-space: pre-wrap; }',
                     '.add { background-color: #c8facc; }',
                     '.del { background-color: #fdd; text-decoration: line-through; }',
                     '</style></head><body>']
        diff_html.append('<h2>Spell check comparison</h2>')
        
        has_diff = False
        
        for i, (cl, cr) in enumerate(zip(cleaned_lines, corrected_lines), 1):
            if cl != cr:
                has_diff = True
                sm = difflib.SequenceMatcher(None, cl, cr)
                chunks = []
                for opcode, i1, i2, j1, j2 in sm.get_opcodes():
                    if opcode == 'equal':
                        chunks.append(html.escape(cl[i1:i2]))
                    elif opcode == 'replace':
                        chunks.append(f'<span class="del">{html.escape(cl[i1:i2])}</span><span class="add">{html.escape(cr[j1:j2])}</span>')
                    elif opcode == 'delete':
                        chunks.append(f'<span class="del">{html.escape(cl[i1:i2])}</span>')
                    elif opcode == 'insert':
                        chunks.append(f'<span class="add">{html.escape(cr[j1:j2])}</span>')
        
                diff_html.append(f'<div class="diff"><strong>Line {i}:</strong><br>{"".join(chunks)}</div><hr>')
        
        diff_html.append('</body></html>')
        
        if has_diff:
            html_path = os.path.join(settings['OUTPUT_DIR'], 'spell_diff.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(diff_html))
            print(f"\nHTML comparison saved to: {html_path}")
        else:
            print("\nNo differences found between cleaned and corrected text.")

        # === Stage 4 temporarily disabled: saving only spell_checked_text.txt ===
        # rows = format_text_to_table(corrected)
        # tsv = format_as_tsv(rows)
        # tsv_path = os.path.join(settings['OUTPUT_DIR'], 'recognized_text.tsv')
        # with open(tsv_path, 'w', encoding='utf-8') as f:
        #     f.write(tsv)

        print(f"\nPost-processing completed.") 
    else:
        print("\nPost-processing disabled (ENABLE_POSTPROCESSING=False)")