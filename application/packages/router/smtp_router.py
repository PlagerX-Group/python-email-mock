from flask import Blueprint, g, request, jsonify

from packages.database.connector import SMTPDatabaseConnector
from utils.decorators import content_type

smtp_blueprint = Blueprint("smtp", "SMTPBlueprint", url_prefix="/smtp")


@smtp_blueprint.post('/message')
@content_type('application/json')
def post_smtp_message_create():
    connector: SMTPDatabaseConnector = g.connector
    request_body = request.json

    return jsonify(request_body)
