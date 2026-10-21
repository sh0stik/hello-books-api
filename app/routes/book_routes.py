from flask import Blueprint, Response, abort, make_response, request

from ..db import db
from ..models.book import Book
from .route_utilities import create_model_with_response, get_models_with_filters_with_response, validate_model

bp = Blueprint("book_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    return create_model_with_response(Book, request.get_json())


@bp.get("")
def get_all_books():
    return get_models_with_filters_with_response(Book, request.args)

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
