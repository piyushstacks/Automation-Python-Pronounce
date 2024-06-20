from gtts import gTTS
from translate import Translator
import os
import pandas as pd

# Define the target word
target_word = "how are you"

# Define the target languages (language codes)
languages = {
    "en": "English",
    # "zh-cn": "Chinese (Mandarin)",
    # "es": "Spanish",
    # "hi": "Hindi",
    # "ar": "Arabic",
    # "bn": "Bengali",
    # "pt": "Portuguese",
    # "ru": "Russian",
    # "ja": "Japanese",
    # "pa": "Punjabi",
    "de": "German",
    # "jv": "Javanese",
    # "ko": "Korean",
    # "fr": "French",
    # "te": "Telugu",
    # "mr": "Marathi",
    # "tr": "Turkish",
    # "ta": "Tamil",
    # "vi": "Vietnamese",
    # "ur": "Urdu"
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
# Initialize a list to store translation data
translations = []

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
            
            # Construct the full texts for the audio parts
            audio_text_en_intro = f"Hey, do you know how to pronounce {target_word} in {lang_name}? It goes like,"
            audio_text_translated = translated_word
            audio_text_en_outro = "Follow us, for more such content!"
            final_audio_text = f"{audio_text_en_intro} {audio_text_translated} {audio_text_en_outro}"
            
            # Save translation to the list with the final audio text
            translations.append({
                "Language": lang_name,
                "Translated Word": translated_word,
                "Final Audio Text": final_audio_text
            })
            
            # Generate the audio file for the English introductory text
            file_path_en_intro = os.path.join(output_dir, f"{target_word}_{lang_code}_en_intro.mp3")
            generate_audio(audio_text_en_intro, 'en', file_path_en_intro)
            
            # Generate the audio file for the translated word in the target language
            file_path_translated = os.path.join(output_dir, f"{target_word}_{lang_code}_translated.mp3")
            generate_audio(audio_text_translated, lang_code, file_path_translated)
            
            # Generate the audio file for the English closing phrase
            file_path_en_outro = os.path.join(output_dir, f"{target_word}_{lang_code}_en_outro.mp3")
            generate_audio(audio_text_en_outro, 'en', file_path_en_outro)
            
            # Combine the three audio files into one
            combined_file_path = os.path.join(output_dir, f"{target_word}_{lang_code}.mp3")
            os.system(f"ffmpeg -y -i \"concat:{file_path_en_intro}|{file_path_translated}|{file_path_en_outro}\" -acodec copy {combined_file_path}")
            print(f"Combined and saved {combined_file_path} ({lang_name})")
            
        except Exception as e:
            print(f"Error translating '{target_word}' to {lang_name}: {e}")

# Save translations to a CSV file
translations_df = pd.DataFrame(translations)
translations_df.to_csv(os.path.join(output_dir, "translations.csv"), index=False, encoding='utf-8')

print("All audio files have been generated and saved.")
print("Translations have been saved to translations.csv.")
