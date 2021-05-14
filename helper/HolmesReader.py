# %%
import os
import json
import subprocess
import pandas as pd
from pandas.core.arrays import boolean


class HolmesReader:
    """Helper for reading holmes stories"""

    def __init__(self):
        # credits: https://stackoverflow.com/questions/22081209/find-the-root-of-the-git-repository-where-the-file-lives#comment44778829_22081487
        self.repo_dir = subprocess.Popen(
            ['git', 'rev-parse', '--show-toplevel'],
            stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
        self.metadata = self._read_metadata()

    def _read_metadata(self):
        """
        Reads metadata from json file.
        """
        filename_metadata = os.path.join(self.repo_dir, "helper", "metadata.json")
        with open(filename_metadata, "r") as fp:
            parsed = json.load(fp)
        return parsed

    def get_collections(self, as_dataframe=False):
        collections = self.metadata['collections'].copy()

        for collection_id, collection in collections.items():
            for story_id, story in collection['stories'].items():

                # filepath
                filepath = os.path.join(self.repo_dir, "dataset", "processed", "stories", collection_id, f"{story_id}.txt")

                if os.path.isfile(filepath):
                    with open(filepath, "r") as fp:
                        story['text'] = fp.read()
        if as_dataframe:
            coll_ids = []
            frames = []
            for coll_id, coll in collections.items():
                coll_ids.append(coll_id)
                frames.append(pd.DataFrame.from_dict(coll['stories'], orient="index"))
            df = pd.concat(frames, keys=coll_ids)
            df = df.reset_index()
            df = df.rename({"level_0":"collection", "level_1":"story"}, axis=1).drop("title", axis=1)
            return df

        return collections

    def get_collection(self, wanted_collection_id):
        collections = self.metadata['collections'].copy()

        if wanted_collection_id not in list(collections.keys()):
            raise FileNotFoundError(f"Collection id {wanted_collection_id} not found.")

        for collection_id, collection in collections.items():
            if collection_id != wanted_collection_id:
                continue

            for story_id, story in collection['stories'].items():

                # filepath
                filepath = os.path.join(self.repo_dir, "dataset", "processed", "stories", collection_id, f"{story_id}.txt")

                if os.path.isfile(filepath):
                    with open(filepath, "r") as fp:
                        story['text'] = fp.read()

        return collections

    def get_story(self, wanted_story_id):
        collections = self.metadata['collections'].copy()

        for collection_id, collection in collections.items():

            for story_id, story in collection['stories'].items():

                if story_id != wanted_story_id:
                    continue

                # filepath
                filepath = os.path.join(self.repo_dir, "dataset", "processed", "stories", collection_id, f"{story_id}.txt")

                if os.path.isfile(filepath):
                    with open(filepath, "r") as fp:
                        story['text'] = fp.read()
                
                return story

        return None

    def get_novels(self):
        novels = self.metadata['novels'].copy()

        for novel_id, novel in novels.items():

            # filepath
            filepath = os.path.join(self.repo_dir, "dataset", "processed", "novels", f"{novel_id}.json")

            if os.path.isfile(filepath):
                with open(filepath, "r") as fp:
                    novel['text'] = json.load(fp)

        return novels

    def get_metadata(self):
        return self.metadata
