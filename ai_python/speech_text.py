import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')

def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            user_input = self.text
            print(f"User: {user_input}")
            return user_input.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            return None


def read_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Please speak the prompt:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        prompt = recognizer.recognize_google(audio)
        print("User:", prompt)
        return prompt
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio. Please try again.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

# def recognize_speech(timeout=5):
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source, duration=1)
#         try:
#             audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
#         except sr.WaitTimeoutError:
#             print("No speech detected. Listening timed out.")
#             return None

#     try:
#         user_input = recognizer.recognize_google(audio)
#         print(f"User: {user_input}")
#         return user_input.lower()
#     except sr.UnknownValueError:
#         print("Sorry, I didn't understand that.")
#         return None
#     except sr.RequestError:
#         print("Could not request results; check your internet connection.")
#         return None
