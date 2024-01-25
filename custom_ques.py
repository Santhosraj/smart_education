# -*- coding: utf'8 -*-

"""
Created on Fri Sep  1 17:10:36 2023

@author: SanthosRaj
"""
def execute():
    
    # PDF Loaders. If unstructured gives you a hard time, try PyPDFLoader
    from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader
    
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    import os
    
    loader = PyPDFLoader("D:/Santhosraj Machine learning/spyder/Langchain/book_pdfs/Solid-Edge-Fidget-Spinner-Steps-01.pdf")
    
    ## Other options for loaders 
    # loader = UnstructuredPDFLoader("../data/field-guide-to-data-science.pdf")
    # loader = OnlinePDFLoader("https://wolfpaulus.com/wp-content/uploads/2017/05/field-guide-to-data-science.pdf")
    
    data = loader.load()
    
   # print (f'You have {len(data)} document(s) in your data')
    #print (f'There are {len(data[30].page_content)} characters in your document')
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    
    #print (f'You have {len(data)} document(s) in your data')
    #print (f'There are {len(data[30].page_content)} characters in your document')
    
    print (f'Now you have {len(texts)} documents')
    
    from langchain.vectorstores import Chroma, Pinecone
    from langchain.embeddings.openai import OpenAIEmbeddings
    import pinecone
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]=""
    
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = ""
    PINECONE_API_ENV = os.environ["PINECONE_API_ENV"] = ""
    
    
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    pinecone.init(
        api_key=PINECONE_API_KEY, 
        environment=PINECONE_API_ENV  
    )
    index_name = "langchaintest" 
    
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
    
    query = "What are the steps to build Solid Edge Fidget Spinner?"
    docs = docsearch.similarity_search(query)
    print(docs[0].page_content[:])
    
    
    from langchain.llms import OpenAI
    from langchain.chains.question_answering import load_qa_chain
    
    llm = OpenAI(temperature=1.8, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    
    query = "Solid Edge Fidget Spinner Steps?"
    docs = docsearch.similarity_search(query)
    
    chain.run(input_documents=docs, question=query)
    
execute()
