# Edge Compass

Computes the most frequent edge orientation in a static image.

This project loads a static grayscale image (generated internally for standalone execution), detects edges using the Canny algorithm, and then computes the single most frequent edge orientation (in degrees) found among all detected edge pixels. All visual output is saved to disk, ensuring compatibility with headless server environments.

## Setup

1.  **Clone the repository (or save the files):**
    ```bash
    git clone https://github.com/your-username/edge-compass.git
    cd edge-compass
    ```
    (Note: Replace `your-username/edge-compass` with your actual repo path if you host it.)

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## How to Run

Simply execute the `main.py` script:

```bash
python main.py
```

The script will:
1.  Generate a synthetic grayscale image with various lines.
2.  Perform Canny edge detection.
3.  Compute the orientation of each detected edge pixel.
4.  Determine and print the single most frequent edge orientation.
5.  Save the generated image and the Canny edge map to an `output/` directory.

### Example Output

```
--- Edge Compass Project ---
1. Generating synthetic grayscale image...
   Generated image saved to output/generated_image.png
2. Detecting edges using Canny...
   Canny edges image saved to output/canny_edges.png
3. Computing pixel gradient orientations...
4. Filtering orientations to Canny edge pixels...
   Found 1024 edge pixels.
5. Computing the most frequent edge orientation...

Result: Most frequent edge orientation: 0.50 degrees

All visual outputs (generated_image.png, canny_edges.png) saved in the 'output' directory.
```

The `output` directory will contain `generated_image.png` (the input) and `canny_edges.png` (the detected edges).