@echo off
mkdir python
pip install -r requirements.txt -t python
powershell Compress-Archive -Path python -DestinationPath lambda-layer.zip -Force
rmdir /s /q python
echo Layer created: lambda-layer.zip