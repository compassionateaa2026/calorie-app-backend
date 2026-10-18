import os
from google import genai
from PIL import Image

client = genai.Client(api_key="")

def analyze_food(image_path):
    try:
        image = Image.open(image_path)
        prompt = "Analyze this food image and provide in English: 1. Dish name 2. Calories 3. Macronutrients (Protein, Carbs, Fats) 4. Notes"
        print("Analyzing image...")
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=[image, prompt]
        )
        print("\n--- Analysis Result ---")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    image_file = "Food.jpg"
    if os.path.exists(image_file):
        analyze_food(image_file)
    else:
        print(f"Image file '{image_file}' not found.")
	
	

