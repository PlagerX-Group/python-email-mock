from flask import Blueprint, g, jsonify

from packages.database.connector import SMTPDatabaseConnector
from packages.pymodels.smtp_models import PySMTPMessageModel
from utils.decorators import content_type, request_to_object

smtp_blueprint = Blueprint("smtp", "SMTPBlueprint", url_prefix="/smtp")


@smtp_blueprint.post('/message')
@content_type('application/json')
@request_to_object(PySMTPMessageModel)
def post_smtp_message_create(request_object: PySMTPMessageModel):
    connector: SMTPDatabaseConnector = g.connector
    connector.append_message(message=request_object)

    return jsonify(request_object.as_json)
