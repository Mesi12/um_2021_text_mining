
if __name__ == "__main__":
    import os

    rootdir = os.path.join(os.getcwd(), "processed")
    paths = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".txt"):
                paths.append(os.path.join(subdir, file))

    with open("file_paths.txt", "w") as f:
        f.write("\n".join(paths))

    print("file file_paths.txt created.")
