from controller.controller import register_callbacks
from layout.layout import generate_layout

import dash

app = dash.Dash(title='MT5 Analyzer')
app.layout = generate_layout
register_callbacks(app)

if __name__ == '__main__':

	app.run_server(debug=True)