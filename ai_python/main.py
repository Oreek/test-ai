from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pyttsx3
from speech_text import recognize_speech, read_speech
from flask import Flask, request, jsonify

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Set up the text-to-speech engine
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    chat_history_ids = None
    print("Say 'quit' to end the conversation.")
    
    while True:
        # Get user input through speech
        prompt = read_speech()
        
        # Check for quit command
        if prompt == "quit":
            print("Ending conversation. Goodbye!")
            speak_text("Goodbye!")
            break
        elif prompt:
            # Encode user input, append it to chat history
            new_user_input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
            
            # Generate response with a limit of 1000 tokens in history
            chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
            
            # Decode and print the response
            bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
            print(f"CoolMan: {bot_response}")
            
            # Speak the bot response
            speak_text(bot_response)

if __name__ == "__main__":
    main()



# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch


# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# # Let's chat for 5 lines
# for step in range(5):
#     # encode the new user input, add the eos_token and return a tensor in Pytorch
#     new_user_input_ids = tokenizer.encode(input(">> User: ") + tokenizer.eos_token, return_tensors='pt')

#     # append the new user input tokens to the chat history
#     bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

#     # generated a response while limiting the total chat history to 1000 tokens, 
#     chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

#     # pretty print last ouput tokens from bot
#     print("CoolMan: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import pyttsx3
# import pyaudio
# import json
# from vosk import Model, KaldiRecognizer

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Load the model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# # Load Vosk model for offline speech recognition
# vosk_model = Model("model")  # Ensure you have the Vosk model downloaded and placed in the correct directory

# def recognize_speech():
#     # Set up the audio stream
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 16000

#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

#     print("Listening...")

#     recognizer = KaldiRecognizer(vosk_model, RATE)
#     frames = []

#     while True:
#         data = stream.read(CHUNK)
#         if recognizer.AcceptWaveform(data):
#             result = recognizer.Result()
#             result_dict = json.loads(result)
#             if result_dict.get("text"):
#                 print(f"Recognized speech: {result_dict['text']}")
#                 stream.stop_stream()
#                 stream.close()
#                 p.terminate()
#                 return result_dict['text']

# def speak_text(text):
#     print(f"Speaking: {text}")
#     engine.say(text)
#     engine.runAndWait()

# def main():
#     chat_history_ids = None
#     print("Say 'quit' to end the conversation.")
    
#     while True:
#         user_input = recognize_speech()
        
#         if user_input is None:
#             continue
        
#         # Check for quit command
#         if user_input.lower() == "quit":
#             print("Ending conversation. Goodbye!")
#             speak_text("Goodbye!")
#             break
#         elif user_input:
#             # Encode user input, append it to chat history
#             new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
#             bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
            
#             # Generate response with a limit of 1000 tokens in history
#             chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
            
#             # Decode and print the response
#             bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
#             print(f"CoolMan: {bot_response}")
#             speak_text(bot_response)

# if __name__ == "__main__":
#     main()