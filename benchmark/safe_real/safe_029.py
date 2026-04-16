# source: RedashSafe / redash/cli/__init__.py
# function: create

def create():
    app = current_app or create_app()

    @app.shell_context_processor
    def shell_context():
        from redash import models, settings

        return {"models": models, "settings": settings}

    return app