# %%
import os
import json

def create_file_list():

    rootdir = os.path.join(os.getcwd(), "processed")
    paths = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".txt"):
                paths.append(os.path.join(subdir, file))

    with open("file_paths.txt", "w") as f:
        f.write("\n".join(paths))

    print("file file_paths.txt created.")


def novel_to_txt_by_chapter(title):
    folder = os.path.join("processed", "novels")
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        if os.path.isfile(filepath) and file == f"{title}.json":
            print(f"Process file: {filepath}")
            with open(filepath, "r") as f:
                novel = json.load(f)
            
            output = os.path.join(folder, title)
            os.makedirs(output, exist_ok=True)
            all_files = []
            for p, chapters in novel.items():
                for c, chapter in chapters.items():
                    output_file = f"{p}_{c}.txt"
                    all_files.append(os.path.join(os.getcwd(), output, output_file))
                    print(output_file)
                    with open(os.path.join(output, output_file), "w") as f:
                        f.write(chapter['text'])
            
            with open(os.path.join(output, "all_files.txt"), "w") as f:
                f.write("\n".join(all_files))



if __name__ == "__main__":
    #create_file_list()
    novel = novel_to_txt_by_chapter("a_study_in_scarlet")
# %%
