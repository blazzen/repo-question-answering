import os

from pydriller import RepositoryMining

from source_file import SourceFile
from source_method import METHOD_FULL_NAME_SEPARATOR
from util import get_pure_filename, to_df
from source_paragraphs_transformer import SourceParagraphsTransformer

SRC_FILE_SUFFIX = ".java"


class GitData:
    def __init__(self, methods_initial_commits, methods_last_modification_commits):
        self.methods_initial_commits = methods_initial_commits
        self.methods_last_modification_commits = methods_last_modification_commits


class Miner:
    def __init__(self, repo_dir, src_dir_suffix):
        self.repo_dir = repo_dir
        self.src_dir_suffix = src_dir_suffix
        self.src_dir = os.path.join(repo_dir, src_dir_suffix)
        self.files = []

    def mine(self):
        files = self.mine_current_repository_state()
        git_data = self.mine_git_repository_data()
        self.connect_mined_data(files, git_data)
        self.files = files
        return to_df(SourceParagraphsTransformer.to_paragraph_like_view(files))

    def mine_current_repository_state(self):
        files = []
        for dir_path, dir_names, filenames in os.walk(self.src_dir):
            for filename in filenames:
                if self.is_java_file(filename):
                    file_path = os.path.join(dir_path, filename)
                    files.append(SourceFile(file_path))
        return files

    def mine_git_repository_data(self):
        methods_initial_commits = {}
        methods_last_modification_commits = {}
        for commit in RepositoryMining(self.repo_dir, order='reverse').traverse_commits():
            for modification in commit.modifications:
                if not self.is_java_file(modification.filename) or not modification.new_path \
                        or self.src_dir_suffix not in modification.new_path:
                    continue

                new_methods = {x.name for x in modification.methods}
                old_methods = {x.name for x in modification.methods_before}
                added_methods = new_methods - old_methods

                for method in new_methods:
                    enriched_method_name = self.resolve_enriched_method_name(method, modification.filename)
                    if method in added_methods:
                        methods_initial_commits[enriched_method_name] = commit
                    if enriched_method_name not in methods_last_modification_commits:
                        methods_last_modification_commits[enriched_method_name] = commit
        return GitData(methods_initial_commits, methods_last_modification_commits)

    @staticmethod
    def connect_mined_data(initial_data, git_data):
        for file in initial_data:
            for method in file.methods:
                if method.is_abstract:
                    continue

                initial_commit = git_data.methods_initial_commits[method.name_with_class]
                method.enrich_with_initial_commit_data(initial_commit)

                last_modification_commit = git_data.methods_last_modification_commits[method.name_with_class]
                method.enrich_with_last_modification_commit_data(last_modification_commit)

    @staticmethod
    def resolve_enriched_method_name(method_name, filename):
        if len(method_name.split(METHOD_FULL_NAME_SEPARATOR)) == 1:
            return METHOD_FULL_NAME_SEPARATOR.join([get_pure_filename(filename), method_name])
        return method_name

    @staticmethod
    def is_java_file(filename):
        return filename.endswith(SRC_FILE_SUFFIX)
