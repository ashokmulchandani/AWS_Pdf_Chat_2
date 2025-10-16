# Insurance Underwriting Document Processor

AWS Lambda function that processes insurance application PDFs using Textract and Bedrock to generate structured underwriting summaries.

## Overview

This solution extracts text from insurance PDFs, analyzes the content using AI, and generates comprehensive underwriting reports in both JSON and DOCX formats.

## Architecture

**PDF → Textract → Bedrock → Structured Output (JSON + DOCX)**

## Files

- `textract_ashok.py` - Main Lambda function
- `Nobleoak_json.txt` - JSON template with 17 underwriting sections
- `requirements.txt` - Python dependencies
- `build_layer.bat` - Creates Lambda layer
- `package_lambda.bat` - Packages Lambda function

## Quick Start

### 1. Build Lambda Layer
```cmd
build_layer.bat
```

### 2. Package Lambda Function
```cmd
package_lambda.bat
```

### 3. Deploy to AWS
- Upload `lambda-layer.zip` as Lambda layer
- Upload `lambda-function.zip` as Lambda function
- Set environment variables:
  - `BUCKET_NAME=python-docx-bucket1`
  - `PREFIX=output`

### 4. Configure IAM Permissions
Grant Lambda access to:
- S3 (GetObject, PutObject)
- Textract (GetDocumentTextDetection)
- Bedrock (InvokeModel)
- CloudWatch Logs

## S3 Bucket Structure
```
python-docx-bucket1/
├── input/           # Upload PDFs here
├── output/          # Generated JSON and DOCX files
├── processed_pdfs/  # Processed PDFs moved here automatically
└── templates/       # Nobleoak_json.txt template
```

## Output Format

### JSON Structure
- **applicant**: Name, DOB, state
- **underwritingSections**: 17 detailed sections including:
  - Applicant details, Applied for cover, Medical history
  - Lifestyle factors, Income details, Travel plans
  - Recreation activities, Family history, etc.
- **summary**: Categorized disclosure summary and red flags

### DOCX Report
- Formatted underwriting summary document
- Organized sections with bullet points
- Professional layout matching sample format

## Usage

1. Upload PDF to `s3://python-docx-bucket1/input/`
2. Textract processes the document
3. Lambda function generates structured output
4. Results saved to `s3://python-docx-bucket1/output/`

## Dependencies

- `python-docx==0.8.11` (for DOCX generation)
- `boto3` (included in Lambda runtime)

## AI Model

Uses **Claude 3 Sonnet** via AWS Bedrock for intelligent text analysis and structuring.