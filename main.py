import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# Define strategies
strategies = ['Cooperate on AI Policy', 'Compete on AI Policy']

# Define multiple scenarios with different payoff matrices
scenarios = {
    'Mutual Cooperation': {
        'payoff_matrix': np.array([
            [(4, 4), (2, 5)],
            [(5, 2), (3, 3)]
        ]),
        'description': 'Both countries choose to cooperate, leading to high '
                       'mutual benefits.'
    },
    'One-Sided Cooperation': {
        'payoff_matrix': np.array([
            [(4, 4), (1, 6)],
            [(6, 1), (3, 3)]
        ]),
        'description': 'One country cooperates while the other competes, '
                       'leading to asymmetric payoffs.'
    },
    'Mutual Competition': {
        'payoff_matrix': np.array([
            [(3, 3), (2, 5)],
            [(5, 2), (4, 4)]
        ]),
        'description': 'Both countries choose to compete, leading to moderate '
                       'mutual benefits.'
    },
    'Balanced': {
        'payoff_matrix': np.array([
            [(3, 3), (2, 4)],
            [(4, 2), (3, 3)]
        ]),
        'description': 'A balanced scenario with moderate payoffs across '
                       'strategies.'
    },
    'Custom': {
        'payoff_matrix': np.array([
            [(4, 4), (2, 5)],
            [(5, 2), (3, 3)]
        ]),
        'description': 'Custom Scenario: Adjust payoffs using the sliders below.'
    }
}

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Stag Hunt Game: China vs US on AI Policy"

# Define the app layout
app.layout = html.Div([
    html.H1("Stag Hunt Game: China vs US on AI Policy",
            style={'textAlign': 'center', 'fontFamily': 'SanSerif'}),

    html.Div([
        html.Label("Select Scenario:", style={'fontSize': '20px'}),
        dcc.Dropdown(
            id='scenario-dropdown',
            options=[{'label': key, 'value': key} for key in scenarios.keys()],
            value='Mutual Cooperation',
            clearable=False,
            style={'width': '50%', 'fontSize': '18px', 'margin': 'auto'}
        ),
    ], style={'padding': '20px', 'textAlign': 'center'}),

    html.Div(id='scenario-description',
             style={'padding': '20px', 'fontSize': '18px',
                    'textAlign': 'center'}),

    dcc.Graph(id='payoff-heatmap'),

    html.Div([
        html.H2("Adjust Payoffs (Custom Scenario)",
                style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.Label("China Cooperates vs US Cooperates:",
                           style={'fontSize': '16px'}),
                dcc.Slider(
                    id='cc-slider',
                    min=1,
                    max=10,
                    step=1,
                    value=4,
                    marks={i: str(i) for i in range(1, 11)},
                    tooltip={"placement": "bottom",
                             "always_visible": True}
                ),
            ], style={'padding': '10px'}),

            html.Div([
                html.Label("China Cooperates vs US Competes:",
                           style={'fontSize': '16px'}),
                dcc.Slider(
                    id='cc-slider-2',
                    min=1,
                    max=10,
                    step=1,
                    value=2,
                    marks={i: str(i) for i in range(1, 11)},
                    tooltip={"placement": "bottom",
                             "always_visible": True}
                ),
            ], style={'padding': '10px'}),

            html.Div([
                html.Label("China Competes vs US Cooperates:",
                           style={'fontSize': '16px'}),
                dcc.Slider(
                    id='cc-slider-3',
                    min=1,
                    max=10,
                    step=1,
                    value=5,
                    marks={i: str(i) for i in range(1, 11)},
                    tooltip={"placement": "bottom",
                             "always_visible": True}
                ),
            ], style={'padding': '10px'}),

            html.Div([
                html.Label("China Competes vs US Competes:",
                           style={'fontSize': '16px'}),
                dcc.Slider(
                    id='cc-slider-4',
                    min=1,
                    max=10,
                    step=1,
                    value=3,
                    marks={i: str(i) for i in range(1, 11)},
                    tooltip={"placement": "bottom",
                             "always_visible": True}
                ),
            ], style={'padding': '10px'}),
        ], style={'width': '80%', 'margin': 'auto'})
    ], style={'padding': '40px', 'display': 'none'},
        id='slider-container'),  # Initially hidden
])

@app.callback(
    Output('scenario-description', 'children'),
    Input('scenario-dropdown', 'value')
)
def update_description(selected_scenario):
    return scenarios[selected_scenario]['description']

@app.callback(
    [Output('payoff-heatmap', 'figure'),
     Output('slider-container', 'style')],
    [Input('scenario-dropdown', 'value'),
     Input('cc-slider', 'value'),
     Input('cc-slider-2', 'value'),
     Input('cc-slider-3', 'value'),
     Input('cc-slider-4', 'value')]
)
def update_heatmap(selected_scenario, cc, cc2, cc3, cc4):
    if selected_scenario == 'Custom':
        payoff_matrix = np.array([
            [(cc, cc), (cc2, 10 - cc2)],
            [(cc3, 10 - cc3), (cc4, cc4)]
        ])
    else:
        payoff_matrix = scenarios[selected_scenario]['payoff_matrix']

    china_payoffs = payoff_matrix[:, :, 0]
    us_payoffs = payoff_matrix[:, :, 1]

    hover_text = []
    for i in range(payoff_matrix.shape[0]):
        row = []
        for j in range(payoff_matrix.shape[1]):
            row.append(f"China: {payoff_matrix[i, j, 0]}"
                       f"<br>US: {payoff_matrix[i, j, 1]}")
        row.append('')
        hover_text.append(row)

    # Determine best responses
    china_best_responses = []
    for i in range(len(strategies)):
        payoffs = payoff_matrix[i, :, 0]
        max_payoff = np.max(payoffs)
        best_actions = np.where(payoffs == max_payoff)[0]
        china_best_responses.append(best_actions)

    us_best_responses = []
    for j in range(len(strategies)):
        payoffs = payoff_matrix[:, j, 1]
        max_payoff = np.max(payoffs)
        best_actions = np.where(payoffs == max_payoff)[0]
        us_best_responses.append(best_actions)

    nash_equilibria = []
    for i in range(len(strategies)):
        for j in china_best_responses[i]:
            if i in us_best_responses[j]:
                nash_equilibria.append((i, j))

    # Create shapes for Nash equilibria
    shapes = []
    for eq in nash_equilibria:
        i, j = eq
        shapes.append(dict(
            type='rect',
            x0=j - 0.5,
            y0=i - 0.5,
            x1=j + 0.5,
            y1=i + 0.5,
            line=dict(color='gold', width=4),
            fillcolor='rgba(0,0,0,0)'
        ))

    trace = go.Heatmap(
        z=china_payoffs + us_payoffs,
        x=strategies,
        y=strategies,
        text=hover_text,
        hoverinfo='text',
        colorscale='Viridis',
        showscale=False
    )

    data = [trace]

    layout = go.Layout(
        title='Payoff Matrix: China vs US on AI Policy',
        xaxis=dict(
            title='US Strategies',
            tickfont=dict(size=12),
            ticks='',
            side='top'
        ),
        yaxis=dict(
            title='China Strategies',
            tickfont=dict(size=12),
            ticks='',
            autorange='reversed'
        ),
        shapes=shapes,
        margin=dict(l=100, r=100, b=50, t=100),
        hovermode='closest',
        plot_bgcolor='white',
    )

    fig = go.Figure(data=data, layout=layout)

    slider_style = {'display': 'block'} if selected_scenario == 'Custom' else {'display': 'none'}

    return fig, slider_style

if __name__ == '__main__':
    app.run_server(debug=True)

