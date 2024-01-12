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

def double_llm(message1, message2, message3, **kwargs) -> str:
    # print(f"[Debug Info] messages = {messages}")
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        # model="gpt-3.5",
        messages=[
            {"role": "system", "content": "You are an agent and you will complete a task."},
            {"role": "user", "content": f"{message1}"},
            {"role": "assistant", "content": f"{message2}"},
            {"role": "user", "content": f"{message3}"}
        ]
    )
    content = response.choices[0].message.content
    return content


def load_denoised_data(filename: str):
    with open(f"./dataset/GPT_denoised/{filename}.txt", "r") as f:
        content = f.read()
    return content

def vanilla_generation_prompt(keyword: str):
    pre_prompt = "You are an expert in writing Encyclopedia documents. "
    pre_prompt += "I will give you some materials for your reference, based on which you should generate an Encyclopedia document. "
    pre_prompt += "Your generated Encyclopedia document should be structured as a real Encyclopedia document. "
    pre_prompt += "You should only output your generated Encyclopedia document, without other sentences. "
    pre_prompt += f"\n \n The key word is: {keyword}.           "
    pre_prompt += "Here is the original materials, for your reference: \n \n"
    post_prompt = "\n \n Now it's your turn. You should only output your generated Encyclopedia document, without other sentences."
    return pre_prompt, post_prompt

def CoT(keyword):
    CoT_prompt = "Let's think step by step. First, please answer these questions: \n \n "
    CoT_prompt += "1. What is a common structure of an Encyclopedia document? \n"
    CoT_prompt += f"2. What do you know about the key word, {keyword}? \n"
    CoT_prompt += "3. Please give a sentence-level outline of your Encyclopedia document, describing what you would convey in each part. \n"
    return CoT_prompt

def ICL(example_keyword, example_ground_truth):
    ICL_prompt = f"Here is an example Encyclopedia document, whose key word is {example_keyword}: \n"
    ICL_prompt += f"\n {example_ground_truth} \n \n"
    ICL_prompt += "Now it's your turn. Here is the original materials, for your reference: \n \n"
    return ICL_prompt

def pre_define():
    pre_defined_prompt = "\n A common Encyclopedia document contains the following parts: \n \n"
    pre_defined_prompt += "1. Introduction \n"
    pre_defined_prompt += "2. History or Biography \n"
    pre_defined_prompt += "3. Detailed Explanations \n"
    pre_defined_prompt += "4. Debates or Supporting Evidences over this topic \n"
    pre_defined_prompt += "5. Broad Impact or Applications \n"
    pre_defined_prompt += "6. References \n \n "
    pre_defined_prompt += "You can generate your Encyclopedia document following this structure. \n \n"
    pre_defined_prompt += "Here is the original materials, for your reference: \n \n"
    return pre_defined_prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="orange", type=str)
    parser.add_argument("--method", default=1, type=int)  # 1: vanilla baseline; 2: CoT; 3: ICL; 4: pre-defined template outline  
    args = parser.parse_args()
    method = args.method

    # load in example ground truth for ICL
    with open(f"./dataset/ground_truth/bottle_gt.txt", "r") as f:
        example_ground_truth = f.read()
    example_keyword = "bottle"

    files = os.listdir("./dataset/rank_top_3/")

    ICL_prompt = ICL(example_keyword, example_ground_truth)
    pre_defined_prompt = pre_define()
    original_content = ""
    for keyword in ["GreatWall", "luxun", "MoM", "montezuma", "RLHF", "whale"]:
        print(f"[Debug Info] keyword == {keyword}")
        for original_file in files:
            if keyword in original_file:
                original_content += load_denoised_data(original_file[:-4])[:2000]           # truncated to first 2000 characters
                original_content += "\n \n"
        pre_prompt, post_prompt = vanilla_generation_prompt(keyword)
        CoT_prompt = CoT(keyword)

        for method in [1, 2, 3, 4]:
            print(f"[Debug Info] method == {method}")
            if method == 1:
                response = llm(pre_prompt + original_content + post_prompt)
            elif method == 2:
                intermediate = llm(pre_prompt[:-56] + CoT_prompt)
                response = double_llm(pre_prompt[:-56] + CoT_prompt, intermediate, 
                                    "Based on your answers above, please generate. Here is the original materials, for your reference: \n \n" + original_content + post_prompt)
            elif method == 3:
                response = llm(pre_prompt[:-56] + ICL_prompt + original_content + post_prompt)
            elif method == 4:
                response = llm(pre_prompt[:-56] + pre_defined_prompt + original_content + post_prompt)

            with open(f"./generated_truncated/{method}/{keyword}.txt", "w") as f:
                f.write(response)


    # original_content = load_denoised_data(args.file)
    # pre_prompt, post_prompt = vanilla_generation_prompt(args.file)
    # CoT_prompt = CoT(args.file)
    # ICL_prompt = ICL(example_keyword, example_ground_truth)
    # pre_defined_prompt = pre_define()

    # if method == 1:
    #     response = llm(pre_prompt + original_content + post_prompt)
    # elif method == 2:
    #     intermediate = llm(pre_prompt[:-56] + CoT_prompt)
    #     response = double_llm(pre_prompt[:-56] + CoT_prompt, intermediate, 
    #                           "Based on your answers above, please generate. Here is the original materials, for your reference: \n \n" + original_content + post_prompt)
    # elif method == 3:
    #     response = llm(pre_prompt[:-56] + ICL_prompt + original_content + post_prompt)
    # elif method == 4:
    #     response = llm(pre_prompt[:-56] + pre_defined_prompt + original_content + post_prompt)

    # with open(f"./generated/{method}/{args.file}.txt", "w") as f:
    #     f.write(response)