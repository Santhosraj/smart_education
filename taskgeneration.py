# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 14:00:51 2023

@author: SanthosRaj
"""
def execute():
    
    import os
    import sys
    import pyttsx3
    import openai
    from langchain.chains import ConversationalRetrievalChain, RetrievalQA
    from langchain.chat_models import ChatOpenAI
    from langchain.document_loaders import DirectoryLoader, TextLoader
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.indexes import VectorstoreIndexCreator
    from langchain.indexes.vectorstore import VectorStoreIndexWrapper
    from langchain.llms import OpenAI
    from langchain.vectorstores import Chroma
    
    
    os.environ["OPENAI_API_KEY"] = ""
    

    PERSIST = False
    
    query = None
    if len(sys.argv) > 1:
      query = sys.argv[1]
    
    if PERSIST and os.path.exists("persist"):
      print("Reusing index...\n")
      vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
      index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
      loader = TextLoader("D:/Santhosraj Machine learning/spyder/Langchain/task.txt") # Use this line if you only need data.txt
      #loader = DirectoryLoader
      if PERSIST:
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
      else:
        index = VectorstoreIndexCreator().from_loaders([loader])
    
    chain = ConversationalRetrievalChain.from_llm(
      llm=ChatOpenAI(model="gpt-3.5-turbo"),
      retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    
    import speech_recognition as sr
    
   
    recognizer = sr.Recognizer()
    
    # Open the microphone and start listening for speech
    with sr.Microphone() as source:
        pyttsx3.speak("What do you want to know?...")
        print("What do you want to know?...")
        audio = recognizer.listen(source)
    
    try:
        # Recognize the speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
       
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    
    
    chat_history = []
    while True:
      if not query:
        query = text
      if query in ['quit', 'q', 'exit']:
        sys.exit()
      result = chain({"question": query, "chat_history": chat_history})
      print(result['answer'])
      pyttsx3.speak(result['answer'])
      chat_history.append((query, result['answer']))
      query = None

    
execute()    
