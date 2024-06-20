from gtts import gTTS
from translate import Translator
import requests
import os
import pandas as pd
from datetime import datetime

# Define the target words
target_words = [
    "Hello, how are you",
    "What time is it",
    "Can you help me",
    "I love you.",
    "Thank you very much.",
    "Where are you from",
    "I'm sorry.",
    "Excuse me, where is the restroom",
    "Have a nice day",
    "Goodbye, see you later."
]

# Define the target language (language code)
target_language_code = "ru"
target_language_name = "russian"

# Directory to save audio files
output_dir = "pronunciations"
os.makedirs(output_dir, exist_ok=True)

# Function to generate and save audio
def generate_audio(text, lang_code, file_path):
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(file_path)
        print(f"Saved {file_path} ({target_language_name})")
    except Exception as e:
        print(f"Error generating audio for '{text}' in {target_language_name}: {e}")

# Function to create file names based on the first and last words of the phrase
def create_file_name(phrase, suffix, lang_code):
    words = phrase.split()
    if len(words) > 1:
        file_name = f"{words[0]}{words[-1]}_{suffix}_{lang_code}.mp3"
    else:
        file_name = f"{words[0]}_{suffix}_{lang_code}.mp3"
    return file_name

# Function to translate using the primary translator
def primary_translate(word, lang_code):
    try:
        translator = Translator(to_lang=lang_code)
        translated_word = translator.translate(word)
        return translated_word
    except Exception as e:
        print(f"Primary translation API failed for '{word}': {e}")
        return None

# Function to translate using the fallback MyMemory API
def fallback_mymemory_translate(word, lang_code):
    try:
        response = requests.get(f"https://api.mymemory.translated.net/get?q={word}&langpair=en|{lang_code}")
        result = response.json()
        translated_word = result['responseData']['translatedText']
        return translated_word
    except Exception as e:
        print(f"MyMemory translation API failed for '{word}': {e}")
        return None

# Function to translate using the fallback LibreTranslate API
def fallback_libretranslate(word, lang_code):
    try:
        response = requests.post(
            "https://libretranslate.com/translate",
            data={
                "q": word,
                "source": "en",
                "target": lang_code,
                "format": "text"
            }
        )
        result = response.json()
        translated_word = result['translatedText']
        return translated_word
    except Exception as e:
        print(f"LibreTranslate API failed for '{word}': {e}")
        return None

# Initialize a list to store translation data
translations = []

# Translate the words and generate audio files
for word in target_words:
    try:
        # Try primary translation
        translated_word = primary_translate(word, target_language_code)
        
        # If primary translation fails, use MyMemory translation
        if not translated_word or translated_word.strip() == "":
            translated_word = fallback_mymemory_translate(word, target_language_code)
        
        # If MyMemory translation fails, use LibreTranslate translation
        if not translated_word or translated_word.strip() == "":
            translated_word = fallback_libretranslate(word, target_language_code)
        
        # Skip if no translation is received
        if not translated_word or translated_word.strip() == "":
            print(f"Skipping '{word}' as translation could not be retrieved.")
            continue
        
        # Construct the full texts for the audio parts
        audio_text_en_intro = f"Hey, do you know how to pronounce {word} in {target_language_name}? It goes like,"
        audio_text_translated = translated_word
        audio_text_en_outro = "Follow us, for more such content!"
        final_audio_text = f"{audio_text_en_intro} {audio_text_translated} {audio_text_en_outro}"
        
        # Save translation to the list with the final audio text
        translations.append({
            "Word": word,
            "Language": target_language_name,
            "Translated Word": translated_word,
            "Final Audio Text": final_audio_text
        })
        
        # Generate file names
        file_name_intro = create_file_name(word, "en_intro", target_language_code)
        file_name_translated = create_file_name(word, "translated", target_language_code)
        file_name_outro = create_file_name(word, "en_outro", target_language_code)
        combined_file_name = create_file_name(word, "combined", target_language_code)
        
        # Generate the audio file for the English introductory text
        file_path_en_intro = os.path.join(output_dir, file_name_intro)
        generate_audio(audio_text_en_intro, 'en', file_path_en_intro)
        
        # Generate the audio file for the translated word in the target language
        file_path_translated = os.path.join(output_dir, file_name_translated)
        generate_audio(audio_text_translated, target_language_code, file_path_translated)
        
        # Generate the audio file for the English closing phrase
        file_path_en_outro = os.path.join(output_dir, file_name_outro)
        generate_audio(audio_text_en_outro, 'en', file_path_en_outro)
        
        # Combine the three audio files into one
        combined_file_path = os.path.join(output_dir, combined_file_name)
        os.system(f"ffmpeg -y -i \"concat:{file_path_en_intro}|{file_path_translated}|{file_path_en_outro}\" -acodec copy {combined_file_path}")
        print(f"Combined and saved {combined_file_path} ({target_language_name})")
        
    except Exception as e:
        print(f"Error processing '{word}': {e}")

# Save translations to a CSV file with a unique name
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
csv_file_name = f"translations_{target_language_name}_{timestamp}.csv"
translations_df = pd.DataFrame(translations)
translations_df.to_csv(os.path.join(output_dir, csv_file_name), index=False, encoding='utf-8')

print("All audio files have been generated and saved.")
print(f"Translations have been saved to {csv_file_name}.")
