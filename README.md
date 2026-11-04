# ⚽ EA FC & FIFA 3D Kit Layer Generator

An automated Python processing pipeline designed for sports simulation modders. It converts flat 2D graphic assets (club crests, badges, sponsor logos) into photorealistic **Normal Maps** and **SRS (Smoothness/Roughness/Metalness) coefficient maps** tailored for the EA Sports Frostbite Engine.

---

## 📸 Sample Visual Outputs

This tool calculates pixel-level spatial gradients and hue ranges to convert 2D vectors and images into fully articulated 3D bump maps used directly in-game:

| Raja Club Athletic Crest (`RCA_-layer`) | ITT Tanger Crest (`TANGER_-layer`) |
| :---: | :---: |
| ![Raja Club Athletic Normal Map](samples/RCA_-layer.jpg) | ![ITT Tanger Normal Map](samples/TANGER_-layer.jpg) |

---

## ⚡ Features

* **Dynamic Normal Map Generation (`generate_normal_map.py`):**
  * Uses 2D Sobel operators (`scipy.signal.convolve2d` with a spatial fallback) to compute surface gradients[cite: 15].
  * Adjustable `--intensity` flag to tune the depth and embossing effect of 3D logos[cite: 15].
  * Preserves native alpha channels for clean transparency in kit rendering[cite: 15].
* **SRS Texture Generation (`generate_coeff_texture.py`):**
  * Channel-mapped texture generation for the Frostbite engine material pipeline:
    * **Red Channel (Metalness):** Automatically detects gold/metallic regions and assigns high reflectivity.
    * **Blue Channel (Smoothness):** Controls glossiness vs. matte fabric finishes.

---

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **Core Libraries:** NumPy, Pillow (PIL), SciPy (optional for accelerated convolution)[cite: 15]

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Python installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ea-fc-kit-layer-generator.git
   cd ea-fc-kit-layer-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 Usage

### 1. Generating a Normal Map (3D Relief)

Run the script specifying your input image and optional relief intensity:

```bash
python generate_normal_map.py --input logo.png --intensity 2.5
```
> **Output:** Generates `logo_-layer.png` ready for import into FIFA Editor Tool or Frostbite Mod Manager[cite: 15].

### 2. Generating an SRS Coefficient Texture

Convert a color texture into a specular/roughness map:

```bash
python generate_coeff_texture.py
```

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
