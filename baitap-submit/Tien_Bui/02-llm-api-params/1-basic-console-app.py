from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="hola",
)

question = input("Enter your question: ")

stream = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You're a helpful assistant that can answer anything.",
        },
        {"role": "user", "content": question},
    ],
    model="deepseek-r1-distill-qwen-7b",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
print()
