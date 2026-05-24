from flask import Flask

from routes.auth_stub import auth_bp

app = Flask(__name__)

# Register stubs
app.register_blueprint(auth_bp)


@app.route("/")
def health():

    return {
        "message": "Mock server running"
    }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=3001,
        debug=True
    )