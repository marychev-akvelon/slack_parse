import os
from shutil import copytree
from slack_file import SlackFile


class SlackParse:
    BACKUP_FILENAME = '__BACKUP__'

    def __init__(self, path):
        self.path = path
        self.real_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_root = os.path.join(self.real_path, self.path)

    def run(self, dir_root=None):
        self.dir_root = dir_root if dir_root else self.dir_root
        self.analyze_and_create_copies()
        self.process_copied_files()
        self.delete_copy_files()
        self.apply_fixed_files()

    def analyze_and_create_copies(self):
        for filename in os.listdir(self.dir_root):
            filepath = self.get_full_path(filename)
            self.run(filepath) if os.path.isdir(filepath) else SlackFile(filepath).copy_file()

    def process_copied_files(self):
        print('PROCCESS PATH:', self.dir_root)
        for entry in os.listdir(self.dir_root):
            filename = self.get_full_path(entry)

            if SlackFile.PREFIX_COPY in entry and SlackParse.BACKUP_FILENAME not in self.path:
                slack_file = SlackFile(filename)
                slack_file.create_fix_file()

    def delete_copy_files(self):
        for filename in os.listdir(self.dir_root):
            filepath = self.get_full_path(filename)

            if SlackFile.PREFIX_COPY in filename:
                os.remove(filepath)
                # print('Delete copy file: {}'.format(filepath))

    def apply_fixed_files(self):
        for filename in os.listdir(self.dir_root):
            filepath = self.get_full_path(filename)
            slack_file = SlackFile(filepath)
            slack_file.replace_fix_file(filename)

    def backup(self):
        print('backup', self.dir_root, self.path, self.real_path)
        copytree(self.dir_root, SlackParse.BACKUP_FILENAME)

    def show_tree(self, dir_root=None):
        print('>> TREE <<')
        self.dir_root = dir_root if dir_root else self.dir_root

        for entry in os.listdir(self.dir_root):
            full_path = os.path.join(self.dir_root, entry)
            print(full_path)

            if os.path.isdir(full_path):
                self.show_tree(full_path)

    def get_full_path(self, filename):
        return os.path.join(self.dir_root, filename)

    @staticmethod
    def help():
        with open('./readme.md') as file:
            print(file.read())
