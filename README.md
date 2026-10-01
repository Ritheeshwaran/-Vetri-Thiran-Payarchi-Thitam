# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI learning assistant based on the supplied project document. It provides:

- Question answering
- Beginner-friendly concept explanation
- Three-question MCQ generation
- Educational text summarization
- Beginner-to-advanced learning recommendations

The original document describes FastAPI, HTML/CSS, Gemini 1.5 Pro, and LaMini-Flan-T5-783M. The implementation keeps the same module structure and API routes, but uses Google's current `google-genai` Python SDK and a configurable current Gemini model by default. This avoids depending on the older Gemini 1.5 API generation.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

## 1. Prerequisites

- Python 3.10+
- VS Code
- A Google AI Studio API key

## 2. Open the project in VS Code

Open the `EduGenie` folder in VS Code.

Then open:

**Terminal → New Terminal**

## 3. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Gemini

Copy `.env.example` to `.env`.

Windows:

```powershell
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Open `.env` and replace:

```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```

with your real key.

Do not commit `.env` to Git. It is already ignored by `.gitignore`.

## 6. Run the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## 7. Test the application

Run automated tests:

```bash
pip install pytest
pytest -q
```

The tests mock AI calls, so they do not consume Gemini API quota.

Then manually test:

### Q&A
Choose **Ask a Question** and enter:

```text
Which is the largest ocean?
```

### Explanation
Choose **Explain a Topic** and enter:

```text
Binary search
```

### Quiz
Choose **Generate a Quiz** and enter:

```text
The Pythagorean theorem states that for a right triangle, the square of
the hypotenuse is equal to the sum of the squares of the other two sides.
```

### Summary
Paste a long educational paragraph.

### Learning path
Enter:

```text
SQL
```

## 8. Optional local LaMini explanation model

The supplied project document describes `MBZUAI/LaMini-Flan-T5-783M` as the local explanation model.

To use it:

```bash
pip install -r requirements-local.txt
```

Then change `.env`:

```env
EXPLANATION_PROVIDER=local
```

Restart Uvicorn.

The first local explanation request downloads the model from Hugging Face. This can require substantial disk space and RAM. Other EduGenie functions continue to use Gemini.

To switch back:

```env
EXPLANATION_PROVIDER=gemini
```

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/health` | Application status |
| GET | `/qa?question=...` | Q&A |
| POST | `/explain` | Explain a topic |
| POST | `/quiz` | Generate 3 MCQs |
| POST | `/summarize` | Summarize educational text |
| GET | `/learn/recommendations?topic=...` | Learning path |

FastAPI also provides interactive API testing at `/docs`.

## Common problems

### `GEMINI_API_KEY is not configured`

Check that `.env` exists in the project root and contains:

```env
GEMINI_API_KEY=...
```

Restart Uvicorn after changing `.env`.

### `ModuleNotFoundError`

Make sure the virtual environment is activated and run:

```bash
pip install -r requirements.txt
```

### Port 8000 is already in use

Use another port:

```bash
uvicorn main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

### Gemini quota/API error

Check the API key, model name, quota, and Google AI Studio project configuration. The application will return the upstream error through the API response instead of silently hiding it.

## Security notes

- Never put the Gemini API key in `static/app.js` or HTML.
- Keep the key only in the server-side `.env`.
- Do not commit `.env`.
- For production deployment, add authentication, rate limiting, request logging, HTTPS, and stricter CORS rules.

## Future extensions

The supplied document proposes voice interaction, multilingual support, mobile/offline access, progress dashboards, gamification, adaptive learning, group study, teacher/parent dashboards, LMS integration, and image/PDF understanding. Those are intentionally not required for this first complete implementation.
