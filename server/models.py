from flask_sqlalchemy import SQLAlchemy
import re
from sqlalchemy.orm import validates
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates ('name')
    def validate_name(self, key,name):
        if len(name)==0:
            raise ValueError("Author must have a non-empty name")

        existing_person = Author.query.filter_by(name=name).first()
        if existing_person:
            raise ValueError("Author's name must be unique.")
        return name
        
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not re.match(r'^\d{10}$', phone_number):
            raise ValueError("Phone number must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def content_lenght(self,key,content):
        if len(content) < 250:
            raise ValueError("Content should be more than 250 characters")
        return content
    
    @validates('summary')
    def summary_length(self, key, summary):
        if len(summary)>250:
            raise ValueError("Summary should not exceed 250 characters")
        return summary
    @validates('title')
    def title_validation(self,key,title):
        most_phrase =["Won't Believe","Secret","Top","Guess"]
        if not any(phrase in title for phrase in most_phrase):
            raise ValueError("Title should contain one of the following words:\n{}".format(', '.join(most_phrase)))
        return title

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
