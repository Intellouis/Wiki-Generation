import os
import nltk
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

def calculate_bleu(reference_texts, candidate_text):
    """
    Calculate the BLEU score for a candidate text based on reference texts.

    :param reference_texts: A list of reference translations (each reference is a list of tokens)
    :param candidate_text: The candidate translation (a list of tokens)
    :return: BLEU score
    """
    smoothing = SmoothingFunction().method1
    return sentence_bleu(reference_texts, candidate_text, smoothing_function=smoothing)


def lcs_length_dp(x, y):
    """
    Compute the length of the longest common subsequence between two sequences using dynamic programming.

    :param x: First sequence
    :param y: Second sequence
    :return: Length of LCS
    """
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

def rouge_l(reference, candidate):
    """
    Calculate the ROUGE-L score for a candidate sentence based on a reference sentence.

    :param reference: Reference sentence (list of tokens)
    :param candidate: Candidate sentence (list of tokens)
    :return: ROUGE-L score
    """
    lcs = lcs_length_dp(reference, candidate)
    if lcs == 0:
        return 0
    precision = lcs / len(candidate)
    recall = lcs / len(reference)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1



if __name__ == "__main__":
    filenames = os.listdir("./dataset/GPT_denoised/")
    for each_file in filenames:
        print(f"filename = {each_file}")
        with open(f"./dataset/original/{each_file}", "r") as f:
            candidate_1 = f.read().split()
        with open(f"./dataset/rule_based_denoised/{each_file}", "r") as f:
            candidate_2 = f.read().split()
        with open(f"./dataset/GPT_denoised/{each_file}", "r") as f:
            candidate_3 = f.read().split()
        with open(f"./dataset/human_denoised/{each_file}", "r") as f:
            reference = f.read().split()
        bleu = calculate_bleu(reference, candidate_1)
        print(bleu, end="     ")
        bleu = calculate_bleu(reference, candidate_2)
        print(bleu, end="     ")
        bleu = calculate_bleu(reference, candidate_3)
        print(bleu, end="     ")
        rouge = rouge_l(reference, candidate_1)
        print(rouge, end="     ")
        rouge = rouge_l(reference, candidate_2)
        print(rouge, end="     ")
        rouge = rouge_l(reference, candidate_3)
        print(rouge)