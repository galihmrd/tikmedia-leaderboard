import sys

from api import create_app

app = create_app()

try:
    port = sys.argv[1]
except:
    port = 80

if __name__ == "__main__":
    app.run("0.0.0.0", port=port)
