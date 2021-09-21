def configure(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///clothes.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = b'\xc36@\xa8\x80\x0bWO\x04\xb7\xdc\xc8\xdd3\xa4\xa2\xe9\xaeV\x0bd\xf9\x98\xde'
