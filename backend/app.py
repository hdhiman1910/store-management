from flask import Flask

def create_app():

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Welcome to the Store Management Web Application!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)