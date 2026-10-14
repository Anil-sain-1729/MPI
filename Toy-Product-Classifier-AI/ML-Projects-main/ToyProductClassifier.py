"""
Toy Product Classifier - image + tabular + text feature demo

Run:
    python ToyProductClassifier.py

Keep sample_product.png in the same folder as this Python file.
Install dependencies:
    python -m pip install pillow numpy pandas
"""

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "sample_product.png"


def load_image_features(image_path: Path) -> np.ndarray:
    """Load the supplied product photo and turn it into 64 grayscale features."""
    if not image_path.is_file():
        raise FileNotFoundError(
            f"Product photo was not found: {image_path}\n"
            "Place sample_product.png in the same folder as ToyProductClassifier.py."
        )

    # Resize to a small, consistent size so the feature vector has a fixed length.
    with Image.open(image_path) as image:
        grayscale = image.convert("L").resize((8, 8))
        pixels = np.asarray(grayscale, dtype=np.float32) / 255.0

    return pixels.flatten()


def main() -> None:
    # Example product information (tabular features).
    products = pd.DataFrame(
        {
            "Product": ["Red Toy SUV", "Toy Robot", "Building Blocks", "Toy Train"],
            "Category": ["Toys", "Toys", "Toys", "Toys"],
            "Price": [499, 699, 299, 399],
        }
    )

    category_codes = {"Toys": 0}
    products["Category_Code"] = products["Category"].map(category_codes)

    # Load the actual photo included with this project.
    image_features = load_image_features(IMAGE_PATH)

    print("=" * 58)
    print("TOY PRODUCT CLASSIFIER - PHOTO LOADED SUCCESSFULLY")
    print("=" * 58)
    print(f"Photo: {IMAGE_PATH.name}")
    print(f"Original photo is converted to grayscale and resized to 8 x 8.")
    print(f"Image feature count: {image_features.size}")
    print(f"First 10 normalized pixel values: {np.round(image_features[:10], 3)}")

    print("\nProduct table:")
    print(products.to_string(index=False))

    # Simple text features for the example product.
    product_name = "Red Toy SUV"
    words = product_name.lower().split()
    vocabulary = {word: index + 1 for index, word in enumerate(sorted(set(words)))}
    text_features = [vocabulary[word] for word in words]

    print(f"\nExample product name: {product_name}")
    print(f"Text tokens: {words}")
    print(f"Text feature IDs: {text_features}")

    # Combine example numeric, image, and text features.
    numeric_features = products.loc[0, ["Price", "Category_Code"]].to_numpy(dtype=float)
    combined_features = np.concatenate(
        [numeric_features, image_features, np.asarray(text_features, dtype=float)]
    )

    print(f"\nCombined feature vector length: {combined_features.size}")
    print("First 12 combined features:", np.round(combined_features[:12], 3))
    print("\nDemo complete. This script extracts features; it does not train a real classifier yet.")


if __name__ == "__main__":
    main()
