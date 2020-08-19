import os
import json
from shutil import copyfile
from pathlib import Path


class SlackFile:
    PREFIX_COPY = 'COPY__'
    PREFIX_FIX = 'FIX__'

    def __init__(self, path):
        self._path = Path(path) if os.path.isfile(path) else ValueError
        self.filename = self._path.name
        self.file_dir = self._path.parent
        self.copy_name = '{}{}'.format(SlackFile.PREFIX_COPY, self.filename)
        self.copy_dir = os.path.join(self.file_dir, self.copy_name)
        self.json_data = self._json_data()
        self.can_copy = bool(self._analyze_data())

    def __str__(self):
        return str(self._path.absolute())

    def _json_data(self):
        with open(self._path) as file:
            return [data for data in json.load(file)]

    def _analyze_data(self):
        for data in self.json_data:
            if SlackFile.rules_to_fix(data):
                # print('File "{}" must be copy!'.format(self.filename))
                return True

    def copy_file(self):
        if SlackFile.PREFIX_COPY not in self.filename and self.can_copy:
            copyfile(self._path, self.copy_dir)

    def fix_json(self):
        new_json = []
        for data in self.json_data:
            new_json.append(self.fix(data)) if SlackFile.rules_to_fix(data) else new_json.append(data)
        return new_json

    def create_fix_file(self):
        fix_file = str(self._path).replace(SlackFile.PREFIX_COPY, SlackFile.PREFIX_FIX)
        with open(fix_file, 'w') as outfile:
            json.dump(self.fix_json(), outfile, indent=4)

    def replace_fix_file(self, origin_filename):
        if SlackFile.PREFIX_FIX in origin_filename and os.path.isfile(self._path):
            old_fix_file = str(self._path).replace(SlackFile.PREFIX_FIX, '')

            if os.path.isfile(old_fix_file):
                os.remove(old_fix_file)

            os.rename(self._path, old_fix_file)

    @staticmethod
    def fix(obj):
        if SlackFile.rules_to_fix(obj):
            del obj['files']
            del obj['upload']
            print('Object was fixed!')
        return obj

    @staticmethod
    def rules_to_fix(obj):
        return bool(
            obj.get('files') is not None and obj.get('upload') is not None and (
                obj.get('type') is not None and obj['type'] == 'message') and (
                    obj.get('text') is not None and obj['text'] != '')
        )

