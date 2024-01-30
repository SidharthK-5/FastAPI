import os
from helper import generate_unique_filename


class FileHandleController:
    @staticmethod
    def process_upload(file):
        try:
            upload_dir = "uploads"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            file_name = file.filename
            file_path = os.path.join(upload_dir, file_name)

            while os.path.exists(file_path):
                new_file_name = generate_unique_filename(file_name)
                file_path = os.path.join(upload_dir, new_file_name)

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            response = f"File '{file_name}' uploaded successfully... New {file_path=}"
            return response

        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}

    @staticmethod
    def list_file_names():
        try:
            file_names = os.listdir(path="uploads")
            return file_names
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}

    @staticmethod
    def read_file(file_name: str):
        try:
            file_path = os.path.join("uploads", file_name)
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
    def delete_file(file_name: str):
        try:
            file_path = os.path.join("uploads", file_name)
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
