# Gemini Assistant

## Features
- **Generate Recipe from Image:** Upload an image, and the app will analyze it to provide a detailed recipe based on the contents.
- **Generate Images:** Create unique images from text prompts (coming soon).

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
   # windows
   .\venv\Scripts\activate

   # macos/linux
   source venv/bin/activate
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
