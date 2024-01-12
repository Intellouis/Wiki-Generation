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

def choose_one_from_four(d1, d2, d3, d4):
    prompt = "Here are four passages of generated encyclopedia documents, and you should give a order of them based on these aspects: \n \n"
    prompt += "1. Fluency: Whether the entire passage reads smoothly and whether it is noisy (with polluted text). \n"
    prompt += "2. Understanding: Whether it is easy to understand with a clear meaning. \n"
    prompt += "3. Structure: Whether is is well structured with a clear organization. \n"
    prompt += "Here are the documents: \n \n"
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an agent and you will complete a task."},
            {"role": "user", "content": f"{prompt}"},
            {"role": "user", "content": f"This is the first document: \n \n {d1}"},
            {"role": "user", "content": f"This is the second document: \n \n {d2}"},
            {"role": "user", "content": f"This is the third document: \n \n {d3}"},
            {"role": "user", "content": f"This is the fourth document: \n \n {d4}"},
            {"role": "user", "content": f"You should give a ranking of them based on those metrics, from the best to the worst."}
        ]
    )
    content = response.choices[0].message.content
    return content

def prompt_denoising():
    pre_prompt = "Here is a passage, and you should evaluate it based on these aspects: \n \n"
    pre_prompt += "1. Fluency: Whether the entire passage reads smoothly and whether it is noisy (with polluted text). \n"
    pre_prompt += "2. Understanding: Whether it is easy to understand with a clear meaning. \n"
    pre_prompt += "3. Structure: Whether is is well structured with a clear organization. \n"
    pre_prompt += "Here is the passage: \n \n"
    post_prompt = "You should give ratings of these aspects (each out of 10), and a overall score. \n \n"
    return pre_prompt, post_prompt

def prompt_generation():
    pre_prompt = "Here is a generated encyclopedia document, and you should evaluate it based on these aspects: \n \n"
    pre_prompt += "1. Fluency: Whether the entire passage reads smoothly and whether it is noisy (with polluted text). \n"
    pre_prompt += "2. Understanding: Whether it is easy to understand with a clear meaning, which is user-friendly. \n"
    pre_prompt += "3. Structure: Whether it is well structured with a clear organization, which is proper for an encyclopedia document. \n"
    pre_prompt += "Here is the encyclopedia document: \n \n"
    post_prompt = "You should give ratings of these aspects (each out of 10), and a overall score. \n \n"
    return pre_prompt, post_prompt


def main():
    # # evaluate the performance of denoising
    # pre_prompt, post_prompt = prompt_denoising()
    # filenames = os.listdir("./dataset/original/")
    # for each_file in filenames:
    #     print(f"filename = {each_file}")

    #     with open(f"./dataset/original/{each_file}", "r") as f:
    #         candidate_1 = f.read()
    #     response = llm(pre_prompt + candidate_1 + post_prompt)
    #     with open(f"./evaluation_results/evaluation_of_denoising/original/{each_file}", "w") as f:
    #         f.write(response)

    #     with open(f"./dataset/rule_based_denoised/{each_file}", "r") as f:
    #         candidate_2 = f.read()
    #     response = llm(pre_prompt + candidate_2 + post_prompt)
    #     with open(f"./evaluation_results/evaluation_of_denoising/rule/{each_file}", "w") as f:
    #         f.write(response)

    #     with open(f"./dataset/GPT_denoised/{each_file}", "r") as f:
    #         candidate_3 = f.read()
    #     response = llm(pre_prompt + candidate_3 + post_prompt)
    #     with open(f"./evaluation_results/evaluation_of_denoising/gpt/{each_file}", "w") as f:
    #         f.write(response)

    #     # with open(f"./dataset/human_denoised/{each_file}", "r") as f:
    #     #     reference = f.read()
    #     # response = llm(pre_prompt + reference + post_prompt)
    #     # with open(f"./evaluation_results/evaluation_of_denoising/human/{each_file}", "w") as f:
    #     #     f.write(response)

    # evaluate the performance of wiki generation
    pre_prompt, post_prompt = prompt_generation()
    filenames = os.listdir("./generated_top_3/1/")
    for each_task in filenames:
        print(f"task = {each_task}")

        with open(f"./generated_top_3/1/{each_task}", "r") as f:
            content = f.read()
        response = llm(pre_prompt + content + post_prompt)
        with open(f"./evaluation_results/evaluation_of_generation_rank_top_3/vanilla/{each_task}", "w") as f:
            f.write(response)

        with open(f"./generated_top_3/2/{each_task}", "r") as f:
            content = f.read()
        response = llm(pre_prompt + content + post_prompt)
        with open(f"./evaluation_results/evaluation_of_generation_rank_top_3/CoT/{each_task}", "w") as f:
            f.write(response)

        with open(f"./generated_top_3/3/{each_task}", "r") as f:
            content = f.read()
        response = llm(pre_prompt + content + post_prompt)
        with open(f"./evaluation_results/evaluation_of_generation_rank_top_3/ICL/{each_task}", "w") as f:
            f.write(response)

        with open(f"./generated_top_3/4/{each_task}", "r") as f:
            content = f.read()
        response = llm(pre_prompt + content + post_prompt)
        with open(f"./evaluation_results/evaluation_of_generation_rank_top_3/predefined/{each_task}", "w") as f:
            f.write(response)

        
def main2():
    # evaluate the performance of wiki generation
    filenames = os.listdir("./generated/1/")
    for each_task in filenames:
        print(f"task = {each_task}")

        with open(f"./generated/1/{each_task}", "r") as f:
            d1 = f.read()

        with open(f"./generated/2/{each_task}", "r") as f:
            d2 = f.read()

        with open(f"./generated/3/{each_task}", "r") as f:
            d3 = f.read()

        with open(f"./generated/4/{each_task}", "r") as f:
            d4 = f.read()

        response = choose_one_from_four(d1, d2, d3, d4)
        with open(f"./evaluation_results/evaluation_of_generation/choose_one_from_four/{each_task}", "w") as f:
            f.write(response)


if __name__ == "__main__":
    main()