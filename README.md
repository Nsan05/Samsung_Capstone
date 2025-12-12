VisionChef: Smart Fridge Assistant
<div align="center"> <img src="./images/main.jpg" alt="VisionChef Main Interface" width="800"/> <p><em>Main application interface showing detected ingredients and recipe suggestions</em></p> </div>
VisionChef is an intelligent web application that helps you reduce food waste and cook creative meals. It uses AI object detection (YOLOv8) to identify ingredients in your fridge from a photo and suggests recipes based on what you have (via Spoonacular API).

The UI is designed with a premium Samsung One UI aesthetic, featuring clean lines, large squircles, and intuitive interactions.

✨ Features
🤖 AI Ingredient Detection: Automatically identifies food items in uploaded images using a fine-tuned YOLOv8 model.

🔍 Smart Recipe Search: Suggests recipes based on detected ingredients, prioritizing what you already have.

📖 Detailed Recipe View: View full instructions, missing ingredients, and cook times in a beautiful modal.

🎨 Samsung One UI Design: Modern, responsive interface with Dark Mode support.

🧠 Custom Training: Includes scripts to merge datasets and fine-tune the model on specific ingredients.

📸 Visual Walkthrough
🍽️ Recipe Discovery Interface
<div align="center"> <img src="./images/main.jpg" alt="Recipe List View" width="600"/> <p><em>Browse recipes with ingredient detection results and cooking metrics</em></p> </div>
📋 Detailed Recipe View
<div align="center"> <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;"> <div> <img src="./images/description.jpg" alt="Recipe Description" width="300"/> <p><em>Recipe details with nutrition information</em></p> </div> <div> <img src="./images/descriptionItem.jpg" alt="Recipe Instructions" width="300"/> <p><em>Recipe instructions and required ingredients</em></p> </div> </div> </div>
📊 Key Screens
Feature	Screenshot	Description
Main Dashboard	<img src="./images/main.jpg" width="250">	Shows detected ingredients and recipe suggestions
Recipe Details	<img src="./images/description.jpg" width="250">	Displays nutrition info, cooking time, and ratings
Ingredients List	<img src="./images/descriptionItem.jpg" width="250">	Shows required ingredients with checkboxes
🔄 How It Works
graph TD
    A[📸 Upload Fridge Photo] --> B[🤖 AI Detection<br/>YOLOv8]
    B --> C[📋 Extract Ingredients]
    C --> D[🔍 Query Spoonacular API]
    D --> E[🍳 Display Recipes]
    E --> F[📱 Samsung One UI Interface]
    F --> G[✅ User Selects Recipe]
    G --> H[👨‍🍳 Cook & Enjoy!]
📋 Prerequisites
Before running the project, ensure you have the following installed:

Requirement	Version	Purpose
Python	3.8+	Backend API & AI model
Node.js	16+	Frontend React application
npm	Latest	Package management
Git	Latest	Version control
🔑 API Keys
You will need API keys for the following services:

Service	Purpose	Get Key
Spoonacular API	Fetching recipes	Get Key
Roboflow API	Training datasets (optional)	Get Key
🚀 Installation
1. Clone the Repository
bash
git clone https://github.com/Start-Catch-Up/VisionChef.git
cd VisionChef
2. Set Up Images Directory
Ensure your images are in the images folder:

bash
# Verify images are in the correct location
ls images/
# Should show: main.jpg, description.jpg, descriptionItem.jpg
3. Backend Setup
bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Configure environment variables:

bash
# Copy example environment file
cp .env.example .env
Edit .env file:

env
SPOONACULAR_API_KEY=your_actual_key_here
ROBOFLOW_API_KEY=your_actual_key_here
4. Model Weights (Crucial Step)
<div align="center"> <img src="./images/description.jpg" width="400" alt="AI Model in Action"/> <p><em>AI-powered ingredient detection requires trained weights</em></p> </div>
Download weights from: Google Drive

Create directory:

bash
mkdir -p backend/runs/detect/train/weights
Place files:

text
backend/runs/detect/train/weights/
├── best.pt    # Primary model weights
└── last.pt    # Backup weights
5. Frontend Setup
bash
cd ../frontend
npm install
🖥️ Running the Application
Run both servers in separate terminals:

Terminal 1 - Backend
bash
cd backend
python app.py
# Server: http://localhost:8000
Terminal 2 - Frontend
bash
cd frontend
npm run dev
# Server: http://localhost:5173
<div align="center"> <img src="./images/main.jpg" width="500" alt="Running Application"/> <p><em>Application running with both backend and frontend servers</em></p> </div>
🧪 Model Training (Optional)
To train your own model:

bash
cd backend
python train.py
This script:

📥 Downloads datasets from Roboflow

🔄 Merges "Food in Fridge" and "Food Ingredients" datasets

🏋️‍♂️ Trains YOLOv8 model

💾 Saves results to runs/detect/train/

📁 Project Structure
text
VisionChef/
├── 📁 images/                    # Application screenshots
│   ├── main.jpg                 # Main interface
│   ├── description.jpg          # Recipe details
│   └── descriptionItem.jpg      # Ingredients list
├── 📁 backend/
│   ├── app.py                   # FastAPI application
│   ├── train.py                 # Model training
│   ├── evaluate.py              # Model evaluation
│   ├── services.py              # YOLO & Spoonacular logic
│   ├── requirements.txt         # Python dependencies
│   └── 📁 runs/                 # Trained model weights
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── App.tsx              # React application
│   │   └── index.css            # Tailwind styles
│   ├── tailwind.config.js       # Tailwind config
│   └── package.json             # Node.js dependencies
└── README.md                    # This file
🎯 User Flow
<div align="center"> <img src="./images/main.jpg" alt="User Flow Diagram" width="400" style="border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border: 2px solid #4CAF50;"/> </div>
📸 Capture - Take a photo of your fridge

🤖 Detect - AI identifies ingredients

🍳 Browse - View matching recipes

👨‍🍳 Cook - Follow instructions with confidence

🌱 Reduce Waste - Use what you have efficiently

📝 Example Usage
python
# Example of how VisionChef processes images
from services import detect_ingredients, get_recipes

# 1. User uploads image
image = "fridge_photo.jpg"

# 2. AI detects ingredients
ingredients = detect_ingredients(image)
# Returns: ["tomatoes", "onion", "eggs", "bacon"]

# 3. Find matching recipes
recipes = get_recipes(ingredients)
# Returns recipes that use detected items
🛠️ Troubleshooting
Issue	Solution
Images not loading	Ensure images are in ./images/ folder
Model weights missing	Download from Google Drive link above
API errors	Check .env file for correct keys
Port conflicts	Change ports in app.py (backend) or vite.config.js (frontend)
📄 License
MIT License - see LICENSE file for details.

<div align="center">
🚀 Ready to Reduce Food Waste?
bash
# Start your culinary AI journey
git clone https://github.com/Start-Catch-Up/VisionChef.git
cd VisionChef
# Follow installation steps above
Made with ❤️ by the VisionChef Team
Smart cooking for a sustainable future

<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;"> <img src="./images/descriptionItem.jpg" width="150" alt="Ingredients"> <img src="./images/description.jpg" width="150" alt="Recipe"> <img src="./images/main.jpg" width="150" alt="Dashboard"> </div></div>
