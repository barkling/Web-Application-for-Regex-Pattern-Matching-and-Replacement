from django.shortcuts import render
import pandas as pd
import json
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .models import FileUpload
import openai
from openai import OpenAI
import os
from django.conf import settings

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Create your views here.

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    
    def create(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        file_type = file.name.split('.')[-1].lower()
        if file_type not in ['csv', 'xlsx']:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
            
        file_upload = FileUpload.objects.create(
            file=file,
            original_filename=file.name,
            file_type=file_type
        )
        
        # Read and return the file contents
        file_path = default_storage.path(file_upload.file.name)
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        return Response({
            'id': file_upload.id,
            'data': df.to_dict(orient='records'),
            'columns': df.columns.tolist()
        })
    
    @action(detail=True, methods=['post'])
    def generate_regex(self, request, pk=None):
        file_upload = self.get_object()
        natural_language = request.data.get('description')
        
        if not natural_language:
            return Response({'error': 'No description provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Call OpenAI API to generate regex
            file_path = file_upload.file.path
            if file_upload.file_type == 'csv':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin1') as f:
                        file_content = f.read()
            elif file_upload.file_type == 'xlsx':
                df = pd.read_excel(file_path)
                file_content = df.head(10).to_csv(index=False)
            else:
                file_content = ''

            # user_content = f"{natural_language}\nThe file content is:\n{file_content}"
            user_content = f"I have a DataFrame called df, with some of the data being:\n{file_content}.\n Please help me generate the processing code for it based on the following description:\n{natural_language}"

            response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {"role": "developer", "content": "You are a regex expert. Convert the following natural language description into a Python regular expression pattern. Only return the regex pattern that can work with 're' library."},
                    # {"role": "developer",
                    #  "content":"You are a Python engineer who is skilled at processing tabular data. Only return the code of handling the data. Any operation directly affects the original table."},
                    {"role": "user", "content": user_content}
                ]
            )
            print("LLM response:", response)
            regex_pattern = response.output[0].content[0].text.strip()
            
            return Response({'regex': regex_pattern})
        except Exception as e:
            # return Response({'error': "Error generating regex about the llm"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            import traceback
            print("LLM调用异常:", e)
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def replace_text(self, request, pk=None):
        file_upload = self.get_object()
        regex_pattern = request.data.get('regex')
        replacement = request.data.get('replacement')
        column = request.data.get('column')
        
        if not all([regex_pattern, replacement, column]):
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            file_path = default_storage.path(file_upload.file.name)
            if file_upload.file_type == 'csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
                
            if column not in df.columns:
                return Response({'error': 'Invalid column name'}, status=status.HTTP_400_BAD_REQUEST)
                
            # 先转为字符串再替换
            df[column] = df[column].astype(str)
            df[column] = df[column].str.replace(regex_pattern, replacement, regex=True)
            print("df:", df)

            # Store processed data
            file_upload.processed_data = df.to_dict(orient='records')
            file_upload.save()
            
            return Response({
                'data': df.to_dict(orient='records'),
                'columns': df.columns.tolist()
            })
        except Exception as e:
            import traceback
            print("替换异常:", e)
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
