from layout import generate_layout

import dash

app = dash.Dash(title='MT5 Analyzer')
app.layout = generate_layout

if __name__ == '__main__':

	app.run_server(debug=True)