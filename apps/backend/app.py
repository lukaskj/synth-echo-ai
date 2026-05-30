from tts_backend import create_app, get_model_service
from tts_backend.lifecycle import register_shutdown_handlers


app = create_app()
register_shutdown_handlers(get_model_service(app))


def main() -> None:
    app.run(host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
