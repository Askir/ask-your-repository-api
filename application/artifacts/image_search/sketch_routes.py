"""Provides Artifact functionality and routes"""
from flask import Blueprint

from .sketch_view import SketchesView, SketchView

SKETCHES = Blueprint("sketches", __name__)

SKETCHES.add_url_rule("", view_func=SketchesView.as_view("artifactsview"))
SKETCHES.add_url_rule("/<sketch_id>", view_func=SketchView.as_view("artifactview"))

SKETCHES.add_url_rule("/<sketch_id>/search", "search", SketchView().search, methods=["GET"])
