@echo off
echo Creating Lambda deployment package...
powershell Compress-Archive -Path textract_ashok.py,Nobleoak_json.txt -DestinationPath lambda-function.zip -Force
echo Lambda package created: lambda-function.zip