# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:01:03 2023

@author: SanthosRaj
"""
def execute():
    
    from langchain.llms import OpenAI;
    from langchain.document_loaders import YoutubeLoader;
    from langchain.chains.summarize import load_summarize_chain
    import os 
    
    
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]="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"
    
    
    loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=6Ub7Z1AGIuk", add_video_info=True)
    result = loader.load()
    
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    llm = OpenAI(temperature =0,openai_api_key  = OPENAI_API_KEY)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=0)
    texts = text_splitter.split_documents(result)
    
    chain = load_summarize_chain(llm, chain_type="map_reduce" , verbose=True)
    
    chain.run(texts)

execute()