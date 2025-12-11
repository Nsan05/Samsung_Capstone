from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file BEFORE importing services
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

from services import YoloService, SpoonacularService

app = FastAPI(title="VisionChef API")


# Allow CORS for local frontend execution
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
yolo_service = YoloService()
spoonacular_service = SpoonacularService()

# Ensure temp directory exists
os.makedirs("temp_uploads", exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "VisionChef API is running"}

@app.get("/health")
def health_check():
    """Health check endpoint - also shows API key status"""
    spoon_key = os.getenv("SPOONACULAR_API_KEY")
    roboflow_key = os.getenv("ROBOFLOW_API_KEY")
    return {
        "status": "healthy",
        "spoonacular_key_loaded": bool(spoon_key),
        "roboflow_key_loaded": bool(roboflow_key),
    }

@app.post("/analyze_fridge")
async def analyze_fridge(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"temp_uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Detect Ingredients
        detection_result = yolo_service.detect(file_path)
        detected_ingredients = detection_result["ingredients"]
        detections = detection_result["detections"]
        
        # Fetch Recipes
        recipes = []
        if detected_ingredients:
            try:
                recipes = spoonacular_service.find_recipes_by_ingredients(detected_ingredients)
            except Exception as recipe_error:
                print(f"Recipe fetching failed: {recipe_error}")
                recipes = []
            
        return {
            "detected_ingredients": detected_ingredients,
            "raw_detections": detections,
            "recipes": recipes,
            "image_id": filename
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Simple way to serve the uploaded images if needed (though client has the original)
# app.mount("/files", StaticFiles(directory="temp_uploads"), name="files")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
