from roboflow import Roboflow
from ultralytics import YOLO
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def train_model():
    print("Downloading dataset from Roboflow...")
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise ValueError("ROBOFLOW_API_KEY not found in .env file")
        
    rf = Roboflow(api_key=api_key)
    project = rf.workspace("samsung-capstone").project("food-in-fridge-2slx4-asarp")
    version = project.version(1)
    dataset = version.download("yolov8")

    print("Starting YOLOv8 training...")
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    # checks relative to the current working directory for dataset location
    data_yaml_path = f"{dataset.location}/data.yaml"
    
    # Train for a reasonable number of epochs (e.g., 20) for transfer learning
    results = model.train(data=data_yaml_path, epochs=20, imgsz=640)
    
    print("Training complete.")
    print(f"Best model weights should be saved in: {results.save_dir}/weights/best.pt")

if __name__ == "__main__":
    train_model()
