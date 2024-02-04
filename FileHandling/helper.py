import os
import random
import string
from datetime import datetime
import docx
from pypdf import PdfReader


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


class FileReader:
    @staticmethod
    def read_text(file_path: str) -> str:
        with open(file=file_path, mode="r") as file:
            file_content = file.read()
            file.close()
        return file_content

    @staticmethod
    def read_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        file_content = ""

        total_pages = len(reader.pages)
        for page_id in range(total_pages):
            page = reader.pages[page_id].extract_text()
            file_content = file_content + "\n\n" + page

        return file_content

    @staticmethod
    def read_docx(file_path: str) -> str:
        document = docx.Document(file_path)
        file_content = ""

        for paragraph in document.paragraphs:
            file_content = file_content + "\n\n" + paragraph.text

        return file_content
