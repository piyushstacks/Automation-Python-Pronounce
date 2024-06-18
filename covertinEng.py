from gtts import gTTS
from translate import Translator
import os

# Define the target word
target_word = "hello"

# Define the target languages (language codes)
languages = {
    "en": "English",
    "zh-cn": "Chinese (Mandarin)",
    "es": "Spanish",
    "hi": "Hindi",
    "ar": "Arabic",
    "bn": "Bengali",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "pa": "Punjabi",
    "de": "German",
    "jv": "Javanese",
    "ko": "Korean",
    "fr": "French",
    "te": "Telugu",
    "mr": "Marathi",
    "tr": "Turkish",
    "ta": "Tamil",
    "vi": "Vietnamese",
    "ur": "Urdu"
}

# Directory to save audio files
output_dir = "pronunciations"
os.makedirs(output_dir, exist_ok=True)

# Function to generate and save audio
def generate_audio(text, lang_code, file_path):
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(file_path)
        print(f"Saved {file_path} ({languages[lang_code]})")
    except Exception as e:
        print(f"Error generating audio for '{text}' in {languages[lang_code]}: {e}")

# Generate and save the audio file for the input word in English
input_file_path = os.path.join(output_dir, f"{target_word}_en.mp3")
generate_audio(target_word, 'en', input_file_path)

# Translate the word and generate audio files for each target language
for lang_code, lang_name in languages.items():
    if lang_code != "en":
        try:
            # Translate the word
            translator = Translator(to_lang=lang_code)
            translated_word = translator.translate(target_word)
            
            # Construct the full text for the audio (English with translated word in target language)
            audio_text = f"Hey, Do you know how to Pronounce {target_word} in {languages[lang_code]}? It goes like {translated_word}. Follow us for more!"
            
            # Generate the audio file for the constructed text
            file_path = os.path.join(output_dir, f"{target_word}_{lang_code}.mp3")
            generate_audio(audio_text, 'en', file_path)
            
        except Exception as e:
            print(f"Error translating '{target_word}' to {languages[lang_code]}: {e}")

print("All audio files have been generated and saved.")
