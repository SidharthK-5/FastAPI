from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from controller import FileHandleController
from schema import EditFile

router = APIRouter(prefix="/file")


@router.post("/upload/")
async def upload_file(file: UploadFile):
    extension = file.filename.lower().split(".")[-1]
    supported_ext = extension in ("txt")
    if not supported_ext:
        return JSONResponse(
            content=f"File type .{extension} is not supported!!!", status_code=500
        )
    response = FileHandleController.process_upload(file)
    status_code = response.get("status_code")
    if not status_code:
        status_code = 500
    return JSONResponse(
        content={"response": response["message"]}, status_code=status_code
    )


@router.get("/list-all")
async def list_all_files():
    response = FileHandleController.list_file_names()
    print(f"{response=}")
    return JSONResponse(
        content=response.get("message"), status_code=response.get("status_code")
    )


@router.get("/read-file")
async def read_file_by_name(file_name: str):
    response = FileHandleController.read_file(file_name=file_name)
    return JSONResponse(
        content={"content": response["message"]}, status_code=response["status_code"]
    )


@router.put("/edit-file")
async def edit_file_by_name(edit_file: EditFile):
    response = FileHandleController.edit_file(**edit_file.model_dump())
    return JSONResponse(
        content={"message": response["message"]}, status_code=response["status_code"]
    )


@router.delete("/delete-file")
async def delete_file_by_name(file_name: str):
    response = FileHandleController.delete_file(file_name=file_name)
    return JSONResponse(
        content={"message": response["message"]}, status_code=response["status_code"]
    )
