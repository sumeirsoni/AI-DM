# D&D 5e Data Viewer with Text-to-Speech

A Next.js web application for browsing D&D 5e data with text-to-speech functionality powered by ElevenLabs.

## Setup

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Set up environment variables:**

   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your ElevenLabs API key:
     ```
     ELEVENLABS_API_KEY=your_api_key_here
     ```

3. **Ensure D&D data is available:**
   - Make sure the `dnd_raw/` folder contains the JSON data files
   - If not, run `harvest_dnd5e.py` first to download the data

## Running the Application

1. **Start the development server:**

   ```bash
   npm run dev
   ```

2. **Open your browser:**
   - Navigate to `http://localhost:3000`
   - The app will load and display D&D 5e data

## Features

- Browse D&D 5e races, classes, spells, and monsters
- Click on any item to see detailed information
- Click the "🔊 Speak" button to hear the item name spoken using ElevenLabs TTS
- The text-to-speech will say the item name in uppercase with an exclamation mark (e.g., "FIREBALL!")

## Python Server (Alternative)

If you prefer to use the Python server instead:

1. **Install Python dependencies:**

   ```bash
   pip install python-dotenv requests
   ```

2. **Set up environment variable:**

   - Make sure `.env` file contains `ELEVENLABS_API_KEY`

3. **Run the server:**

   ```bash
   python server.py
   ```

4. **Open your browser to `http://localhost:8000`**
