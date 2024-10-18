import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

# Define the image generation model
imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

def generate_image_from_prompt(prompt):
    """Generates an image based on the provided prompt."""
    try:
        result = imagen.generate_images(
            prompt=prompt,
            number_of_images=1,
            safety_filter_level="block_only_high",
            person_generation="allow_adult",
            aspect_ratio="3:4",
            negative_prompt="Outside",
        )
        # Return the PIL image
        return result.images[0]._pil_image

    except Exception as e:
        raise Exception(f"Error generating image: {str(e)}")
