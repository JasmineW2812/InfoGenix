from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .serializers import UserSerializer, NoteSerializer, UploadedFileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, UploadedFile
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

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

        except Exception as e:
            print(f"Error processing uploaded file: {e}")






        
