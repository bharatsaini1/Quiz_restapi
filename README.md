# Quiz Generation API

## 📌 Overview
The **Quiz Generation API** is an AI-powered system that generates **multiple-choice quizzes** based on the content of a PDF file uploaded by the user. It offers three difficulty levels: **Easy, Medium, and Hard** to ensure flexibility in learning.

## 🚀 Features
- **PDF-Based Quiz Generation**: Upload a PDF file, and the AI extracts key concepts to create quizzes.
- **Three Difficulty Levels**: Choose between Easy, Medium, and Hard quizzes.
- **AI-Powered Question Creation**: Uses **LangChain** and an LLM to generate relevant MCQs.
- **REST API Integration**: Built with **Django Rest Framework** for seamless integration.
- **Structured JSON Output**: The generated quiz is returned in JSON format for easy use.

## 🛠 Tech Stack
- **Backend**: Django Rest Framework (DRF)
- **AI Framework**: LangChain
- **PDF Processing**: PyMuPDF (fitz)
- **Database**: Mysql (or SQLite for testing)
- **Deployment**: Pythonanywhere

## 🔧 Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/bharatsaini1/Quiz_restapi.git
   cd Quiz_restapi
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## 📤 API Endpoints
### 1️⃣ Upload PDF & Generate Quiz
**Endpoint:**
```
POST /api/generate-quiz/
```
**Payload:**
```json
{
  "file": "<PDF File>",
  "difficulty": "easy | medium | hard"
}
```
**Response:**
```json
{
  "questions": [
    {
      "question": "What is AI?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A"
    }
  ]
}
```

## 📌 Contribution
Feel free to fork the repo, create a pull request, and contribute!

## 🔗 GitHub Repository
[Quiz Generation API](https://github.com/bharatsaini1/Quiz_restapi)

## 📝 License
This project is licensed under the **MIT License**.

