from flask.cli import AppGroup
from application.artifacts.image_search.searcher import Searcher
from application.artifacts.artifact import Artifact

debug_cli = AppGroup("debug")


@debug_cli.command("something")
def something():
    print(Searcher.default().search('91919aef-9dc2-46e1-b7f3-8608709c1d40_anna-pelzer-472429-unsplash_1080w.jpg', Artifact.all()))

def add_debug_scripts(app):
    app.cli.add_command(debug_cli)
