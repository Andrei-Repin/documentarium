## Documentarium – v0.2.0
# Archival Inventories and Documents Processing Tool

A tool for processing and recognizing archival inventories and documents, with support for typewritten and handwritten text.

## 📌 Features

- 📄 Support for various document types:
  - Typewritten (typewritten)
  - Handwritten (handwritten - in development)
- 🔄 Automatic image processing:
  - Rotation and alignment
  - Edge cropping
  - Contrast enhancement
- ✨ Text recognition:
  - Tesseract OCR for printed/typewritten text
  - Kraken (в разработке) для рукописного текста
- 🔧 Text post-processing:
  - Text cleanup and error correction
  - Spell-checking with custom dictionaries
  - Text transformation for database import

## 🛠 Installation

1. Clone the repository:
```bash
git clone https://github.com/Andrei-Repin/documentarium.git
cd documentarium
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Install Tesseract OCR:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Linux:
```bash
sudo apt install tesseract-ocr tesseract-ocr-rus tesseract-ocr-deu tesseract-ocr-lav
```
- MacOS:
```bash
brew install tesseract
```
## 🚀 Usage

1. Place images in the input_images folder.
2. Run the processing script:
```bash
python main.py
```
## ⚙ Configuration

Main settings can be adjusted in config/settings.py.

## 📁 Project Structure

documentarium/  
├── config/                          # Configuration files  
│   └── settings.py                  # Main settings for paths, OCR, and processing  
│  
├── image_processing/                # Image preprocessing modules  
│   ├── image_processing.py          # Main image processing pipeline  
│   ├── brightness_contrast.py       # Brightness and contrast adjustment  
│   ├── rotation.py                  # Auto-alignment and manual rotation  
│   └── cropping.py                  # Edge-based image cropping  
│  
├── ocr/                             # Text recognition modules  
│   ├── tesseract_ocr.py             # OCR using Tesseract (printed/typewritten text)  
│   └── kraken_ocr.py                # OCR using Kraken (handwritten text)  
│  
├── postprocessing/                  # Post-processing of recognized text  
│   ├── text_cleanup.py              # Noise removal, line break fixes, error correction  
│   ├── spell_check.py               # Spell-checking with custom dictionaries  
│   └── structure_parser.py          # Text transformation into tabular format (TSV)  
│  
├── logs/                            # System logs  
│   └── spell_log.txt                # Spell-checking correction log  
│  
├── resources/                       # Additional resources and dictionaries  
│   └── dictionaries/  
│       └── ru_RU/                   # Russian language (Hunspell)  
│           ├── ru_RU.aff            # Main aff dictionary file  
│           ├── ru_RU.dic            # Main dic dictionary file  
│           └── custom_ru/           # Custom dictionaries  
│               ├── common_ru.txt    # Frequent words not in the base dictionary  
│               ├── locations_ru.txt # Geographic names  
│               └── names_ru.txt     # First names, surnames, patronymics  
│  
├── utils/                           # General utilities  
│   ├── file_utils.py                # File and directory operations  
│   └── image_utils.py               # Helper functions for image processing  
│  
├── input_images/                    # Input images (before processing)  
├── processed_images/                # Images after preprocessing  
│  
├── output/                          # Recognition results  
│   ├── recognized_text.txt          # Raw OCR output  
│   ├── cleaned_text.txt             # Text after cleanup  
│   ├── spell_checked_text.txt       # Text after spell-checking  
│   ├── recognized_text.tsv          # Final structured table  
│   └── spell_diff.html              # Visual comparison of spelling corrections  
│  
├── main.py                          # Main processing script  
├── README.md                        # Project documentation  
└── requirements.txt                 # Python dependencies  

## 🛣️ Planned improvements (roadmap)

- Improved robustness to diverse image conditions
  The current image preprocessing scripts are optimized for relatively uniform conditions (e.g., good lighting, minimal distortion, no strong shadows). Support for more challenging input (e.g., shadows, skewed angles, variable lighting) is planned.
- Post-processing of printed OCR text
  Ongoing work includes improving the correction of common OCR errors, such as misrecognized characters, broken lines, and formatting issues. More advanced error correction mechanisms are planned.
- Handwritten text recognition
  Planned integration of OCR models capable of recognizing handwritten text in various styles.

## 📁 Archive notice and previous development

Note: The earlier development stage focusing on image preprocessing is archived and no longer maintained.
You can find the archived version here: [image-preprocessing](https://github.com/Andrei-Repin/image-preprocessing)

## 🤝 How to Contribute

1. Fork the repository.
2. Create a feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a Pull Request.

## 📜 License

Distributed under the MIT License. See LICENSE for details.


🛠 Developed by: Andrei Repin
📧 Contact: baltic.ancestors.riga@gmail.com
🔗 Website: baltic-ancestors.com