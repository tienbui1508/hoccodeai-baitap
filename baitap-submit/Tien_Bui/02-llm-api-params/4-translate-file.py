# Requirements: pip install openai nltk

from openai import OpenAI
import os
import nltk
import re

nltk.download("punkt", quiet=True)
from nltk.tokenize import sent_tokenize, word_tokenize

# === CONFIG ===
CHUNK_WORDS = 1000  # Max words per chunk (adjust as needed)

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key="5170d1b0ae5f7a6f18b4cd8804fa153fc438026a1874b825e735295d961a35d7",
    #     base_url="http://localhost:1234/v1",
    #     api_key="key",
)


def get_input_file():
    filename = input("Enter the name of the file to translate: ").strip()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    if not os.path.isfile(file_path):
        print(f"File '{filename}' not found.")
        exit(1)
    return file_path, filename


def get_target_language():
    return input("Enter the target language (e.g., English, Vietnamese): ").strip()


def build_system_prompt(target_language):
    return (
        f"You are a professional translator. Detect the original language of the following text, "
        f"then translate it into {target_language}. Keep the original meaning, context, and tone. "
        f"Only output the translated text. Do not include any explanation or comments."
    )


def chunk_sentences_by_word_count(filepath, max_words):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    sentences = sent_tokenize(text)
    chunks, current_chunk, current_count = [], "", 0
    for sentence in sentences:
        wc = len(word_tokenize(sentence))
        if current_count + wc <= max_words:
            current_chunk += (" " if current_chunk else "") + sentence
            current_count += wc
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
            current_count = wc
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def remove_think_blocks(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def translate_chunk(chunk, system_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": chunk},
    ]
    try:
        response = client.chat.completions.create(
            messages=messages,
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            # model="llama-3.2-3b-instruct",
        )
        return remove_think_blocks(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"API error: {e}")
        return ""


def get_output_filename(input_filename, target_language):
    name, ext = os.path.splitext(input_filename)
    return f"{name}_translated_to_{target_language}{ext}"


def main():
    input_file_path, input_filename = get_input_file()
    target_language = get_target_language()
    system_prompt = build_system_prompt(target_language)
    output_file = get_output_filename(input_filename, target_language)
    print("Splitting file into sentence-based chunks...")
    chunks = chunk_sentences_by_word_count(input_file_path, CHUNK_WORDS)
    translated_chunks = []
    for idx, chunk in enumerate(chunks):
        print(f"Translating chunk {idx+1}/{len(chunks)}...")
        # translated_chunks.append(f"Part {idx+1}")
        # translated_chunks.append(chunk)  # Keep original chunk for reference
        translated_chunks.append(translate_chunk(chunk, system_prompt))
    print("Writing translated text to output file...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_chunks))
    print(f"Done! Translated file saved as {output_file}")


if __name__ == "__main__":
    main()
