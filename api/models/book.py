import datetime
from flask import jsonify, request, abort
from api import db
from api.models.validate import HelloBooks
from api.models.user import User


class Books(db.Model):
    '''Class containing book functions'''

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    author = db.Column(db.String(60))
    date_published = db.Column(db.String(60))
    genre = db.Column(db.String(20))
    description = db.Column(db.String(200))
    copies = db.Column(db.Integer, default=1)
    isbn = db.Column(db.String(15), unique=True, index=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def save(self, data):
        '''Save/add a book'''
        User().check_user_is_admin()
        db.session.add(data)
        db.session.commit()
        return jsonify({"message": "Successfully created."}), 201
    
    @staticmethod
    def check_if_book_exists(book_id):
        '''Check if book exists, return error if not'''
        if Books().query.filter_by(id=book_id).count() is 0:
            return abort(404, 'Book does not exist')


    def delete(self, id):
        '''delete a book'''
        User().check_user_is_admin
        self.check_if_book_exists(id)
        book = Books().query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Successfully deleted."}), 200

    def get_by_id(self, book_id):
        '''Function for retriving a book by its Id'''
        self.check_if_book_exists(book_id)
        item = Books().query.filter_by(id=book_id).first()
        book = self.book_item_dictionary(item)
        return jsonify(book), 200

    def get_all(self, page, per_page):
        '''Function for retrieving all books'''
        books = Books().query.order_by(Books.id.asc()).paginate(
            page,
            per_page,
            error_out=True)
        books_list = []
        for item in books.items:
            book = self.book_item_dictionary(item)
            books_list.append(book)
        return jsonify(books_list), 200

    def add_book(self, title, author, date_published, genre, description, isbn, copies, date_created):
        '''Function for adding a user'''
        User().check_user_is_admin()
        if Books().query.filter_by(isbn=isbn).count() != 0:
            return jsonify({'message': 'Book exists, please got edit it..'}), 409
        else:
            new_book = Books(
                title=title,
                author=author,
                date_published=date_published,
                genre=genre,
                description=description,
                isbn=isbn,
                copies=copies,
                date_created=date_created)
            self.save(new_book)
            return jsonify(
                {"message": "%s by %s has been added to library" % (title, author)}),201

    def edit_book(self, title, book_id, author, date_published, genre, description, copies, isbn):
        '''Function for editing a book'''
        User().check_user_is_admin()
        self.check_if_book_exists(book_id)
        book = Books().query.filter_by(id=book_id).first()
        if book.isbn != isbn:
            if Books().query.filter_by(isbn=isbn).count() is not 0:
                return jsonify({"message": "Cannot create a duplicate ISBN"}), 200
        fields = {
            'title': title,
            'id': book_id,
            'author': author,
            'genre': genre,
            'description': description,
            'copies': copies,
            'isbn': isbn
        }
        #edit fields with data only
        for key in fields:
            if fields[key] is not None:
                if HelloBooks().edit_book_validation({'%s' % key : fields[key]}) is True:
                    setattr(book, key, fields[key])
                else:
                    return jsonify(
                        {'message': 'Please enter %s correctly.' % key}), 200
        #edit the date
        if date_published is not None:
            if HelloBooks().date_validate(date_published) is True:
                book.date_published = date_published
            else:
                return jsonify(
                    {'message': 'Please enter a correct date format DD/MM/YYYY'}), 400
        book.date_modified = datetime.datetime.now()
        db.session.commit()
        return jsonify({"message": "Successfully edited %s" % book.title}), 201

    def book_item_dictionary(self, item):
        '''Return a dictionary of book details'''
        return {
            "id": item.id,
            "title": item.title,
            "author": item.author,
            "date_published": item.date_published,
            "genre": item.genre,
            "description": item.description,
            "copies": item.copies,
            "isbn": item.isbn
        }
