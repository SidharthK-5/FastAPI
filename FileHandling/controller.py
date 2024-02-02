import os
from helper import FileNameGenerator

SUPPORTED_FILES = ["txt"]
UPLOAD_DIR = "uploads"


class FileHandleController:
    @staticmethod
    def process_upload(file):
        try:
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)

            file_name = file.filename
            file_path = os.path.join(UPLOAD_DIR, file_name)

            while os.path.exists(file_path):
                new_file_name = FileNameGenerator.generate_unique_filename_timestamp(
                    file_name
                )
                file_path = os.path.join(UPLOAD_DIR, new_file_name)

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            return {
                "message": f"File '{file_name}' uploaded successfully... New {file_path=}",
                "status_code": 201,
            }

        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}

    @staticmethod
    def list_file_names():
        try:
            if not os.path.exists(UPLOAD_DIR):
                return {"message": "Upload directory is empty!!!", "status_code": 200}
            else:
                file_names = os.listdir(path=UPLOAD_DIR)
                if len(file_names) == 0:
                    return {
                        "message": "Upload directory is empty!!!",
                        "status_code": 200,
                    }
                else:
                    return {"message": file_names, "status_code": 200}
        except Exception as e:
            return {
                "message": f"Encountered an error - {str(e)}",
                "status_code": 404,
            }

    @staticmethod
    def read_file(file_name: str):
        try:
            file_path = os.path.join(UPLOAD_DIR, file_name)
            with open(file=file_path, mode="r") as file:
                file_content = file.read()
                file.close()
            return {"message": file_content, "status_code": 200}
        except FileNotFoundError:
            return {
                "message": f"File {file_name} is not present!!!",
                "status_code": 404,
            }

    @staticmethod
    def edit_file(file_name: str, new_content: str):
        try:
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found")
            else:
                with open(file=file_path, mode="w") as file:
                    file.write(new_content)
                return {
                    "message": f"File {file_name} edited successfully...",
                    "status_code": 201,
                }
        except FileNotFoundError:
            return {
                "message": f"File {file_name} is not present!!!",
                "status_code": 404,
            }

    @staticmethod
    def delete_file(file_name: str):
        try:
            file_path = os.path.join(UPLOAD_DIR, file_name)
            os.remove(path=file_path)
            return {
                "message": f"File {file_name} removed successfully!!!",
                "status_code": 200,
            }
        except FileNotFoundError:
            return {
                "message": f"File {file_name} is not present!!!",
                "status_code": 404,
            }
