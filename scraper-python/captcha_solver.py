import pytesseract
import cv2
import requests
import base64
import logging
import yaml
import pathlib

# Load configurations
with open(pathlib.Path(__file__).parent / "config.yaml", "r") as config_file:

    config = yaml.safe_load(config_file)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CaptchaSolver:
    def __init__(self):
        self.service = config["captcha_solver"].get("service", "local-ocr")
        self.api_key = config["captcha_solver"].get("api_key", None)

    def solve_local(self, image_path):
        """Solve CAPTCHA using local OCR (Tesseract)."""
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(thresh, config='--psm 6')
        return text.strip()

    def solve_remote(self, image_path):
        """Solve CAPTCHA using external API services like 2Captcha or AntiCaptcha."""
        if not self.api_key:
            logging.error("API key is missing for external CAPTCHA solving.")
            return None
        
        with open(image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        
        payload = {
            "method": "base64",
            "key": self.api_key,
            "body": base64_image,
            "json": 1
        }
        
        response = requests.post("http://2captcha.com/in.php", data=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == 1:
                captcha_id = result.get("request")
                logging.info(f"CAPTCHA submitted. ID: {captcha_id}")
                return self._get_solution(captcha_id)
        logging.error("Failed to submit CAPTCHA.")
        return None

    def _get_solution(self, captcha_id):
        """Retrieve CAPTCHA solution from external service."""
        url = f"http://2captcha.com/res.php?key={self.api_key}&action=get&id={captcha_id}&json=1"
        for _ in range(10):
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == 1:
                    return result.get("request")
        logging.error("Failed to retrieve CAPTCHA solution.")
        return None

    def solve(self, image_path):
        """Decide which method to use for CAPTCHA solving."""
        if self.service == "local-ocr":
            return self.solve_local(image_path)
        elif self.service in ["2captcha", "anticaptcha"]:
            return self.solve_remote(image_path)
        else:
            logging.error("Invalid CAPTCHA solving service.")
            return None

# Example usage
if __name__ == "__main__":
    solver = CaptchaSolver()
    captcha_text = solver.solve("captcha_image.png")
    logging.info(f"Solved CAPTCHA: {captcha_text}")
