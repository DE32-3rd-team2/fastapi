# FastAPI Age Prediction

```python
@app.get("/all")
def all():
    from age_pred.db import select
    sql = "SELECT * FROM face_age"
    result = select(query=sql, size=-1)
    return result
```
face_age TABLE에 저장된 모든 데이터를 불러오는 함수


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