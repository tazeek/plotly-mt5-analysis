import dash_core_components as dcc
import dash_html_components as html

def _generate_dropdown():

    forex_list = ['GBPUSD','EURGBP','EURUSD','AUDUSD','AUDJPY','USDJPY']

    dropdown_options = [{'label': currency, 'value': currency} for currency in forex_list]
    print(dropdown_options)

    return html.Div([
        dcc.Dropdown(
            id='currency-dropdown',
            options=dropdown_options,
            value='GBPUSD'
        )
    ])

def generate_layout():

    _generate_dropdown()
    
    return html.Div([
        html.H1(children='Hello World')
    ])