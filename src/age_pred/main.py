from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
import os
import pymysql.cursors

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    img = await file.read()
    origin_name = file.filename
    file_ext = file.content_type.split('/')[-1]

    upload_dir = os.getenv('UPLOAD_DIR','/home/ubuntu/images')

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    import uuid

    file_path = os.path.join(upload_dir,
            f'{uuid.uuid4()}.{file_ext}')

    with open(file_path, "wb") as f:
        f.write(img)

    sql = """
        INSERT INTO face_age (origin_name, file_path, request_time)
        VALUES(%s, %s, %s)
    """

    from jigeumseoul import seoul
    request_time = seoul.now()

    from age_pred.db import dml
    insert_row = dml(sql, origin_name, file_path, request_time)

    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_path,
            "insert_row_cont": insert_row
           }

@app.get("/all")
def all():
    from age_pred.db import select
    sql = "SELECT * FROM face_age"
    result = select(query=sql, size=-1)
    return result
