import os
import random
import string
from datetime import datetime


class FileNameGenerator:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_unique_filename(file_path):
        file_name, file_extension = os.path.splitext(file_path)
        random_string = FileNameGenerator.generate_random_string(7)
        new_file_name = f"{file_name}_{random_string}{file_extension}"
        while os.path.exists(new_file_name):
            random_string = FileNameGenerator.generate_random_string(7)
            new_file_name = f"{file_name}_{random_string}{file_extension}"
        return new_file_name

    @staticmethod
    def generate_unique_filename_timestamp(file_path):
        file_name, file_extension = os.path.splitext(file_path)
        time_stamp = datetime.now()
        new_file_name = f"{file_name}_{time_stamp}{file_extension}"
        return new_file_name
