from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from utils.exceptions import BaseHttpException

index_blueprint = Blueprint("index", "IndexBlueprint", url_prefix="/")


@index_blueprint.app_errorhandler(BaseHttpException)
def exception_handler(exc: BaseHttpException):
    return jsonify(exc.jsonify_response), exc.status_code


@index_blueprint.app_errorhandler(SQLAlchemyError)
def exception_sqlalchemy_handler(exc: SQLAlchemyError):
    return jsonify({"detail": exc.args[0].replace('\n', ' ').replace('\"', '\'').strip(),
                    "status_code": 500}), 500


@index_blueprint.app_errorhandler(500)
def handler_500_exc(exc: Exception):
    return jsonify({"detail": exc.args, "status_code": 500}), 500


@index_blueprint.app_errorhandler(405)
def handler_405_exc(exc: HTTPException):
    return jsonify({'detail': f"{exc.description}", "status_code": 405}), 405


@index_blueprint.app_errorhandler(404)
def handler_405_exc(exc: HTTPException):
    return jsonify({'detail': f"Page not found: {request.path}", "status_code": 404}), 404


@index_blueprint.app_errorhandler(400)
def handler_400_exc(exc: HTTPException):
    return jsonify({'detail': f'{exc.name}: {exc.description}', 'status_code': 400}), 400


@index_blueprint.app_errorhandler(ValidationError)
def pydantic_validation_error(exc: ValidationError):
    return jsonify({'detail': f"ValidationError", 'status_code': 400,
                    'args': exc.errors()}), 400
