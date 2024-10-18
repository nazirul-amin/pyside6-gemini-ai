import os
import google.generativeai as genai
from dotenv import load_dotenv
import typing_extensions as typing

# Load environment variables from .env
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

# Define the recipe generation model
recipe_model = genai.GenerativeModel("gemini-1.5-flash")

# Define the TypedDict for the recipe response schema
class Recipe(typing.TypedDict):
    recipe_name: str
    ingredients: list[str]
    instructions: list[str]

def generate_recipe_from_prompt(image_path):
    """Generates a recipe based on the provided image."""
    try:
        myfile = genai.upload_file(image_path)
        print(f"{myfile=}")

        result = recipe_model.generate_content(
            [myfile, "\n\n", "Given this image:\n\nFirst, describe the image\n\nThen, detail the recipe to cook this food in JSON format. Include item names and quantities for the recipe, as well as step-by-step cooking instructions."],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=list[Recipe]
            )
        )

        return result.text
    except Exception as e:
        raise Exception(f"Error generating recipe: {str(e)}")
