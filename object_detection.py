
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 16:11:44 2023

@author: SanthosRaj
"""


def execute():
    import wikipedia
    import cv2
    import cvlib as cv 
    from cvlib.object_detection import draw_bbox
    from gtts import gTTS
    from playsound import playsound
    import pyttsx3
    
    
    
    
    
    def speech(text):
        print(text)
        language = "en"
        output = gTTS(text=text, lang=language, slow=True)
        output.save("D:\Santhosraj Machine learning\spyder\Langchain\sounds\output.mp3")
        playsound("D:\Santhosraj Machine learning\spyder\Langchain\sounds\output.mp3")
    
    video = cv2.VideoCapture(0)
    labels = []
    
    while True:
        ret, frame = video.read()
        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf)
        cv2.imshow("ImageSummary", output_image)
    
        for item in label:
            if item =="cell phone" and item not in labels:
                labels.append(item)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break
    
    print(labels)
    for i in labels:
         summary = wikipedia.summary(i)
         print(summary)
    pyttsx3.speak(summary)
    
    
    '''
    i=0
    new_sentence = []
    for label in labels:
        if i ==0 :
            new_sentence.append(f"I found a {label}, and , ")
        else:
            new_sentence.append(f"a {label}")
        
        i+=1
        
    speech(" ".join(new_sentence))  
        '''

execute()  
 
