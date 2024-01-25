# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 09:56:38 2023

@author: SanthosRaj
"""
def execute():
    
    import langchain
    from langchain import PromptTemplate
    from langchain.chat_models import ChatOpenAI
    from langchain.llms import OpenAI
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.chains.summarize import load_summarize_chain
    from langchain.prompts import PromptTemplate
    import youtube_transcript_api,pytube
        
        #scrapping 
        
    import requests 
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
        
        #youtube data 
    from langchain.document_loaders import YoutubeLoader
        
        #env variables
    import os 
    from dotenv import load_dotenv
    load_dotenv()
        
        #pulling data from websites 
        
    def pull_website(url):
                try :
                    response = requests.get(url)
                except:
                    print("An error occured")
                
                
                #transferring response to beautifulsoup
                
                soup = BeautifulSoup(response.text,"html.parser")
                
                #getting the text
                
                text = soup.get_text()
                
                #reducing tokens and noise by converting html to markdown
                text = md(text)
                
                return text
            
        #storing website in a string
        
    website_data = ""
        
    urls =["https://www.electronics-tutorials.ws/dccircuits/dcp_4.html"]
    for url in urls :
            text = pull_website(url)
            
            website_data+=text
    print(website_data[:400])
        
        
        #getting data from youtube
        
    '''def get_video_transcript(url):
            loader  = YoutubeLoader.from_youtube_url(url,add_video_info=True)
            documents = loader.load()
            transcript = ' '.join([doc.page_content for doc in documents])
            return transcript
        
        
        #getting video urls 
    video_urls= ['https://www.youtube.com/watch?v=Bt6V7D5av9A']
        
    video_text = ""
        
    for video_url in video_urls:
            video_text = get_video_transcript(video_url)
            video_text+=video_text
    '''
    user_information = website_data 
        
        #text _splitter
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000,chunk_overlap=2000)
        
        #splitting information into different documents  
        
    docs = text_splitter.create_documents([user_information]) 
        
        #mapping prompt 
        
    map_prompt = """You are a helpful AI bot that aids a user in research.
        Below is information about a topic named {topic_name}.
        Information will include video transcripts, and blog posts about {topic_name}
        Your goal is to generate possible questions for an examination that can be asked under {topic_name}
        Use specifics from the research when possible
        
        % START OF INFORMATION ABOUT {topic_name}:
        {text}
        % END OF INFORMATION ABOUT {topic_name}:
        
        Please respond with list of a few questions based on the topics above
        
        YOUR RESPONSE:"""
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "topic_name"])
        
        
        
    combine_prompt = """
        You are a helpful AI bot that aids a user in research.
        You will be given a list of potential questions that we can ask {topic_name}.
        
        Please consolidate the questions and return a list
        
        % POSSIBLE EXAMINATION QUESTIONS
        {text}
        """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "topic_name"])
        
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]=""
        
    llm = ChatOpenAI(temperature = 2,model_name = 'gpt-3.5-turbo')
        
    chain = load_summarize_chain(llm,
                                     chain_type="map_reduce",
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template,
        #                              verbose=True
                                    )
        
        
    output = chain({"input_documents":docs,
                        "topic_name":"Kirchhoffs Circuit Law"
                        })
        
        
    print(output['output_text'])
execute()
