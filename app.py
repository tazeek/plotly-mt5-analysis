from layout import generate_layout

import dash

app = dash.Dash()
app.layout = generate_layout

if __name__ == '__main__':

	app.run_server(debug=True)