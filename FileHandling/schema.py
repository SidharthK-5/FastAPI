from pydantic import BaseModel


class EditFile(BaseModel):
    file_name: str
    new_content: str
