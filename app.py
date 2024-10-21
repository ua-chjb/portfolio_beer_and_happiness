from dash import Dash

from index import lyt
from callbacks import callbacks_baby

app = Dash(__name__)

app.layout = lyt

callbacks_baby(app)

if __name__ == "__main__":
    app.run_server(debug=True, port="8080")