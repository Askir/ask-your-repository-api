from flask.cli import AppGroup
from application.artifacts.image_search.searcher import Searcher
from application.artifacts.image_search.sketch import Sketch
from application.artifacts.artifact import Artifact
from flask import current_app

debug_cli = AppGroup("debug")


@debug_cli.command("something")
def something():
    print(Searcher.default().search('91919aef-9dc2-46e1-b7f3-8608709c1d40_anna-pelzer-472429-unsplash_1080w.jpg', Artifact.all()))


@debug_cli.command("evaluate")
def evaluate():
    results = {}
    for sketch in Sketch.all():
        if sketch.intended_result.single() == None:
            continue
        results[sketch.id_] = sketch.ordered_results.index(sketch.intended_result.single())
    print(results)

@debug_cli.command("search")
def search():
    for sketch in Sketch.all():
        Searcher.default().search(sketch.file_url, Artifact.all(), sketch)

@debug_cli.command("load")
def load():
    pass

def add_debug_scripts(app):
    app.cli.add_command(debug_cli)

