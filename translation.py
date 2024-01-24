# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 18:52:33 2023

@author: SanthosRaj
"""
def execute():
    from googletrans import Translator
    import cv2
    import pytesseract
    import pyttsx3
    import time
    import speech_recognition as sr
    
    def translate_text(text, target_language='en'):
        translator = Translator()
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    
    # Set the path to the Tesseract executable (change this path to match your installation)
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    
    # Initialize pyttsx3
    engine = pyttsx3.init()
    
    # Create a VideoCapture object to capture video from your webcam (0 is usually the default webcam)
    cap = cv2.VideoCapture(0)
    
    # Initialize the recognizer for speech input
    recognizer = sr.Recognizer()
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    
    while True:
        # Introduce a delay
        time.sleep(1)
    
        # Capture a frame from the webcam
        ret, frame = cap.read()
    
        if not ret:
            print("Error: Could not read a frame.")
            break
    
        # Perform OCR on the frame using Tesseract
        text = pytesseract.image_to_string(frame)
    
        # If text is detected, close the camera and ask for the target language using speech input
        if text is not None and text.strip():
            cap.release()
            cv2.destroyAllWindows()
            print("Recognized Text:")
            print(text)
    
            # Use speech recognition to capture the target language
            with sr.Microphone() as source:
                print("Please say the target language (e.g., 'German' or 'Deutsch'):")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
    
            try:
                target_language = recognizer.recognize_google(audio).lower()
                print(f"Target Language: {target_language}")
    
                # Translate the recognized text to the target language
                translated_text = translate_text(text, target_language)
                print(f"Translated text ({target_language}): {translated_text}")
    
                # Use pyttsx3 to convert and speak the translated text
                engine.say(translated_text)
                engine.runAndWait()
    
                break
    
            except sr.UnknownValueError:
                print("Sorry, I could not understand your speech.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        else:
             print("No text detected in the frame.")
        # Display the recognized text on the frame
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
        # Display the captured frame in an OpenCV window
        cv2.imshow("Webcam OCR", frame)
    
        # Press 'q' to close the camera and display the result
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the VideoCapture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

execute()