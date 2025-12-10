<<<<<<< HEAD
# ------------------------------
# app.py
# ------------------------------

# 1️⃣ Load environment variables from .env
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file in backend folder

# Optional: Test if keys are loaded
print("Spoonacular Key:", os.getenv("SPOONACULAR_API_KEY"))
print("Roboflow Key:", os.getenv("ROBOFLOW_API_KEY"))

# 2️⃣ Import other modules
=======
>>>>>>> 5d49f6c6b3898b81e67e64cb55c32255fadebba0
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
<<<<<<< HEAD
import uuid
from services import YoloService, SpoonacularService

# 3️⃣ Initialize FastAPI
app = FastAPI(title="VisionChef API")

# 4️⃣ Allow CORS for local frontend development
=======
import os
import uuid
from services import YoloService, SpoonacularService

app = FastAPI(title="VisionChef API")

# Allow CORS for local frontend execution
>>>>>>> 5d49f6c6b3898b81e67e64cb55c32255fadebba0
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development convenience
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# 5️⃣ Initialize services
yolo_service = YoloService()
spoonacular_service = SpoonacularService()

# 6️⃣ Ensure temporary uploads folder exists
os.makedirs("temp_uploads", exist_ok=True)

# 7️⃣ Root endpoint
=======
# Services
yolo_service = YoloService()
spoonacular_service = SpoonacularService()

# Ensure temp directory exists
os.makedirs("temp_uploads", exist_ok=True)

>>>>>>> 5d49f6c6b3898b81e67e64cb55c32255fadebba0
@app.get("/")
def read_root():
    return {"message": "VisionChef API is running"}

<<<<<<< HEAD
# 8️⃣ Analyze fridge endpoint
@app.post("/analyze_fridge")
async def analyze_fridge(file: UploadFile = File(...)):
    # Save uploaded file
=======
@app.post("/analyze_fridge")
async def analyze_fridge(file: UploadFile = File(...)):
    # 1. Save uploaded file
>>>>>>> 5d49f6c6b3898b81e67e64cb55c32255fadebba0
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"temp_uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
<<<<<<< HEAD
    
    try:
        print(f"Processing image: {filename}")
        
        # Detect Ingredients
        print("Running YOLO detection...")
        detection_result = yolo_service.detect(file_path)
        detected_ingredients = detection_result.get("ingredients", [])
        detections = detection_result.get("detections", [])
        
        print(f"Detected ingredients: {detected_ingredients}")
        
        # Fetch Recipes
        recipes = []
        if detected_ingredients:
            print("Fetching recipes from Spoonacular API...")
            recipes = spoonacular_service.find_recipes_by_ingredients(detected_ingredients)
            print(f"Retrieved {len(recipes)} recipes")
        else:
            print("No ingredients detected")
        
        response_data = {
            "detected_ingredients": detected_ingredients,
            "raw_detections": detections,
            "recipes": recipes,
            "image_id": filename
        }
        
        print(f"Response: {len(detected_ingredients)} ingredients, {len(recipes)} recipes")
        return response_data
    
    except Exception as e:
        import traceback
        print(f"Error during analysis: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    finally:
        # Optional: Keep files or delete later
        pass

# 9️⃣ Serve uploaded images if needed
# app.mount("/files", StaticFiles(directory="temp_uploads"), name="files")

# 10️⃣ Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
=======
        
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
>>>>>>> 5d49f6c6b3898b81e67e64cb55c32255fadebba0
