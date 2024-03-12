import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import requests
from image_processing.images import image_urls


def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for invalid response
        image_data = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"Error loading image from URL: {e}")
        return None


def calculate_image_metrics(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    laplacian_var = round(laplacian_var)

    # Calculate noise
    mean = np.mean(gray)
    stddev = np.std(gray)
    noise = stddev / mean * 100
    noise = round(noise)

    # Calculate contrast
    contrast = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 2].std()
    contrast = round(contrast)

    # Calculate saturation
    saturation = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 1].std()
    saturation = round(saturation)

    # Calculate SSIM score (using a reference image, or the image itself as reference)
    ssim_score = ssim(gray, gray, full=True)[0]

    # Calculate brightness
    brightness = np.mean(gray)
    brightness = round(brightness)

    return laplacian_var, noise, contrast, saturation, ssim_score, brightness


def detect_humans(image):
    # Load the pre-trained Haar Cascade classifier for human faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If any faces are detected, consider humans are present in the image
    if len(faces) > 0:
        return True
    else:
        return False


def is_photo_clear(laplacian_var, noise, contrast, saturation, ssim_score, brightness):
    # Define thresholds for clarity assessment
    laplacian_var_threshold = list(range(20, 17000))  # Provided value
    noise_threshold = list(range(20, 140))  # Provided value
    contrast_threshold = list(range(25, 100))  # Provided value
    saturation_threshold = list(range(8, 110))  # Provided value
    ssim_threshold = 1.5  # Provided value
    brightness_threshold = list(range(30, 200))  # Adjust as needed

    # Check if the image meets the clarity criteria
    if (laplacian_var in laplacian_var_threshold and
            noise in noise_threshold and
            contrast in contrast_threshold or
            brightness > 100 and laplacian_var > 15 and
            saturation in saturation_threshold and
            ssim_score < ssim_threshold and
            brightness in brightness_threshold):
        return True
    else:
        return False


def process_images(image_urls):
    for idx, image_url in enumerate(image_urls):
        print(f"Processing Image {idx + 1}: {image_url}")
        image = load_image_from_url(image_url)

        if image is not None:
            laplacian_var, noise, contrast, saturation, ssim_score, brightness = calculate_image_metrics(image)

            print(f"Laplacian Variance: {laplacian_var}")
            print(f"Noise: {noise}")
            print(f"Contrast: {contrast}")
            print(f"Saturation: {saturation}")
            print(f"SSIM Score: {ssim_score}")
            print(f"Brightness: {brightness}")


            # Check if the image is clear
            is_clear = is_photo_clear(laplacian_var, noise, contrast, saturation, ssim_score, brightness)
            print("Is the image clear?", is_clear)
        else:
            print(f"Failed to load the image from URL: {image_url}")
        print()


if __name__ == "__main__":
    process_images(image_urls)
