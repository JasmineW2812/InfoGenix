from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .serializers import UserSerializer, NoteSerializer, UploadedFileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, UploadedFile
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from openai import OpenAI
from django.conf import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


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
                {"role": "user", 
                 "content":
                      f"What can you tell me about this data? {date_cols} and {cat_summary} and {num_summary} and describe what the dashboard could look like for this data. Be direct use the file attached as a quick glance for any extra info that may help"
                }
            ]
            )

            print(completion.choices[0].message)

        except Exception as e:
            print(f"Error processing uploaded file: {e}")





