import os

dirty_words = [
    "$", "pay", "sale", "ad", "advertisement", "discount", "license", "Play", "IMAGE", "YouTube", "AD", "ADVERTISEMENT", "written by", "Acknowledgement",
    "ISBN", "Reading Time", "BY ", " ON ", " IN ", "REPORT THIS AD", "NOVEMBER", "DECEMBER", "reading time", "Screen Shot", "image", ".png", ".jpg", ".jpeg",
    "http", "link", "download", "Download", "Screenshot", "2023-", "Read about", "Andy", "min read", ", 2023", "source:", "Aug ", "EDT", "UTC", "Photograph:",
    "Report this ad", "share", "Share", "VERSION", "DOWNLOAD", "September ", "JAMES", "James"
]

def denoising(content):
    idx_to_be_deleted = []
    split_content = content.split("\n")
    for i in range(0, len(split_content)-1):
        if split_content[i] in split_content[i+1]:
            # split_content.remove(split_content[i])
            # del split_content[i]
            idx_to_be_deleted.append(i)
        elif split_content[i+1] in split_content[i]:
            # split_content.remove(split_content[i+1])
            # del split_content[i+1]
            idx_to_be_deleted.append(i+1)
        for word in dirty_words:
            if word in split_content[i]:
                # split_content.remove(split_content[i])
                # del split_content[i]
                idx_to_be_deleted.append(i)
    for j in sorted(list(set(idx_to_be_deleted)), reverse=True):
        del split_content[j]
    return "\n".join(split_content)


if __name__ == "__main__":
    files = os.listdir("./dataset/denoised/")
    for original_file in files:
        print(f"[Debug Info] original_file == {original_file}")
        with open(f"./dataset/original/{original_file}", "r") as f:
            content = f.read()
        content = denoising(content)
        with open(f"./dataset/rule_based_denoised/{original_file}", "w") as f:
            f.write(content)
        