from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="hola",
)

messages = [
    {
        "role": "system",
        "content": "You're a helpful assistant that can answer anything.",
    }
]

while True:
    question = input("Enter your question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    stream = client.chat.completions.create(
        messages=messages,
        model="deepseek-r1-distill-qwen-7b",
        stream=True,
    )

    assistant_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        print(content, end="")
        assistant_response += content
    print()

    messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )
