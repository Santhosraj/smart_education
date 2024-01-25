# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 14:12:31 2023

@author: SanthosRaj
"""
def execute():
    import os
    os.environ["OPENAI_API_KEY"]=''
    
    
    import tiktoken
    
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    num_tokens_from_string("tiktoken is great!", "cl100k_base")
    
    import gradio as gr
    from langchain import OpenAI, PromptTemplate
    from langchain.chains.summarize import load_summarize_chain
    from langchain.document_loaders import PyPDFLoader
    
    llm = OpenAI(temperature=0)
         
    def summarize_pdf(pdf_file_path):
        loader = PyPDFLoader(pdf_file_path)
        docs = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)   
        return summary
    
    summarize = summarize_pdf("D:/Santhosraj Machine learning/spyder/Langchain/book_pdfs/The-Field-Guide-to-Data-Science.pdf")
    
    print(summarize)
