import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import scipy.optimize

# Define strategies with emojis
strategies = ['🤝 Cooperate', '🚫 Defect']


def utility_function(a, b, c, d):
    """
    Compute the payoff matrix based on user-defined integer utility values.
    Matrix format:
       [ [(a, a), (b, c)],
         [(c, b), (d, d)] ]
    """
    return np.array([
        [(a, a),  # AI Stability & Advancement
         (b, c)],  # Exploited Trust
        [(c, b),  # Strategic Edge, Lost Trust
         (d, d)]  # AI Arms Race & Fragmentation
    ], dtype=int)


def find_mixed_strategy_nash(payoff_matrix):
    """
    Solve for mixed-strategy Nash equilibrium using linear programming.
    This is unchanged; it can still work with integer payoffs.
    """
    A = np.array(payoff_matrix[:, :, 0], dtype=float)
    B = np.array(payoff_matrix[:, :, 1], dtype=float)

    def nash_obj(x):
        # Negative min of (A @ x) for a zero-sum approach
        return -np.min(A @ x)

    cons = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        {'type': 'ineq', 'fun': lambda x: x}
    ]

    from scipy.optimize import minimize
    res = minimize(nash_obj, np.array([0.5, 0.5]), constraints=cons)

    return res.x if res.success else None


# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Stag Hunt Game (Integer Payoffs)"

app.layout = html.Div([
    html.H1("Stag Hunt Game: US-China AI Policy (Integer Only)",
            style={'textAlign': 'center', 'fontSize': '32px'}),

    html.P("Adjust the integer parameters (0 to 4) for the payoff matrix and see how the equilibrium changes.",
           style={'textAlign': 'center', 'fontSize': '16px'}),

    # Sliders for integer payoff parameters
    html.Div([
        html.Label("a (max 4)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-a', min=0, max=4, step=1, value=4,
                   marks={i: str(i) for i in range(5)}),

        html.Label("b (max 4)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-b', min=0, max=4, step=1, value=0,
                   marks={i: str(i) for i in range(5)}),

        html.Label("c (max 4)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-c', min=0, max=4, step=1, value=3,
                   marks={i: str(i) for i in range(5)}),

        html.Label("d (max 4)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-d', min=0, max=4, step=1, value=3,
                   marks={i: str(i) for i in range(5)}),

        html.Button("Update Payoff Matrix", id='update-button', n_clicks=0)
    ], style={'margin': '20px'}),

    html.Label("Mixed Strategy Nash Equilibrium:", style={'fontSize': '18px', 'fontWeight': 'bold'}),
    html.Div(id='mixed-strategy-output', style={'marginBottom': '20px', 'fontSize': '16px'}),

    dcc.Graph(id='payoff-heatmap', config={'displayModeBar': False})
], style={'padding': '20px', 'backgroundColor': '#f9f9f9'})


@app.callback(
    [Output('payoff-heatmap', 'figure'),
     Output('mixed-strategy-output', 'children')],
    [Input('update-button', 'n_clicks')],
    [State('input-a', 'value'),
     State('input-b', 'value'),
     State('input-c', 'value'),
     State('input-d', 'value')]
)
def update_heatmap(_, a, b, c, d):
    payoff_matrix = utility_function(a, b, c, d)

    # Calculate mixed-strategy equilibrium (if any)
    mixed_strategy = find_mixed_strategy_nash(payoff_matrix)
    if mixed_strategy is not None:
        mixed_str_output = f"China: {mixed_strategy[0]:.2f}, US: {mixed_strategy[1]:.2f}"
    else:
        mixed_str_output = "No Mixed Strategy Nash Equilibrium Found"

    # Sum of payoffs for color scale
    z = payoff_matrix[:, :, 0] + payoff_matrix[:, :, 1]
    z_norm = (z - z.min()) / (z.max() - z.min()) if (z.max() - z.min()) != 0 else z

    trace = go.Heatmap(
        z=z_norm,
        x=strategies,
        y=strategies,
        text=[[f"China Payoff: {payoff_matrix[i, j, 0]}\nUS Payoff: {payoff_matrix[i, j, 1]}"
               for j in range(2)] for i in range(2)],
        hoverinfo='text',
        colorscale='Blues',
        showscale=False
    )

    fig = go.Figure(data=[trace])
    fig.update_layout(
        title='Payoff Matrix: US-China AI Policy (Payoffs Matrix)',
        xaxis=dict(title='US Strategies', tickvals=[0, 1], ticktext=strategies, side='top'),
        yaxis=dict(title='China Strategies', tickvals=[0, 1], ticktext=strategies, autorange='reversed')
    )

    return fig, mixed_str_output


if __name__ == '__main__':
    app.run_server(debug=True)
