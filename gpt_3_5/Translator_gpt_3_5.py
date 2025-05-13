import openai
import csv
import os

# Set your OpenAI API key here
openai.api_key = "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"

# Your input Azerbaijani texts
input_texts = [
    "Sumqayıtda dəniz mənzərəli villa kirayə verilir. Sahəsi 200 kv.m. Qiymət 1200 AZN. Əlaqə: +994552223344",
    "Bakıda 3 otaqlı mənzil satılır. Sahə 100 kv.m. Qiymət 180,000 AZN. Əlaqə: +994501234567",
    "Gəncədə torpaq sahəsi satılır. Qiymət 50,000 AZN. Əlaqə: +994507654321"
]

# Output CSV filename
csv_filename = "translations_with_probabilities.csv"


def translate_and_get_probabilities(text):
    prompt = f"""
Translate the following Azerbaijani sentence into English. 
Then for each Azerbaijani word, give the best English translation and a probability (0-100% confidence).

Sentence:
{text}

Return format strictly JSON:
{{
  "translated_text": "...",
  "words": [
    {{
      "azerbaijani_word": "...",
      "english_translation": "...",
      "probability": "..." 
    }},
    ...
  ]
}}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0  # for more deterministic output
        )
        reply = response['choices'][0]['message']['content']
        return reply
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None


def save_to_csv(data, filename):
    headers = ["input_text", "translated_text", "azerbaijani_word", "english_translation", "probability"]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for entry in data:
            input_text = entry['input_text']
            translated_text = entry['translated_text']
            for word_info in entry['words']:
                writer.writerow({
                    "input_text": input_text,
                    "translated_text": translated_text,
                    "azerbaijani_word": word_info.get('azerbaijani_word', ''),
                    "english_translation": word_info.get('english_translation', ''),
                    "probability": word_info.get('probability', '')
                })


def main():
    all_data = []

    for text in input_texts:
        print(f"Processing: {text}")
        result_json = translate_and_get_probabilities(text)

        if result_json:
            try:
                # Parse JSON
                import json
                parsed = json.loads(result_json)
                all_data.append({
                    "input_text": text,
                    "translated_text": parsed.get("translated_text", ""),
                    "words": parsed.get("words", [])
                })
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")

    # Save all data to CSV
    save_to_csv(all_data, csv_filename)
    print(f"Saved results to {csv_filename}")


if __name__ == "__main__":
    main()
