import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

# Define the upload directory
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the directory exists

class GenerateQuizView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            # Handle uploaded file
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the file to the uploads directory
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Extract question_count and difficulty from the request
            question_count = int(request.data.get('question_count', 5))
            difficulty = request.data.get('difficulty', 'medium')

            # Load and process the PDF
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            if not documents:
                return Response({"error": "Failed to load content from the PDF"}, status=status.HTTP_400_BAD_REQUEST)

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
            )
            chunks = text_splitter.split_documents(documents)
            pdf_content = "\n\n".join([chunk.page_content for chunk in chunks])

            # Create a prompt template
            template = """
            Please analyze the contents of the provided PDF (text below) and create a set of {question_count} multiple-choice questions (MCQs) 
            that reflect the key concepts and ideas from the material. Ensure the questions match the difficulty level: {difficulty}.

            Output the questions in the following JSON format:
            {{
              "questions": [
                {{
                  "question": "Question Text",
                  "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                  }},
                  "correct_answer": "Option A"
                }},
                ...
              ]
            }}

            PDF Content:
            {pdf_content}
            """
            prompt = PromptTemplate.from_template(template)
            llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyB0uUcJaq_ikKEoqHTcjQ64QfYxZXn5LLY")
            chain = prompt | llm

            # Generate quiz
            result = chain.invoke(input={
                "question_count": question_count,
                "difficulty": difficulty,
                "pdf_content": pdf_content
            })

            # Parse the response
            try:
                quiz_data = json.loads(result)
            except json.JSONDecodeError:
                return Response({"error": "Failed to parse the AI response as JSON"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Delete the uploaded file after processing
            if os.path.exists(file_path):
                os.remove(file_path)

            # Return the generated quiz
            return Response(quiz_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
