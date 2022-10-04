import uuid

from flask import Blueprint, g, jsonify, abort

from packages.database.bases.base_connector import BaseORMConnectorMethods
from packages.http.content_type import ContentTypeEnum
from packages.pymodels.smtp_models import PySMTPMessageModel
from utils.decorators import content_type, request_to_object

smtp_blueprint = Blueprint("smtp", "SMTPBlueprint", url_prefix="/smtp")


@smtp_blueprint.post('/message')
@content_type(ContentTypeEnum.APPLICATION_JSON)
@request_to_object(PySMTPMessageModel)
def post_smtp_message_create(request_object: PySMTPMessageModel):
    connector: BaseORMConnectorMethods = g.connector
    command_mode = connector.append_command(message=request_object)
    connector.append_raw_message(command_mode, request_object)
    return jsonify(command_mode.as_json)


@smtp_blueprint.get('message/command/<uuid:message_uuid>')
@content_type(ContentTypeEnum.APPLICATION_JSON)
def get_smtp_message_by_uuid(message_uuid: uuid.UUID):
    if message := g.connector.get_command_by_uuid(message_uuid):
        return jsonify(message.as_json)
    else:
        abort(404)


@smtp_blueprint.get('message/<uuid:message_uuid>')
@content_type(ContentTypeEnum.APPLICATION_JSON)
def get_raw_smtp_message_by_uuid(message_uuid: uuid.UUID):
    connector: BaseORMConnectorMethods = g.connector

    if message := connector.get_message_by_uuid(message_uuid):
        return jsonify(message.as_json)
    else:
        abort(404)
