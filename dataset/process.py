import os
import re
import json


# config
PATH_INPUT = "original"
PATH_OUTPUT = "processed"
PATH_NOVELS = "novels"
FILENAME_METADATA = "metadata-test.json"
METADATA = {
    "novels": {},
    "stories": {}
}


def process_novels():
    """
    Handles novels to be processed.
    """
    FOLDER_PATH = os.path.join(PATH_INPUT, PATH_NOVELS)
    for f in os.listdir(FOLDER_PATH):
        filepath = os.path.join(FOLDER_PATH,f)
        if os.path.isfile(filepath) and f.endswith(".txt"):
            print(f"Process file: {filepath}")

            with open(filepath, "r") as fp:
                content = fp.read()
                title = get_title(content)
                
                # clean content
                content = remove_header(content)
                content = remove_footer(content)

                # rename file with copy to processed
                export_path = os.path.join(PATH_OUTPUT, PATH_NOVELS)
                clean_title = title.lower().replace(" ", "_")
                export_file(clean_title, export_path, content)

                # put into metadata
                METADATA["novels"][clean_title] = {}
                METADATA["novels"][clean_title]["title"] = title



def get_title(content):
    re_grep_title = '(.+)\n\n.*Arthur Conan Doyle'
    parts = re.search(re_grep_title, content, re.IGNORECASE)

    if parts:
        title = parts.group(1).strip()
        print(f".. {title}")
    return title


def export_file(title, export_path, content):
    new_name = title + ".txt"
    os.makedirs(export_path, exist_ok=True)
    with open(os.path.join(export_path, new_name), "w") as fp_new:
        fp_new.write(content)


def remove_header(content):
    re_grep_header = '\n+.+\n\n.*Arthur Conan Doyle\n+ +Table of contents\n\n?( +.*\n\n?)+\n\n\n'
    header = re.search(re_grep_header, content, re.IGNORECASE)

    if header:
        content = content[len(header.group(0)):]
    return content


def remove_footer(content):
    re_grep_footer = '( +-{3,10}\n +This text is provided to you)'
    footer = re.search(re_grep_footer, content, re.IGNORECASE)

    if footer:
        pos_footer_start = content.find(footer.group(1))
        content = content[:pos_footer_start]
    return content



# todo finish function
def read_collections():
    return True



def save_metadata():
    """
    Saves metadata into the json file.
    """
    with open(FILENAME_METADATA, "w") as fp:
        parsed = json.dumps(METADATA, indent=4, sort_keys=True)
        fp.write(parsed)



if __name__ == "__main__":
    print("start")
    process_novels()
    save_metadata()
