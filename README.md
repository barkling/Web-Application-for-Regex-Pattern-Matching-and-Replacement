# Text Pattern Matcher

A web application that allows users to upload CSV/Excel files, describe text patterns in natural language, and use LLM-generated regular expressions to find and replace text patterns.

## Features

- Upload and view CSV/Excel files
- Convert natural language descriptions to regular expressions using LLM
- Apply text replacements using generated regex patterns
- View original and processed data in a table format

## Prerequisites

- Python 3.8+
- Node.js 14+
- OpenAI API key

## Setup

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the backend server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload a CSV or Excel file
3. Enter a natural language description of the text pattern you want to match
4. Click "Generate Regex" to get the regular expression
5. Enter the replacement text and select the column to apply the changes
6. Click "Apply Replacement" to process the data
7. View the processed data in the table below

After entering the api key into the correct place, the video below will show you how to use it. And if you meet some probelms, you can trace the debug log in the terminal.


https://github.com/user-attachments/assets/85417866-a0a0-4869-bc6b-003d612e905d



## API Endpoints

- `POST /api/files/` - Upload a file
- `POST /api/files/{id}/generate_regex/` - Generate regex from natural language
- `POST /api/files/{id}/replace_text/` - Apply regex replacement

## Technologies Used

- Backend: Django, Django REST Framework
- Frontend: React, Ant Design
- Data Processing: Pandas
- LLM Integration: OpenAI API 
