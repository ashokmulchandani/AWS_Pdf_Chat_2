import boto3
import streamlit as st
import os
import uuid

# s3_client
s3_client = boto3.client("s3", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Bedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain_community.chat_models import BedrockChat

# Prompt and chain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Text_splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Pdf_loader
from langchain_community.document_loaders import PyPDFLoader

# import FAISS
from langchain_community.vectorstores import FAISS

bedrock_client=boto3.client(service_name='bedrock-runtime', region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
bedrock_embeddings= BedrockEmbeddings(client=bedrock_client,model_id='amazon.titan-embed-text-v2:0')

folder_path="/tmp/"

def get_unique_id():
    return str(uuid.uuid4())

# load index

def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")  



def get_llm():
   llm=BedrockChat(model_id="anthropic.claude-3-haiku-20240307-v1:0", client=bedrock_client,
                   model_kwargs={'max_tokens': 512})
   
   return llm

# get_response()
def get_response(llm, vectorstore, question):
    ## create prompt / template
    prompt_template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    answer = qa({"query": question})
    return answer['result']

## main method

def main():
    st.header("This is Client Site for Chat with PDF demo using Bedrock, RAG etc")
    load_index()

    dir_list = os.listdir(folder_path)
    st.write(f"Files and Directories in {folder_path}")
    st.write(dir_list)
    ## create index
    faiss_index = FAISS.load_local(
        index_name="my_faiss",
        folder_path=folder_path,
        embeddings=bedrock_embeddings,
        allow_dangerous_deserialization=True
    )

    st.write("INDEX IS READY")
    question = st.text_input("Please ask your question")
    if st.button("Get Response"):
        with st.spinner("Querying..."):
            llm = get_llm()

            # get_response
            st.write(get_response(llm, faiss_index, question))
            st.success("Done")

if __name__ == "__main__":
    main()

    




