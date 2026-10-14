from pathlib import Path
import streamlit as st
from PIL import Image
import torch
from transformers import CLIPModel, CLIPProcessor

APP_DIR = Path(__file__).resolve().parent
MODEL_NAME = "openai/clip-vit-base-patch32"
CANDIDATES = [
    "a photo of a toy car", "a photo of a toy truck", "a photo of a toy train",
    "a photo of a toy airplane", "a photo of a toy robot", "a photo of a doll",
    "a photo of a teddy bear", "a photo of a toy ball", "a photo of building blocks",
    "a photo of a toy dinosaur", "a photo of a toy boat", "a photo of a toy kitchen set",
    "a photo of a toy action figure", "a photo of a toy bicycle", "a photo of a puzzle toy",
    "a photo of a toy gun", "a photo of a toy house", "a photo of a toy helicopter",
    "a photo of a toy drum", "a photo of a toy product"
]

st.set_page_config(page_title="Toy Product Classifier", page_icon="🧸", layout="centered")
st.title("🧸 Toy Product Classifier")
st.write("Upload a toy photo to predict its most likely category using a pretrained CLIP vision-language model.")
st.info("First run needs internet to download the model (about several hundred MB). Predictions are estimates, not guarantees.")

@st.cache_resource(show_spinner="Loading AI model (first run may take a few minutes)...")
def load_model():
    processor = CLIPProcessor.from_pretrained(MODEL_NAME)
    model = CLIPModel.from_pretrained(MODEL_NAME)
    model.eval()
    return processor, model

uploaded = st.file_uploader("Choose a product photo", type=["png", "jpg", "jpeg", "webp"])
if uploaded is None:
    sample = APP_DIR / "sample_product.png"
    if sample.exists():
        st.caption("No photo uploaded? The included sample toy car is shown below.")
        st.image(Image.open(sample), caption="Sample toy car", use_container_width=True)
    st.stop()

try:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Uploaded photo", use_container_width=True)
    if st.button("Classify toy", type="primary"):
        with st.spinner("Analyzing image..."):
            processor, model = load_model()
            inputs = processor(text=CANDIDATES, images=image, return_tensors="pt", padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
                probs = outputs.logits_per_image.softmax(dim=1)[0]
            top = torch.topk(probs, k=5)
        best_label = CANDIDATES[int(top.indices[0])].replace("a photo of ", "").strip()
        st.success(f"Prediction: {best_label.title()}")
        st.metric("Model confidence (relative score)", f"{float(top.values[0]) * 100:.1f}%")
        st.subheader("Top 5 possible categories")
        for idx, score in zip(top.indices.tolist(), top.values.tolist()):
            label = CANDIDATES[idx].replace("a photo of ", "").strip().title()
            st.write(f"**{label}** — {score * 100:.1f}%")
        st.caption("Scores are relative across the candidate labels. They should not be treated as calibrated probabilities.")
except Exception as exc:
    st.error("Could not classify this image. Check your internet connection and installed packages, then try again.")
    st.exception(exc)
