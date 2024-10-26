import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# Define strategies with emojis
strategies = ['🤝 Cooperate', '🚫 Defect']

# Map qualitative payoffs to numerical values
payoff_mapping = {'High': 4, 'Medium': 3, 'Low': 1}

# Define the payoff matrix based on your descriptions
payoff_matrix = np.array([
    [(payoff_mapping['High'], payoff_mapping['High']),   # Both Cooperate
     (payoff_mapping['Low'], payoff_mapping['Medium'])], # China Cooperates, US Defects
    [(payoff_mapping['Medium'], payoff_mapping['Low']),  # China Defects, US Cooperates
     (payoff_mapping['Low'], payoff_mapping['Low'])]     # Both Defect
])

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Stag Hunt Game: China vs US on AI Policy"

# Define the app layout
app.layout = html.Div([
    html.H1("Stag Hunt Game: China vs US on AI Policy",
            style={'textAlign': 'center', 'fontFamily': 'Arial', 'margin-top': '20px', 'fontSize': '32px'}),

    html.Div([
        html.P(
            "This visualization represents the strategic interactions between China and the US regarding AI policy, focusing on cooperation and defection strategies. Hover over each cell to see detailed payoffs and outcome descriptions.",
            style={'textAlign': 'center', 'fontFamily': 'Arial', 'fontSize': '16px', 'maxWidth': '800px', 'margin': 'auto', 'lineHeight': '1.6'}
        )
    ], style={'margin-bottom': '40px'}),

    dcc.Graph(id='payoff-heatmap', config={'displayModeBar': False})
], style={'backgroundColor': '#f9f9f9', 'padding': '20px'})

@app.callback(
    Output('payoff-heatmap', 'figure'),
    Input('payoff-heatmap', 'id')  # Dummy input to trigger the callback
)
def update_heatmap(_):
    china_payoffs = payoff_matrix[:, :, 0]
    us_payoffs = payoff_matrix[:, :, 1]

    # Descriptions for each outcome
    descriptions = [
        ["Alignment on privacy standards, reduced risks of surveillance misuse, shared AI advancements.",
         "China cooperates, but the US independently advances AI capabilities, prioritizing national gains."],
        ["The US focuses on collaboration, but China exploits this by advancing its surveillance capabilities.",
         "Both prioritize national goals, risking privacy violations and a surveillance arms race."]
    ]

    hover_text = []
    annotations = []
    for i in range(len(strategies)):
        for j in range(len(strategies)):
            china_strategy = strategies[i]
            us_strategy = strategies[j]
            china_payoff = payoff_matrix[i, j, 0]
            us_payoff = payoff_matrix[i, j, 1]
            description = descriptions[i][j]
            hovertext = f"<span style='font-size:16px;'><b>China Strategy:</b> {china_strategy}<br>" \
                        f"<b>US Strategy:</b> {us_strategy}<br><br>" \
                        f"<b>China Payoff:</b> {china_payoff}<br>" \
                        f"<b>US Payoff:</b> {us_payoff}<br><br>" \
                        f"{description}</span>"
            hover_text.append(hovertext)

            # Add annotations to each cell
            annotations.append(dict(
                x=j,
                y=i,
                text=f"<b>{china_payoff}, {us_payoff}</b>",
                showarrow=False,
                font=dict(color='white', size=14),  # Reduced size
                xanchor='center',
                yanchor='middle'
            ))

    # Reshape hover_text to match the shape of the heatmap
    hover_text = np.array(hover_text).reshape((len(strategies), len(strategies)))

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

    # Find Nash equilibria
    nash_equilibria = []
    for i in range(len(strategies)):
        for j in china_best_responses[i]:
            if i in us_best_responses[j]:
                nash_equilibria.append((i, j))

    # Create shapes to highlight Nash equilibria
    shapes = []
    for eq in nash_equilibria:
        i, j = eq
        shapes.append(dict(
            type='rect',
            x0=j - 0.5,
            y0=i - 0.5,
            x1=j + 0.5,
            y1=i + 0.5,
            line=dict(color='#FFD700', width=4),
            fillcolor='rgba(0,0,0,0)'
        ))

    colorscale = [
        [0.0, '#002525'],  # Low payoff
        [0.5, '#0D98BA'],  # Medium payoff
        [1.0, '#008B8B']   # High payoff
    ]

    # Normalize z-values for colorscale mapping
    z = china_payoffs + us_payoffs
    z_min, z_max = z.min(), z.max()
    z_norm = (z - z_min) / (z_max - z_min)

    trace = go.Heatmap(
        z=z_norm,
        x=[s for s in strategies],
        y=[s for s in strategies],
        text=hover_text,
        hoverinfo='text',
        colorscale=colorscale,
        showscale=False
    )

    layout = go.Layout(
        title={'text': 'Payoff Matrix: China vs US on AI Policy', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}},
        xaxis=dict(
            title='US Strategies',
            tickmode='array',
            tickvals=[0, 1],
            ticktext=[s for s in strategies],
            side='top',
            ticks='',
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title='China Strategies',
            tickmode='array',
            tickvals=[0, 1],
            ticktext=[s for s in strategies],
            ticks='',
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(size=16),
            autorange='reversed'
        ),
        shapes=shapes,
        annotations=annotations,
        margin=dict(l=150, r=150, b=100, t=150),  # Increased margins
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='#f9f9f9',
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

