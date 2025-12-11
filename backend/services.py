import os
import requests
from typing import List, Dict
from pathlib import Path
from ultralytics import YOLO
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")

class YoloService:
    def __init__(self):
        # specific logic to find the trained model if it exists
        # usually stored in runs/detect/train/weights/best.pt relative to where script is run
        # We will look for it, otherwise fall back to 'yolov8n.pt'
        possible_paths = [
            "runs/weights/best.pt",
            "../runs/weights/best.pt",
            "runs/detect/train/weights/best.pt",
            "../runs/detect/train/weights/best.pt",
            "yolov8n.pt"  # Fallback
        ]
        self.model_path = "yolov8n.pt"
        for path in possible_paths:
            if os.path.exists(path):
                self.model_path = path
                print(f"Loading custom model from: {path}")
                break
        
        if self.model_path == "yolov8n.pt":
             print("Custom model not found. Using generic YOLOv8n (expect poor results for specific fridge items until training is done).")

        self.model = YOLO(self.model_path)

    def detect(self, image_path: str) -> Dict:
        """
        Run inference on an image.
        Returns cleaned labels and detection details for visualization.
        """
        results = self.model(image_path)
        
        detected_items = []
        labels_raw = []

        # Process results
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # get label name
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                
                # get coords (xyxy) - normalized or pixels? pixels is default
                xyxy = box.xyxy[0].tolist()
                
                detected_items.append({
                    "label": label,
                    "bbox": xyxy,
                    "confidence": float(box.conf[0])
                })
                labels_raw.append(label)
        
        unique_ingredients = self._clean_labels(labels_raw)
        
        return {
            "detections": detected_items,
            "ingredients": unique_ingredients
        }

    def _clean_labels(self, labels: List[str]) -> List[str]:
        """
        Clean up labels for the API:
        - Lowercase
        - Remove underscores
        - Remove dash suffixes (e.g., "Ash Gourd -Kubhindo-" -> "ash gourd")
        - Remove duplicates
        """
        import re
        cleaned = set()
        for label in labels:
            # normalization
            l = label.lower().strip()
            l = l.replace("_", " ")
            # Remove content after hyphen if it looks like a local name suffix
            # e.g. "ash gourd -kubhindo-"
            l = re.sub(r'\s*-.*$', '', l)
            cleaned.add(l)
        return list(cleaned)

class SpoonacularService:
    def __init__(self):
        self.base_url = "https://api.spoonacular.com"
        self.api_key = SPOONACULAR_API_KEY

    def find_recipes_by_ingredients(self, ingredients: List[str], number: int = 5) -> List[Dict]:
        if not self.api_key:
            return []
        
        if not ingredients:
            return []
            
        endpoint = f"{self.base_url}/recipes/findByIngredients"
        ingredients_str = ",".join(ingredients)
        
        params = {
            "apiKey": self.api_key,
            "ingredients": ingredients_str,
            "number": number,
            "ignorePantry": True,
            "ranking": 1
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            initial_recipes = response.json()
            
            if not initial_recipes:
                return []
                
            # Fetch details for URLs
            recipe_ids = [str(r['id']) for r in initial_recipes]
            ids_str = ",".join(recipe_ids)
            
            bulk_endpoint = f"{self.base_url}/recipes/informationBulk"
            bulk_params = {
                "apiKey": self.api_key,
                "ids": ids_str
            }
            
            bulk_response = requests.get(bulk_endpoint, params=bulk_params)
            bulk_response.raise_for_status()
            details = bulk_response.json()
            
            details_map = {d['id']: d for d in details}
            
            final_recipes = []
            for r in initial_recipes:
                d = details_map.get(r['id'])
                if d:
                    r['sourceUrl'] = d.get('sourceUrl')
                    r['readyInMinutes'] = d.get('readyInMinutes')
                    r['summary'] = d.get('summary')
                    final_recipes.append(r)
            
            return final_recipes
        
        except requests.exceptions.HTTPError as e:
            # HTTP errors from Spoonacular (e.g., 401 Unauthorized, 402 Quota, etc.)
            resp = e.response
            try:
                body = resp.text
            except Exception:
                body = '<unreadable body>'
            print(f"Spoonacular HTTPError: status={resp.status_code}, body={body}")
            return []
        except Exception as e:
            # Generic fallback
            print(f"Error fetching recipes: {str(e)}")
            return []
