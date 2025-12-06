import { useState, useRef } from 'react';
import axios from 'axios';

// Interfaces
interface BBox {
  label: string;
  bbox: [number, number, number, number]; // [x1, y1, x2, y2]
  confidence: number;
}

interface Recipe {
  id: number;
  title: string;
  image: string;
  usedIngredientCount: number;
  missedIngredientCount: number;
  usedIngredients: { name: string }[];
  missedIngredients: { name: string }[];
  sourceUrl?: string;
  readyInMinutes?: number;
}

interface AnalysisResult {
  detected_ingredients: string[];
  raw_detections: BBox[];
  recipes: Recipe[];
  image_id: string;
}

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  
  // Dark mode state
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Toggle dark mode class on html element
  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    if (!isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };
  
  // For overlay scaling
  const imgRef = useRef<HTMLImageElement>(null);
  const [imgSize, setImgSize] = useState({ width: 0, height: 0 });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setAnalysisResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedImage) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      // Assuming backend is on port 8000
      const response = await axios.post('http://localhost:8000/analyze_fridge', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAnalysisResult(response.data);
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Failed to analyze image. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  // Sort recipes: most used ingredients first
  const sortedRecipes = analysisResult?.recipes 
    ? [...analysisResult.recipes].sort((a, b) => b.usedIngredientCount - a.usedIngredientCount)
    : [];

  const handleImageLoad = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const { width, height } = e.currentTarget;
    setImgSize({ width, height });
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${isDarkMode ? 'dark:bg-gray-900 dark:text-gray-100' : 'bg-gray-50 text-gray-900'} p-8`}>
      <header className="mb-12 flex justify-between items-center max-w-6xl mx-auto">
        <div className="text-center w-full relative">
            <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-green-500 to-teal-600 mb-4 cursor-pointer hover:bg-gradient-to-l transition-all">
            VisionChef
            </h1>
            <p className={`text-xl ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Smart Fridge Assistant & Recipe Recommender</p>
            
            <button 
                onClick={toggleDarkMode}
                className="absolute top-0 right-0 p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                title="Toggle Dark Mode"
            >
                {isDarkMode ? '☀️' : '🌙'}
            </button>
        </div>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
        {/* Left Column: Upload & Visualization */}
        <section className="flex flex-col items-center gap-6">
          <div className={`w-full p-6 rounded-2xl shadow-xl border transition-colors ${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-100'}`}>
            <h2 className={`text-2xl font-bold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>1. Upload Fridge Photo</h2>
            
            <div className="flex items-center justify-center w-full">
                <label className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer transition-colors ${isDarkMode ? 'border-gray-600 bg-gray-700 hover:bg-gray-600' : 'border-gray-300 bg-gray-50 hover:bg-gray-100'}`}>
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <svg className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                        <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                        <p className="text-xs text-gray-500">SVG, PNG, JPG (MAX. 800x400px)</p>
                    </div>
                    <input type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                </label>
            </div> 

            {previewUrl && (
              <div className="mt-6 relative w-full overflow-hidden rounded-lg border border-gray-200">
                <img 
                  src={previewUrl} 
                  alt="Fridge Preview" 
                  className="w-full h-auto block"
                  ref={imgRef}
                  onLoad={handleImageLoad}
                />
                
                {/* Bounding Boxes Overlay */}
                {analysisResult && analysisResult.raw_detections.map((det, idx) => {
                  // Scale coordinates if displayed image size differs from original
                  // YOLO returns [x1, y1, x2, y2]
                  // IF YOLO ran on 640x640 resize, we need to know that.
                  // Wait, YOLOv8 returns coordinates in original image pixels by default unless configured otherwise.
                  // BUT, we need to display them on the scaled image in the browser.
                  
                  // For simplicity in this v1, let's assume the Display Image intrinsic size matches the analysis, 
                  // OR we rely on percentage if we knew original size.
                  // A robust way: The backend sends coordinates. We need to map them to the *current displayed size*.
                  // However, we don't know the original image size easily unless backend returns it.
                  // Let's assume the coordinates are correct for the full resolution image, 
                  // and we just use absolute positioning based on the ratio.
                  
                  // We need 'naturalWidth' and 'naturalHeight' from the image ref.
                  const natW = imgRef.current?.naturalWidth || 1;
                  const natH = imgRef.current?.naturalHeight || 1;
                  
                  // Display Size
                  const dispW = imgSize.width;
                  const dispH = imgSize.height;

                  const [x1, y1, x2, y2] = det.bbox;
                  
                  const style = {
                    left: `${(x1 / natW) * 100}%`,
                    top: `${(y1 / natH) * 100}%`,
                    width: `${((x2 - x1) / natW) * 100}%`,
                    height: `${((y2 - y1) / natH) * 100}%`,
                  };

                  return (
                    <div 
                      key={idx}
                      className="absolute border-2 border-red-500 bg-red-500/20 hover:bg-red-500/30 transition-colors z-10 group"
                      style={style}
                    >
                      <span className="absolute -top-6 left-0 bg-red-500 text-white text-xs px-1 py-0.5 rounded shadow-sm opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                        {det.label} ({Math.round(det.confidence * 100)}%)
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
            
            <div className="mt-6 text-center">
                <button 
                  onClick={handleUpload} 
                  disabled={!selectedImage || loading}
                  className={`px-8 py-3 rounded-full font-bold text-white shadow-lg transition-all transform hover:scale-105 ${
                    !selectedImage || loading 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:shadow-indigo-500/50'
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Analyzing...
                    </span>
                  ) : "Analyze Fridge"}
                </button>
            </div>
          </div>
        </section>

        {/* Right Column: Results */}
        <section className="flex flex-col gap-6">
          <div className={`p-6 rounded-2xl shadow-xl border transition-colors min-h-[500px] ${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-100'}`}>
            <h2 className={`text-2xl font-bold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>Recommmended Recipes</h2>
            
            {!analysisResult && !loading && (
              <div className="h-full flex flex-col items-center justify-center text-gray-400">
                <span className="text-6xl mb-4">🍳</span>
                <p>Upload a photo to get started!</p>
              </div>
            )}

            {loading && (
               <div className="h-full flex flex-col items-center justify-center text-gray-400 animate-pulse">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
               </div>
            )}
            
            {analysisResult && (
              <div className="space-y-4 max-h-[700px] overflow-y-auto pr-2 custom-scrollbar">
                {/* Ingredients Detected Tag Cloud */}
                <div className="flex flex-wrap gap-2 mb-6">
                  {analysisResult.detected_ingredients.map((ing, i) => (
                    <span key={i} className={`px-3 py-1 rounded-full text-sm font-medium border ${isDarkMode ? 'bg-green-900/50 text-green-300 border-green-800' : 'bg-green-100 text-green-700 border-green-200'}`}>
                      ✅ {ing}
                    </span>
                  ))}
                </div>

                {sortedRecipes.length === 0 ? (
                    <p className="text-center text-gray-500">No recipes found matching these ingredients.</p>
                ) : (
                    sortedRecipes.map((recipe) => (
                      <div key={recipe.id} className={`flex gap-4 p-4 rounded-xl border hover:shadow-md transition-all ${isDarkMode ? 'bg-gray-700/50 border-gray-600 hover:bg-gray-700' : 'bg-gray-50/50 border-gray-100'}`}>
                        <img 
                          src={recipe.image} 
                          alt={recipe.title} 
                          className="w-24 h-24 object-cover rounded-lg shadow-sm"
                        />
                        <div className="flex-1 flex flex-col justify-between">
                          <div>
                              <h3 className={`font-bold text-lg leading-tight mb-2 ${isDarkMode ? 'text-gray-100' : 'text-gray-800'}`}>{recipe.title}</h3>
                              <div className="flex gap-4 text-sm mb-2">
                                <span className="text-green-500 font-medium">
                                  {recipe.usedIngredientCount} Used
                                </span>
                                <span className="text-red-500 font-medium">
                                  {recipe.missedIngredientCount} Missing
                                </span>
                              </div>
                          </div>
                          <div className="flex justify-between items-end">
                              <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                                 Missing: {recipe.missedIngredients.map(i => i.name).slice(0, 3).join(", ")}
                                 {recipe.missedIngredients.length > 3 && "..."}
                              </p>
                              {recipe.sourceUrl && (
                                <a 
                                    href={recipe.sourceUrl} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-sm px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
                                >
                                    View Recipe →
                                </a>
                              )}
                          </div>
                        </div>
                      </div>
                    ))
                )}
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
