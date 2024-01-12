
import os
import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import language_tool_python
import textstat


def check_topic_consistency(documents):
    texts = [[word for word in document.lower().split()] for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = LdaModel(corpus, num_topics=1, id2word=dictionary, passes=15)
    topics = lda.print_topics(num_words=4)
    for topic in topics:
        print(topic)

def check_grammar(text):
    # tool = language_tool_python.LanguageTool('en-US')
    tool = language_tool_python.LanguageTool('en-US', config={ 'maxTextLength': 100000 })
    matches = tool.check(text)
    return len(matches)

def readability_score(text):
    return textstat.flesch_reading_ease(text)


def main0():
    """
    Check the metrics on denoised data.
    """
    for method in ["original", "rule_based_denoised", "GPT_denoised", "human_denoised"]:
        print(f"\n \n \n  method: {method}")
        filenames = os.listdir(f"./dataset/{method}/")
        for file in filenames:
            print(f"\n file: {file}")
            with open(f"./dataset/{method}/{file}", "r") as f:
                text = f.read()
            grammar_errors = check_grammar(text)
            readability = readability_score(text)

            print(f"Grammar Errors: {grammar_errors}               ", end="")
            print(f"Readability Score: {readability}")
    

    # for method in ["original", "rule_based_denoised", "GPT_denoised", "human_denoised"]:
    #     print(f"\n \n \n  method: {method}")
    #     filenames = os.listdir(f"./dataset/{method}/")
    #     for keyword in ["GreatWall", "luxun", "MoM", "montezuma", "RLHF", "whale"]:
    #         print(f"\n keyword: {keyword}")
    #         for file in filenames:
    #             if keyword in file:
    #                 with open(f"./dataset/{method}/{file}", "r") as f:
    #                     text = f.read()
    #                 grammar_errors = check_grammar(text)
    #                 readability = readability_score(text)

    #                 print(f"Grammar Errors: {grammar_errors}               ", end="")
    #                 print(f"Readability Score: {readability}")


def main1():
    # evaluate the performance of wiki generation
    filenames = os.listdir("./generated_top_3/1/")
    for each_task in filenames:
        print(f"\n \n \n task = {each_task}")

        print(f"\n >>> vanilla")
        with open(f"./generated_top_3/1/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")
        
        print(f"\n >>> CoT")
        with open(f"./generated_top_3/2/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")

        print(f"\n >>> ICL")
        with open(f"./generated_top_3/3/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")

        print(f"\n >>> predefined")
        with open(f"./generated_top_3/4/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")


if __name__ == "__main__":
    # evaluate the performance of wiki generation
    filenames = os.listdir("./generated_truncated/1/")
    for each_task in filenames:
        print(f"\n \n \n task = {each_task}")

        print(f"\n >>> vanilla")
        with open(f"./generated_truncated/1/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        # print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")
        
        print(f"\n >>> CoT")
        with open(f"./generated_truncated/2/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        # print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")

        print(f"\n >>> ICL")
        with open(f"./generated_truncated/3/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        # print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")

        print(f"\n >>> predefined")
        with open(f"./generated_truncated/4/{each_task}", "r") as f:
            content = f.read()
        grammar_errors = check_grammar(content)
        readability = readability_score(content)
        # print(f"Grammar Errors: {grammar_errors}               ", end="")
        print(f"Readability Score: {readability}")