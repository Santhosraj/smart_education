
def execute():
    # Import the Metaphor class from the library
    
    
    from metaphor_python import Metaphor
    import speech_recognition as sr
    
    # Initialize an instance of the Metaphor class with your API key
    metaphor = Metaphor("75250cd7-208e-4bde-98d5-91bc0ea66b70")
    
    # Function to get user speech input
    def get_speech_input():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please speak your search query...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)
    
        try:
            # Use Google Web Speech API to recognize speech
            query = recognizer.recognize_google(audio)
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand your speech.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
    
    # Get user's spoken query
    user_query = get_speech_input()
    
    if user_query:
        # Use the user's spoken query as the search query
        response = metaphor.search(
            user_query,          # User's spoken query
            num_results=10,     # Number of results you want to retrieve
            use_autoprompt=True  # Enable automatic generation of prompts
        )
    
        # The 'response' variable now contains the search results
        # You can process and display these results as needed
        # For example, you can print the titles and URLs of the search results:
        for result in response.results:  # Use dot notation to access 'results'
            print(f"Title: {result.title}")
            print(f"URL: {result.url}")
            print()
    else:
        print("No query detected.")
execute()