from openai import OpenAI
import requests

headers = {
    "Authorization": "Bearer jina_216d9cf2c5284828b1a532ad64feed1cPATNH1TN3a2oGzMzgrG4a_AZK7wY"
}

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="key",
)
systemContent = """
                    From the provided markdown website content, determine the language used, then use that language to summarise its main content clearly and concisely.
                    Keep the summary brief—about 1 to 2 paragraphs—and suitable for someone seeking a quick overview before visiting the site.
                    /no_think"""

while True:
    userInput = input(
        "Enter the website you want to summarise (or type 'exit' to quit): "
    )
    if userInput.lower() == "exit":
        print("Goodbye!")
        break

    url = "https://r.jina.ai/" + userInput
    response = requests.get(url, headers=headers)

    messages = [
        {
            "role": "system",
            "content": systemContent,
        }
    ]
    messages.append(
        {
            "role": "user",
            "content": response.text,
        }
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="deepseek-r1-distill-qwen-7b",
        stream=True,
    )

    print(chat_completion.choices[0].message.content)
