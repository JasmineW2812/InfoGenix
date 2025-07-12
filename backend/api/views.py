from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .serializers import UserSerializer, NoteSerializer, UploadedFileSerializer, GPTResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, UploadedFile, GPTResponse
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from openai import OpenAI
from django.conf import settings
import json
import os


client = OpenAI(api_key=settings.OPENAI_API_KEY)

with open(settings.PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
    instructions = f.read()


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)    

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.order_by('-uploaded_at')
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        uploaded_file_instance = serializer.save(user=user)
        uploaded_file = uploaded_file_instance.file

        try:
            df = pd.read_csv(uploaded_file)
            df = df.dropna()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            date_cols = df.select_dtypes(include=['datetime']).columns.tolist()

            num_summary = df[numeric_cols].describe().to_dict()
            cat_summary = {col: df[col].value_counts().to_dict() for col in categorical_cols}

            print("Numeric columns:", numeric_cols)
            print("Categorical columns:", categorical_cols)
            print("Date columns:", date_cols)
            print("Sample rows:")
            print(df.head(3))
            print("Summary of numeric columns:")
            print(num_summary)

            completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": f"What can you tell me about this data? {date_cols} and {cat_summary} and {num_summary}"},
                          
            ]
            )
            
            response_text = completion.choices[0].message.content
            print(completion.choices[0].message)
            base_filename = os.path.splitext(os.path.basename(uploaded_file.name))[0]
            response_filename = f"{base_filename}_gpt_response.json"
            response_path = os.path.join("gpt_outputs", response_filename)

            os.makedirs("gpt_outputs", exist_ok=True)

            with open(response_path, "w", encoding="utf-8") as outfile:
                json.dump({"response": response_text}, outfile, indent=2)

            GPTResponse.objects.create(file=uploaded_file_instance, response=response_text)


        except Exception as e:
            print(f"Error processing uploaded file: {e}")





