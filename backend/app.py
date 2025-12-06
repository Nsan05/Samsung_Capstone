from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid
from services import YoloService, SpoonacularService

app = FastAPI(title="VisionChef API")

# Allow CORS for local frontend execution
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development convenience
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

@app.post("/analyze_fridge")
async def analyze_fridge(file: UploadFile = File(...)):
    # 1. Save uploaded file
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"temp_uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 2. Detect Ingredients
        detection_result = yolo_service.detect(file_path)
        detected_ingredients = detection_result["ingredients"]
        detections = detection_result["detections"] # Metadata with bboxes
        
        # 3. Fetch Recipes
        recipes = []
        if detected_ingredients:
            recipes = spoonacular_service.find_recipes_by_ingredients(detected_ingredients)
            
        return {
            "detected_ingredients": detected_ingredients,
            "raw_detections": detections, # Frontend can use this to draw boxes
            "recipes": recipes,
            "image_id": filename
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optional: Clean up file after processing, 
        # but might want to keep it if we serve it back. 
        # For now, let's keep it to verify.
        pass

# Simple way to serve the uploaded images if needed (though client has the original)
# app.mount("/files", StaticFiles(directory="temp_uploads"), name="files")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
