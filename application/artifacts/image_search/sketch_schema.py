"""Defines schema for database sketch objects"""
from flask import current_app
from marshmallow import fields

from application.base_schema import BaseSchema, output_decorator
from ..artifact_schema import ARTIFACT_SCHEMA


class SketchSchema(BaseSchema):
    """Schema for importing and exporting neo sketch objects"""

    id_ = fields.String(missing=None)
    created_at = fields.DateTime(missing=None)
    updated_at = fields.DateTime(missing=None)
    file_url = fields.String(missing=None)
    intended_artifact = fields.Nested(ARTIFACT_SCHEMA)

    @output_decorator
    def transform_fields(self, data):
        """Transforms field for output"""
        data["url"] = self.build_url(data.pop("file_url"))
        data["id"] = data.pop("id_")
        return data

    @staticmethod
    def build_url(file_url):
        """Schema: fileserver/id_filename"""
        return current_app.config["FILE_SERVER"] + "/" + file_url

SKETCH_SCHEMA = SketchSchema(decorate=True)
SKETCHES_SCHEMA = SketchSchema(decorate=True, many=True)
