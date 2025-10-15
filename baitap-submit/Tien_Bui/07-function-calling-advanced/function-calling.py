from pprint import pprint
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import inspect
from pydantic import TypeAdapter
import requests

load_dotenv()

# Implement 3 hàm


def get_current_weather(location: str, unit: str):
    """Get the current weather in a given location"""
    # Hardcoded response for demo purposes
    return "Trời rét vãi nôi, 7 độ C"


def get_stock_price(symbol: str):
    # Không làm gì cả, để hàm trống
    pass


# Bài 2: Implement hàm `view_website`, sử dụng `requests` và JinaAI để đọc markdown từ URL
def view_website(url: str)->str:
    # Không làm gì cả, để hàm trống
    """
    Get the content of a given website URL
    :param url: The url of the website to view
    :return: The content of the website
    """
    url_jina = f'https://r.jina.ai/{url}'
    headers = {
        'Accept': 'application/json',
        'X-Return-Format': 'markdown'
    }
    response = requests.get(url_jina, headers=headers)
    return response.text


# Bài 1: Thay vì tự viết object `tools`, hãy xem lại bài trước, sửa code và dùng `inspect` và `TypeAdapter` để define `tools`
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": inspect.getdoc(get_current_weather),
            "parameters": TypeAdapter(get_current_weather).json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": inspect.getdoc(get_stock_price),
            "parameters": TypeAdapter(get_stock_price).json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "view_website",
            "description": inspect.getdoc(view_website),
            "parameters": TypeAdapter(view_website).json_schema(),
        },
    },
]

# https://platform.openai.com/api-keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=OPENAI_API_KEY,
)
COMPLETION_MODEL = "gpt-5-mini"

# messages = [{"role": "user", "content": "Thời tiết ở Hà Nội hôm nay thế nào?"}]
messages = [{"role": "user", "content": "Trang này nói gì https://en.wikipedia.org/wiki/Artificial_intelligence"}]

print("Bước 1: Gửi message lên cho LLM")
pprint(messages)

response = client.chat.completions.create(
    model=COMPLETION_MODEL, messages=messages, tools=tools
)

print("Bước 2: LLM đọc và phân tích ngữ cảnh LLM")
pprint(response)

print("Bước 3: Lấy kết quả từ LLM")
tool_call = response.choices[0].message.tool_calls[0]

pprint(tool_call)
arguments = json.loads(tool_call.function.arguments)

print("Bước 4: Chạy function get_current_weather ở máy mình")

if tool_call.function.name == "get_current_weather":
    weather_result = get_current_weather(
        arguments.get("location"), arguments.get("unit")
    )
    # Hoặc code này cũng tương tự
    # weather_result = get_current_weather(**arguments)
    print(f"Kết quả bước 4: {weather_result}")

    print("Bước 5: Gửi kết quả lên cho LLM")
    messages.append(response.choices[0].message)
    messages.append(
        {"role": "tool", "content": weather_result, "tool_call_id": tool_call.id}
    )

    pprint(messages)

    final_response = client.chat.completions.create(
        model=COMPLETION_MODEL,
        messages=messages,
        # Ở đây không có tools cũng không sao, vì ta không cần gọi nữa
    )
    print(f"Kết quả cuối cùng từ LLM: {final_response.choices[0].message.content}.")

elif tool_call.function.name == "view_website":
    print("Chạy hàm view_website")
    web_content = view_website(
        arguments.get("url")
    )

    print(f"Kết quả bước 4: {web_content}")

    print("Bước 5: Gửi kết quả lên cho LLM")
    messages.append(response.choices[0].message)
    messages.append(
        {"role": "tool", "content": web_content, "tool_call_id": tool_call.id}
    )

    pprint(messages)

    final_response = client.chat.completions.create(
        model=COMPLETION_MODEL,
        messages=messages,

    )
    print(f"Kết quả cuối cùng từ LLM: {final_response.choices[0].message.content}.")
