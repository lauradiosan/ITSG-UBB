import os
from shutil import rmtree


class FileUtils:
    def get_test_files(self, test_folder):
        result = []
        for file in os.listdir(test_folder):
            if ".png" in file:
                json_file = file[:-3] + "json"
                if os.path.exists(test_folder + json_file):
                    result.append((file, json_file))
                else:
                    result.append((file, None))
        return result

    def create_folder(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        return folder

    def delete_files(self, folder, file_type):
        test = os.listdir(folder)

        for item in test:
            if item.endswith(file_type):
                os.remove(os.path.join(folder, item))

    def delete_folder(self, folder):
        rmtree(folder)

    def is_of_type(self, path, term):
        return path.endswith(term)
