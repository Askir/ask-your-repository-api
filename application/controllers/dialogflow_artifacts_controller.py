from flask import current_app
from webargs.flaskparser import use_args
from .. import socketio
from ..responders import no_content, respond_with
from ..error_handling.es_connection import check_es_connection
from ..models.artifact import Artifact
from ..models.team import Team
from ..validators import dialogflow_artifacts_validator
from .application_controller import ApplicationController

class DialogflowArtifactsController(ApplicationController):
    """ Controller for Artifacts """

    method_decorators = [check_es_connection]

    @use_args(dialogflow_artifacts_validator.search_args())
    def index(self, params):
        "Logic for querying several artifacts"

        team = Team.find_by(name=params.pop('image_name'))
        params["image_id"] = team.id_
        artifacts = Artifact.search(params)

        socketio.emit('START_PRESENTATION',
                      room=str(params["team_id"]),
                      data=respond_with(artifacts)
                      )
        return no_content()