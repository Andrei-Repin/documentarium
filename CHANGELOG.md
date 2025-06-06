# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Roadmap section in the README.
- Reference to the previous development stage ([image-preprocessing](https://github.com/Andrei-Repin/image-preprocessing)).
- Initial roadmap for handwritten OCR via Kraken.
- Postprocessing pipeline: structure parsing (partial implementation).

---

## [0.2.0] – 2025-06-06

### Added
- Project reorganized under a new repository: `documentarium`.
- Modular pipeline for preprocessing, OCR, and postprocessing.
- Language-specific dictionary system.
- Tesseract OCR module.
- Postprocessing pipeline: text cleanup.
- Spell-check module using custom and Hunspell dictionaries (partial implementation).
- `.gitignore` to exclude large image files and output text.

---

## [0.1.0] – 2025-04-09  
*(formerly in [image-preprocessing](https://github.com/Andrei-Repin/image-preprocessing))*

### Changed and Improved:
- **Processing settings centralized** into a `settings` dictionary for easier configuration (e.g., toggling OCR, cropping, rotation, binarization, etc.).
- **Advanced cropping and rotation logic added:**
  - Fine control over side cropping via `CROP_SIDE_PAGE`, `CROP_SIDE_DIRECTION`, and `SIDE_WHITE_RATIO_THRESHOLD`.
  - Optional fine rotation based on text angle detection using Hough lines (`FINE_ROTATION`, `get_text_angle_by_hough()`).
- **Improved image preprocessing:**
  - Added `FORCE_GRAYSCALE` option for enforcing grayscale mode regardless of source.
  - Enhanced contrast adjustment now ignores top and bottom 1% pixel values to avoid extreme shifts.
- **OCR added**: Integration with Tesseract OCR using explicit language specification (`rus+deu+lat`). Previously a placeholder, this now performs real text recognition.
- **Document type system introduced** for applying different image processing and OCR strategies depending on the document type (e.g., typeset vs handwritten).
  - Currently only typeset documents are supported; handwritten recognition will be added in future versions.
- **Decoupled processing pipeline**: It is now possible to run image preprocessing separately from OCR.
- **Error handling improvements**: Added validation for unreadable images and invalid angle extraction.
- **Code readability improvements**: Clearer variable and function names, plus added inline comments.
