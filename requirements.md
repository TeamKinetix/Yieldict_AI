# Machine Learning Training: File Extensions & Formats Reference

This guide covers the essential file extensions and formats used across different stages of the machine learning training pipeline.

---

## 1. Code & Environment Files
These files are used to write training code and manage environment dependencies.

*   **`.py` (Python Script):** Standard executable Python code. Best for production pipelines and automated training scripts.
*   **`.ipynb` (Jupyter Notebook):** Interactive notebooks. Best for data exploration, rapid prototyping, and inline data visualization.
*   **`requirements.txt`:** Text file listing required Python packages (e.g., `torch==2.3.0`). Used to reinstall dependencies via `pip install -r requirements.txt`.
*   **`environment.yml`:** YAML configuration file used to recreate exact Anaconda virtual environments.

---

## 2. Dataset Files (Input Data)
These are the files you download or prepare to feed into your machine learning models.

### Tabular Data
*   **`.csv` (Comma-Separated Values):** Simple, human-readable text format. Universal but slow for massive datasets.
*   **`.parquet` / `.feather`:** Optimized, compressed binary formats. Highly recommended for big data because they load into memory instantly.

### Computer Vision (Images/Video)
*   **`.jpg` / `.png` / `.webp`:** Standard image formats. Usually compressed together into a `.zip` or `.tar.gz` archive for bulk downloading.

### Natural Language Processing (Text/LLMs)
*   **`.txt`:** Raw, unformatted plain text.
*   **`.json` / `.jsonl`:** Structured text files. `.jsonl` (JSON Lines) stores one valid JSON object per line and is the industry standard for fine-tuning Large Language Models (LLMs).

---

## 3. Model Weights & Artifacts (Outputs)
These files store your trained model parameters or serve as pre-trained foundations for transfer learning.

### PyTorch Ecosystem
*   **`.safetensors`:** The modern industry standard. Secure, fast format for saving model weights that prevents arbitrary code execution.
*   **`.pt` / `.pth`:** Traditional PyTorch saving formats. Stores weights or full model state dictionaries.

### TensorFlow / Keras Ecosystem
*   **`.keras` / `.h5`:** HDF5-based formats used to save model architecture, weights, and training configurations.
*   **`.pb` (Protocol Buffers):** Used by TensorFlow for frozen computation graphs, ideal for production deployment.

### Classical Machine Learning (Scikit-Learn)
*   **`.joblib` / `.pkl` (Pickle):** Serializes Python objects. Used to save traditional models like Random Forests, Linear Regressions, or data scalers.

### Cross-Platform Deployment
*   **`.onnx` (Open Neural Network Exchange):** A universal framework-agnostic format. Used to convert a model from one framework (like PyTorch) so it can run efficiently in another language or hardware setup (e.g., C++ or mobile).
