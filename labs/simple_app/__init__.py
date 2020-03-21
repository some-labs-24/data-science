from .app import create_app

APP = create_app()
APP.run(debug=True,port=5000)