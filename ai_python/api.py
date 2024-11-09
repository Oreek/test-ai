from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pyttsx3
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Set up the text-to-speech engine
# engine = pyttsx3.init()

# def speak_text(text):
#     engine.say(text)
#     engine.runAndWait()

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize chat_history_ids as a global variable
chat_history_ids = None

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history_ids  # Use the global variable to store chat history
    
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    if prompt.lower() == "quit":
        response = "Goodbye!"
        # speak_text(response)
        return jsonify({'response': response})
    
    # Encode user input, append it to chat history
    new_user_input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
    
    # Generate response with a limit of 1000 tokens in history
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # Decode and print the response
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(f"CoolMan: {bot_response}")
    
    # Speak the bot response
    # speak_text(bot_response)
    
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
