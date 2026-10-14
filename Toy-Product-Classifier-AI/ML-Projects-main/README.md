# Toy Product Classifier (AI image classification)

This project provides a simple web app where you upload a photo and get likely toy categories (toy car, doll, teddy bear, ball, robot, etc.) plus the top 5 scores. It uses the pretrained OpenAI CLIP model through Hugging Face Transformers. It does not require you to train a model or provide a labeled dataset.

## Requirements
- Python 3.10 or 3.11 recommended
- Internet connection on the first run, so the pretrained model can be downloaded
- Several GB of free disk space recommended for Python packages and cached model files

## Run on Windows (VS Code)
1. Extract the ZIP file.
2. Open the `ML-Projects-main` folder in VS Code.
3. Open Terminal in that folder.
4. Create a virtual environment (recommended):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
5. Install packages:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   python -m streamlit run app.py
   ```
7. A local web page will open. Upload a PNG/JPG/JPEG/WebP image and click **Classify toy**.

Alternatively, double-click `run_app.bat`; it installs dependencies and starts the app.

## Included files
- `app.py`: upload-and-classify web app
- `sample_product.png`: sample toy car image
- `ToyProductClassifier.py`: original image-feature extraction demo
- `requirements.txt`: dependencies
- `run_app.bat`: Windows launch helper

## Important notes
- The first app launch downloads the pretrained CLIP model and can take time. Keep the internet connection on.
- It is a zero-shot classifier: predictions are based on candidate text labels and may be wrong, especially for unusual toys or poor-quality photos.
- Displayed scores are relative model scores, not guaranteed real-world probabilities.
- If PowerShell blocks activation, you can skip virtual-environment activation and run `python -m pip install -r requirements.txt` directly.
