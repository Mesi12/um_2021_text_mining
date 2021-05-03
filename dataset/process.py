import os
import re
import json


# config
PATH_INPUT = "original"
PATH_OUTPUT = "processed"
PATH_NOVELS = "novels"
PATH_STORIES = "stories"
FILENAME_METADATA = "metadata.json"
METADATA = {
    "novels": {},
    "collections": {}
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
                title = get_title(content, "novel")
                
                # clean content
                content = remove_header(content, "novel")
                content = remove_footer(content)

                # rename file with copy to processed
                export_path = os.path.join(PATH_OUTPUT, PATH_NOVELS)
                clean_title = title.lower().replace(" ", "_")
                export_file(clean_title, export_path, content)

                # put into metadata
                METADATA["novels"][clean_title] = {}
                METADATA["novels"][clean_title]["title"] = title


def read_collections():
    """
    Handles stories to be processed.
    """
    FOLDER_PATH = os.path.join(PATH_INPUT, PATH_STORIES)
    for collection in os.listdir(FOLDER_PATH):
        PATH_COLLECTION = os.path.join(FOLDER_PATH,collection)
        try:
            collection_title = make_title(collection)
        except NameError:
            continue

        print(f"Process collection: {collection_title}")
        
        # set metadata for collection
        METADATA["collections"][collection] = {}
        METADATA["collections"][collection]["title"] = collection_title
        METADATA["collections"][collection]["stories"] = {}


        for f in os.listdir(PATH_COLLECTION):
            #print(f)
            filepath = os.path.join(PATH_COLLECTION,f)
            if os.path.isfile(filepath) and f.endswith(".txt"):
                print(f"Process file: {filepath}")

                with open(filepath, "r") as fp:
                    content = fp.read()

                    #get title of story
                    title = get_title(content,"story")

                    #remove header and footer
                    content = remove_header(content,"story")
                    content = remove_footer(content)
                    content = cleanup_stories(content)

                    # rename file with copy to processed
                    export_path = os.path.join(PATH_OUTPUT, PATH_STORIES, collection)
                    clean_title = title.lower().replace(" ", "_").replace("-","_").replace('"',"").replace("'","")
                    export_file(clean_title, export_path, content)

                    # put into metadata
                    METADATA["collections"][collection]["stories"][clean_title] = {}
                    METADATA["collections"][collection]["stories"][clean_title]["title"] = title


def make_title(collection):
    if collection == "1_the_adventures_of_sherlock_holmes":
        original_title = "The Adventures of Sherlock Holmes"
    elif collection == "2_the_memoirs_of_sherlock_holmes":
        original_title = "The Memoirs of Sherlock Holmes"
    elif collection == "3_the_return_of_sherlock_holmes":
        original_title = "The Return of Sherlock Holmes"
    elif collection == "4_his_last_bow":
        original_title = "His Last Bow"
    elif collection == "5_the_case_book_of_sherlock_holmes":
        original_title = "The Case-Book of Sherlock Holmes"
    else:
        raise NameError(f"Provided name {collection} is not valid. Skip it.")
    return original_title


def get_title(content, tp):
    if tp == "novel":
        re_grep_title = '(.+)\n\n.*Arthur Conan Doyle'
        parts = re.search(re_grep_title, content, re.IGNORECASE)
        if parts:
            title = parts.group(1).strip()
            print(f".. {title}")
            
    elif tp == "story":
        re_grep_title =  '(.*)\n *\n +(.+)\n\n +Arthur Conan Doyle'
        parts = re.search(re_grep_title, content, re.IGNORECASE)

        if parts:
            title = parts.group(1).strip() + ' ' + parts.group(2).strip()
            title = title.strip()
            print(f".. {title}")
    return title


def export_file(title, export_path, content):
    new_name = title + ".txt"
    os.makedirs(export_path, exist_ok=True)
    with open(os.path.join(export_path, new_name), "w") as fp_new:
        fp_new.write(content)


def remove_header(content, tp):
    if tp == "novel":
        re_grep_header = '\n+.+\n\n.*Arthur Conan Doyle\n+ +Table of contents\n\n?( +.*\n\n?)+\n\n\n'
    elif tp == "story":
        re_grep_header = '\n+.*\n *\n.*\n\n *Arthur Conan Doyle(?:\n+ +Table of contents(?:\n +.+)+\n{3})?'
        
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

def cleanup_stories(data):
    clean_data = []

    chapters = re.split(" {10}chapter[^\n]+", data, flags = re.IGNORECASE)
    print(len(chapters))
    for i, chapter in enumerate(chapters):
        print(f"{i} - {len(chapter)}")

        # put each paragraph into seperate line
        chapter = re.sub(r"(?<=.)\n(?!\n)", " ", chapter)

        # remove whitespaces in front of paragraphs
        chapter = re.sub(r"^ {5}", "", chapter, flags = re.MULTILINE)

        # clean up multiple whitespaces / new lines
        chapter = re.sub(r"\n{3,}", "\n\n", chapter)
        chapter = re.sub(r" {2,}", " ", chapter)

        # clean up before and after chapter
        chapter = chapter.strip("\n").strip(" ")

        clean_data.append(chapter)


    if clean_data[0] == "":
        clean_data.pop(0)

    return "\n\n".join(clean_data)


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
    read_collections()
    save_metadata()
