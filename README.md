# AI-Powered Adaptive Learning System

An AI-powered MCQ generator that creates questions based on SOLO Taxonomy levels, using Google's Gemini API.

## Features

- Generates adaptive multiple-choice questions
- Aligns questions with SOLO Taxonomy levels
- Caches responses for efficiency
- Provides both HTML and JSON API endpoints

## Prerequisites

- Python 3.9+ (I used Python 3.11)
- Google Gemini API key
- Docker (optional)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-adapt.git
cd ai-adapt
```

### 2. Setup the environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a .env file in the root directory:
```bash
    GEMINI_API_KEY=your_api_key_here
```

# Running the Application
### Development Mode
```bash
./venv/bin/python app.py
```

### Using Docker
```bash
docker build -t ai-adapt .
docker run -p 5000:5000 ai-adapt
```


# API Endpoints

## HTML Interface
```bash
GET /generate_mcq?topic=<topic>&solo_level=<level>
```

## JSON API
```bash
GET /api/generate_mcq?topic=<topic>&solo_level=<level>
```


## Available SOLO Levels
Unistructural

Multistructural

Relational

Extended Abstract


## Author
### - Sudhin Karki
