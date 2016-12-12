import os
import time

from PIL import Image
from celery import Celery

app = Celery(
    'taskqueue', #__name__
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

@app.task
def add(a, b):
    time.sleep(5)
    return a + b

@app.task
def sum2(values):
    print(values)
    #assert isinstance(values, [list,tuple])
    time.sleep(5)
    return sum(values)

@app.task
def make_thumbnail(path, width, height):
    filepath, ext = os.path.splitext(path)
    output_path = '{}_thumb{}'.format(filepath, ext)

    if os.path.exists(output_path):
        return output_path

    #im = Image.open(path)
    #im.thumbnail([width, height], Image.LANCZOS)
        # 이미지가 뭉개지는 걸 막기 위해 알고리즘 지정
    #im.save(output_path)
    #im.close()

    with Image.open(path) as im:
        im.thumbnail([width, height], Image.LANCZOS)
        im.save(output_path)

    return output_path
