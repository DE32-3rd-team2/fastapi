# FastAPI Age Prediction

### uploadfile
```python
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
```
- 이미지 업로드시, DB의 `face_age` TABLE의 이미지 관련 행에 데이터 추가
- Streamlit에서 API 호출하여, 이미지 업로드 가능한 웹사이트 구현 가능

### all
```python
@app.get("/all")
def all():
    from age_pred.db import select
    sql = "SELECT * FROM face_age"
    result = select(query=sql, size=-1)
    return result
```
- face_age TABLE에 저장된 모든 데이터를 불러오는 함수


### one
```python
@app.get("/one")
def pred():
    from age_pred.db import select
    sql = """
    SELECT num, file_path, prediction_result
    FROM face_age
    WHERE prediction_result IS NOT NULL AND answer IS NULL
    ORDER BY num
    """
    result = select(query=sql, size=-1)
    return result
```

- face_age TABLE의 데이터 중에서 예측을 완료하였지만, 정답 라벨이 NULL인 row를 불러오는 함수
- Streamlit 웹페이지에서 정답 라벨을 입력하기 위하여 활용