import cv2
import numpy as np
import os

def generate_synthetic_image(width=200, height=200):
    """
    Generates a simple grayscale image with distinct lines at various orientations.
    """
    img = np.zeros((height, width), dtype=np.uint8)

    # Draw a diagonal line (45 degrees)
    cv2.line(img, (0, 0), (width - 1, height - 1), 255, 2)
    # Draw another diagonal line (-45 or 135 degrees)
    cv2.line(img, (width - 1, 0), (0, height - 1), 255, 2)
    # Draw a vertical line (90 degrees)
    cv2.line(img, (width // 2, 0), (width // 2, height - 1), 255, 2)
    # Draw a horizontal line (0 degrees)
    cv2.line(img, (0, height // 2), (width - 1, height // 2), 255, 2)
    # Draw a thicker horizontal line to ensure it's often the dominant orientation
    cv2.line(img, (0, height // 4), (width - 1, height // 4), 255, 5) 
    
    return img

def main():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    print("--- Edge Compass Project ---")

    # 1. Generate/Load Grayscale Image
    print("1. Generating synthetic grayscale image...")
    image = generate_synthetic_image()
    
    # Save the generated image
    generated_image_path = os.path.join(output_dir, "generated_image.png")
    cv2.imwrite(generated_image_path, image)
    print(f"   Generated image saved to {generated_image_path}")

    # 2. Canny Edge Detection
    print("2. Detecting edges using Canny...")
    # Canny parameters: image, low_threshold, high_threshold
    # A common heuristic is high_threshold = 2 or 3 * low_threshold
    edges = cv2.Canny(image, 50, 150)
    
    # Save the Canny edges image
    canny_edges_path = os.path.join(output_dir, "canny_edges.png")
    cv2.imwrite(canny_edges_path, edges)
    print(f"   Canny edges image saved to {canny_edges_path}")

    # 3. Compute Gradient and Orientation
    print("3. Computing pixel gradient orientations...")
    # Calculate gradients using Sobel operators
    # cv2.CV_64F is used for float output to avoid overflow and precision issues
    # during gradient calculations, especially for arctan2.
    dx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # Compute orientation for all pixels using arctan2
    # np.arctan2 returns angles in radians in the range [-pi, pi]
    orientation_rad = np.arctan2(dy, dx)

    # Convert radians to degrees
    orientation_deg = np.degrees(orientation_rad)

    # Normalize angles to the [0, 180) range, which is typical for edge orientations.
    # For an edge, 0 degrees (horizontal) is considered the same orientation as 180 degrees.
    # Similarly, -45 degrees is the same orientation as 135 degrees.
    # The formula (angle + 180) % 180 maps angles from [-180, 180] to [0, 180).
    normalized_orientations = (orientation_deg + 180) % 180

    # 4. Filter Orientations to only include Canny edge pixels
    print("4. Filtering orientations to Canny edge pixels...")
    # Create a boolean mask from the Canny edges (where pixel value > 0)
    edge_mask = edges > 0
    edge_orientations = normalized_orientations[edge_mask]

    if len(edge_orientations) == 0:
        print("   No edges detected to compute orientation. Exiting.")
        return

    print(f"   Found {len(edge_orientations)} edge pixels.")

    # 5. Compute the single most frequent edge orientation
    print("5. Computing the most frequent edge orientation...")
    # Use numpy.histogram to bin the angles into 1-degree bins.
    # The range (0, 180) means bins are [0,1), [1,2), ..., [179,180).
    # With bins=180, bin_edges will be [0, 1, ..., 180].
    hist, bin_edges = np.histogram(edge_orientations, bins=180, range=(0, 180))

    # Find the index of the bin with the maximum count
    max_count_idx = np.argmax(hist)

    # The most frequent orientation is represented by the midpoint of this bin.
    # For 1-degree bins, this is simply the bin's lower edge + 0.5.
    most_frequent_orientation = bin_edges[max_count_idx] + 0.5 

    print(f"\nResult: Most frequent edge orientation: {most_frequent_orientation:.2f} degrees")
    print(f"\nAll visual outputs (generated_image.png, canny_edges.png) saved in the '{output_dir}' directory.")

if __name__ == "__main__":
    main()