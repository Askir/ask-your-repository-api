import pathlib
import uuid
from binascii import a2b_base64

from flask import current_app
from flask_apispec import MethodResource, use_kwargs, marshal_with

from .sketch import Sketch
from .sketch_schema import SKETCHES_SCHEMA, SKETCH_SCHEMA
from ..artifact_schema import ARTIFACTS_SCHEMA
from .sketch_validator import create_args, modify_args, search_args
from ..artifact import Artifact
from .searcher import Searcher


def _save_search_image(data_uri):
    header, image = data_uri.split(",", 1)
    image = image + "=="
    binary_data = a2b_base64(image)
    pathlib.Path('search_images').mkdir(parents=True, exist_ok=True)

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    image_file_name = f"search_images/{uuid.uuid4()}.png"
    search_image_path = f"{upload_folder}/{image_file_name}"
    fd = open(search_image_path, 'wb')
    fd.write(binary_data)
    fd.close()
    return search_image_path, image_file_name


class SketchesView(MethodResource):
    @use_kwargs(create_args())
    @marshal_with(SKETCH_SCHEMA)
    def post(self, **params):
        file_path, file_name = _save_search_image(params.pop('sketch'))
        sketch = Sketch(file_url=file_name, **params).save()
        return sketch

    @marshal_with(SKETCHES_SCHEMA)
    def get(self):
        sketches = Sketch.all()
        return sketches


class SketchView(MethodResource):
    @use_kwargs(modify_args())
    @marshal_with(SKETCH_SCHEMA)
    def put(self, **params):
        sketch = Sketch.find_by(id_=params.pop('sketch_id'))
        sketch.intended_result.disconnect_all()
        artifact = Artifact.find_by(params.get('intended_image'))
        sketch.intended_result.connect(artifact)
        sketch.save()
        return sketch

    @use_kwargs(search_args())
    @marshal_with(ARTIFACTS_SCHEMA)
    def search(self, **params):
        sketch = Sketch.find_by(id_=params.get('sketch_id'))
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        file_path = f"{upload_folder}/{sketch.file_url}"
        return Searcher.default().search(file_path, Artifact.all(), sketch)
