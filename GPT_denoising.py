import os
import json
import yaml
import random
from openai import OpenAI
import argparse

api_key = "API_KEY"     # replace with your API key
client = OpenAI(api_key=api_key)

def llm(messages, **kwargs) -> str:
    # print(f"[Debug Info] messages = {messages}")
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an agent and you will complete a task."},
            {"role": "user", "content": f"{messages}"}
        ]
    )
    content = response.choices[0].message.content
    return content

def load_original_data(filename: str):
    with open(f"./dataset/original/{filename}.txt", "r") as f:
        content = f.read()
    return content

def denoising_prompt():
    pre_prompt = "The following text is noisy. I want you to rewrite the text and denoise. "
    pre_prompt += "You should make as few modifications as possible and try to keep the meaning of original text unchanged. "
    pre_prompt += "Here is the original text: \n \n"
    post_prompt = "You should only output the re-written text, without any other sentences."
    return pre_prompt, post_prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="orange", type=str)
    args = parser.parse_args()

    original_content = load_original_data(args.file)
    pre_prompt, post_prompt = denoising_prompt()
    response = llm(pre_prompt + original_content + post_prompt)

    with open(f"./dataset/denoised/{args.file}.txt", "w") as f:
        f.write(response)