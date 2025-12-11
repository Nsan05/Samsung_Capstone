# Recipe Display Issue - Debug Guide

## Problem Identified ❌
The backend detects ingredients correctly (YOLO works ✓), but **recipes are not showing** because the **Spoonacular API is returning a 401 Unauthorized error**.

### Root Cause
Your `SPOONACULAR_API_KEY` in `.env` is either:
- **Expired** - API key has been revoked or subscription ended
- **Invalid** - API key is malformed or incorrect
- **Rate limited** - Too many requests used up

### Evidence
From backend logs:
```
image 1/1 ... 2 bottles, 6 apples, 1 orange, 1 broccoli ✓ (Detection works!)
Error calling Spoonacular API: 401 Client Error: Unauthorized ❌ (API key issue)
```

---

## Solution Steps

### Step 1: Get a New Spoonacular API Key
1. Go to https://spoonacular.com/food-api
2. Sign up for a free account (if you don't have one)
3. Copy your API key

### Step 2: Update `.env` File
Edit `backend/.env` and replace the old key:
```env
SPOONACULAR_API_KEY=YOUR_NEW_API_KEY_HERE
ROBOFLOW_API_KEY=rf_dnop8hx70dO4FyXsw98WPew476r1
```

### Step 3: Restart Backend
Kill the current backend process and restart:
```bash
cd backend
python app.py
```

### Step 4: Test
Upload an image through the frontend at http://localhost:5173/

---

## What's Been Improved ✨

### Backend Error Handling
- ✓ Detects when API keys are missing or invalid
- ✓ Returns ingredients even if recipe fetching fails
- ✓ Provides clear error messages in console logs
- ✓ No longer crashes on Spoonacular API errors

### Logging
You'll now see clear messages:
```
✓ Detected ingredients: ['apple', 'bottle', 'broccoli', 'orange']
📍 Fetching recipes for ingredients: ['apple', 'bottle', 'broccoli', 'orange']
✓ Successfully fetched 5 recipes for ingredients...
📊 Response: 4 ingredients, 5 recipes
```

Or if there's an error:
```
❌ Spoonacular API Error: 401 - Invalid API key
   Make sure your API key is valid and has available requests.
```

---

## Testing Without a Real API Key

If you want to test the frontend UI with mock data while you get a new key:

**Option A: Use Mock Recipes (Temporary)**
Edit `backend/services.py` and return dummy recipes:
```python
def find_recipes_by_ingredients(self, ingredients: List[str], number: int = 5) -> List[Dict]:
    # TEMPORARY: Return mock recipes for testing
    return [
        {
            "id": 1,
            "title": "Simple Salad",
            "image": "https://via.placeholder.com/300",
            "usedIngredientCount": 3,
            "missedIngredientCount": 0,
            "usedIngredients": [{"name": "apple"}, {"name": "broccoli"}],
            "missedIngredients": [],
            "sourceUrl": "https://example.com",
            "readyInMinutes": 15,
            "summary": "A simple salad recipe"
        }
    ]
```

**Option B: Get a Free Spoonacular API Key (Recommended)**
- Free tier: 150 requests/day
- Sign up at: https://spoonacular.com/food-api
- Takes 1 minute

---

## Health Check Endpoint

To verify API configuration anytime:
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "spoonacular_key_loaded": true,
  "roboflow_key_loaded": true
}
```

If you see `false` for any key, check that it's in `.env` and spelled correctly.
