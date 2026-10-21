from flask import Blueprint, Response, abort, make_response, request

from app.models.book import Book

from ..db import db
from ..models.author import Author
from .route_utilities import create_model_with_response, get_models_with_filters_with_response, validate_model

bp = Blueprint("author_bp", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    return create_model_with_response(Author, request.get_json())

@bp.get("")
def get_all_authors():
    return get_models_with_filters_with_response(Author, request.args) 

@bp.get("/<author_id>")
def get_one_author(author_id):
    author = validate_model(Author, author_id)

    return author.to_dict()

@bp.put("/<author_id>")
def update_author(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()

    author.name = request_body["name"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<author_id>")
def delete_author(author_id):
    author = validate_model(Author, author_id)
    db.session.delete(author)
    db.session.commit()

    return Response(status=204, mimetype="application/json")



@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    
    request_body = request.get_json()
    request_body["author_id"] = author.id

    try:
        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
        
    db.session.add(new_book)
    db.session.commit()

    return make_response(new_book.to_dict(), 201)

@bp.get("/<author_id>/books")
def get_all_books_by_author_id(author_id):
    author = validate_model(Author, author_id)
    return [book.to_dict() for book in author.books]