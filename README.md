# Gemini Assistant

## Overview
The Gen AI App is a versatile tool designed to leverage the power of generative AI to simplify tasks such as recipe creation and image generation. With an intuitive user interface, users can easily generate recipes from images, create stunning visuals, and soon, translate text seamlessly. 

## Features
- **Generate Recipe from Image:** Upload an image, and the app will analyze it to provide a detailed recipe based on the contents.
- **Generate Images:** Create unique images from text prompts (coming soon).
- **Translate Text:** HTTP server for xunity autotranslator to translate unity game.

## Tech Stack
- PySide6
- Gemini API

## Run locally

To set up the Gen AI App locally, follow these steps:
1. **Create virtual env**
   ```bash
   python -m venv venv
   ```
2. **Activate the virtual env**
   ```bash
   .\venv\Scripts\activate
   ```
3. **Install necessary package:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Add api key in .env:**
   ```bash
   API_KEY=your_api_key_here
   ```
5. **Run the app:**
   ```bash
   python main.py
   ```
run ```deactivate``` to exit virtual env
