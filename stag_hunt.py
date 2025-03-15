import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import random
import scipy.optimize

# Define strategies with emojis
strategies = ['🤝 Cooperate', '🚫 Defect']

# AI decision-making weights (AI slightly favors cooperation)
ai_decision_weights = [0.6, 0.4]

# Global variables for scores, achievements, and streaks
user_score = 0
ai_score = 0
achievements = []
cooperate_streak = 0
defect_streak = 0


def utility_function(a, b, c, d):
    """
    Compute the payoff matrix based on integer utility values (0 to 4).
    Matrix format:
       [ [(a, a), (b, c)],
         [(c, b), (d, d)] ]
    """
    return np.array([
        [(a, a),  # (Cooperate, Cooperate)
         (b, c)],  # (Cooperate, Defect)
        [(c, b),  # (Defect, Cooperate)
         (d, d)]  # (Defect, Defect)
    ], dtype=int)


def find_mixed_strategy_nash(payoff_matrix):
    """
    Solve for a mixed-strategy Nash equilibrium using linear programming.
    """
    A = np.array(payoff_matrix[:, :, 0], dtype=float)

    def nash_obj(x):
        # Minimizes the negative of min(A @ x).
        return -np.min(A @ x)

    cons = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        {'type': 'ineq', 'fun': lambda x: x}
    ]

    from scipy.optimize import minimize
    res = minimize(nash_obj, np.array([0.5, 0.5]), constraints=cons)
    return res.x if res.success else None


app = dash.Dash(__name__)
app.title = "Stag Hunt: US-China AI Policy"

app.layout = html.Div([
    html.H1("Stag Hunt: US-China AI Policy", style={'textAlign': 'center', 'fontSize': '32px'}),

    html.P(
        "Tired of all the serious talk about AI policy? "
        "Make your move, and see if you can outwit the cunning 'AI opponent' as you juggle US-China cooperation or conflict. "
        "Can you build trust and synergy, or will everything descend into an AI arms race? It's your call!",
        style={'textAlign': 'center', 'fontSize': '16px'}
    ),

    # Strategy selection and scenario feedback
    html.Div([
        html.Label("Your Strategy:", style={'fontSize': '18px', 'fontWeight': 'bold'}),
        dcc.RadioItems(
            id='user-strategy',
            options=[{'label': s, 'value': i} for i, s in enumerate(strategies)],
            value=0,
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        ),
        html.Button("Submit Strategy", id='submit-strategy', n_clicks=0),
        html.Div(id="game-feedback", style={'marginTop': '10px', 'fontSize': '16px', 'fontWeight': 'bold'}),
    ], style={'margin': '20px'}),

    # Payoff matrix controls
    html.Div([
        html.Label("Utility Function Parameters (0 to 4):", style={'fontSize': '18px', 'fontWeight': 'bold'}),
        html.Label("a (Coop–Coop Payoff)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-a', min=0, max=4, step=1, value=4, marks={i: str(i) for i in range(5)}),
        html.Label("b (US Coop, China Defect)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-b', min=0, max=4, step=1, value=0, marks={i: str(i) for i in range(5)}),
        html.Label("c (US Defect, China Coop)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-c', min=0, max=4, step=1, value=3, marks={i: str(i) for i in range(5)}),
        html.Label("d (Defect–Defect Payoff)", style={'fontSize': '16px'}),
        dcc.Slider(id='input-d', min=0, max=4, step=1, value=3, marks={i: str(i) for i in range(5)}),
        html.Button("Update Payoff Matrix", id='update-button', n_clicks=0)
    ], style={'margin': '20px'}),

    html.Label("Mixed-Strategy Nash Equilibrium:", style={'fontSize': '18px', 'fontWeight': 'bold'}),
    html.Div(id='mixed-strategy-output', style={'marginBottom': '20px', 'fontSize': '16px'}),

    dcc.Graph(id='payoff-heatmap', config={'displayModeBar': False}),

    # Scoreboard
    html.Div([
        html.H3("Scoreboard"),
        html.Div(id="score-output", style={'fontSize': '18px', 'fontWeight': 'bold'})
    ], style={'marginTop': '20px', 'textAlign': 'center'}),

    # Achievements
    html.Div([
        html.H3("Achievements Unlocked"),
        html.Div(id="achievement-output", style={'fontSize': '16px', 'fontWeight': 'bold'})
    ], style={'marginTop': '20px', 'textAlign': 'center'})
], style={'padding': '20px', 'backgroundColor': '#f9f9f9'})


# Update the payoff matrix graph and Nash equilibrium
@app.callback(
    [Output('payoff-heatmap', 'figure'),
     Output('mixed-strategy-output', 'children')],
    [Input('update-button', 'n_clicks')],
    [State('input-a', 'value'),
     State('input-b', 'value'),
     State('input-c', 'value'),
     State('input-d', 'value')]
)
def update_heatmap(n_clicks, a, b, c, d):
    payoff_matrix = utility_function(a, b, c, d)

    mixed_strategy = find_mixed_strategy_nash(payoff_matrix)
    if mixed_strategy is not None:
        mixed_str_output = f"China: {mixed_strategy[0]:.2f}, US: {mixed_strategy[1]:.2f}"
    else:
        mixed_str_output = "No Mixed Strategy Nash Equilibrium Found"

    # Combine payoffs for color scale
    z = payoff_matrix[:, :, 0] + payoff_matrix[:, :, 1]
    z_norm = (z - z.min()) / (z.max() - z.min()) if z.max() != z.min() else z

    trace = go.Heatmap(
        z=z_norm,
        x=strategies,
        y=strategies,
        text=[[
            f"China: {payoff_matrix[i, j, 0]} | US: {payoff_matrix[i, j, 1]}"
            for j in range(2)
        ] for i in range(2)],
        hoverinfo='text',
        colorscale='Blues',
        showscale=False
    )

    fig = go.Figure(data=[trace])
    fig.update_layout(
        title='Payoff Matrix: Witty Stag Hunt',
        xaxis=dict(title='US Strategies', tickvals=[0, 1], ticktext=strategies, side='top'),
        yaxis=dict(title='China Strategies', tickvals=[0, 1], ticktext=strategies, autorange='reversed')
    )

    return fig, mixed_str_output


# Submit strategy -> witty outcome, updated scores, achievements
@app.callback(
    [Output("game-feedback", "children"),
     Output("score-output", "children"),
     Output("achievement-output", "children")],
    [Input("submit-strategy", "n_clicks")],
    [State("user-strategy", "value")]
)
def play_game(n_clicks, user_choice):
    global user_score, ai_score, achievements, cooperate_streak, defect_streak

    # AI picks strategy
    ai_choice = np.random.choice([0, 1], p=ai_decision_weights)

    # Basic outcome text
    result_message = f"You chose {strategies[user_choice]}, Melanie chose {strategies[ai_choice]}. "

    # Witty scenarios:
    if user_choice == 0 and ai_choice == 0:
        # Both cooperate
        narrative = (
            "It's a diplomatic lovefest! You both sign a 'No More GPU Hoarding' pact. "
            "Global headlines proclaim: 'US & China Besties at Last!'"
        )
        user_score += 3
        ai_score += 3
    elif user_choice == 1 and ai_choice == 1:
        # Both defect
        narrative = (
            "Cue the fireworks of rivalry! Both sides ramp up AI arms spending faster than you can say 'data breach.' "
            "At least GPU stocks are booming."
        )
        user_score += 2
        ai_score += 2
    elif user_choice == 0 and ai_choice == 1:
        # You cooperate, AI defects
        narrative = (
            "Ouch—China just swooped up your best AI talent while you wrote the warm-and-fuzzy treaty. "
            "Looks like someone took advantage of your goodwill."
        )
        user_score += 1
        defect_streak = 0
    elif user_choice == 1 and ai_choice == 0:
        # You defect, AI cooperates
        narrative = (
            "You snag the next big AI breakthrough while your cooperative partner politely waits. "
            "Short-term gains could cost your reputation, but hey—NVIDIA shares are going through the roof!"
        )
        ai_score += 1
        cooperate_streak = 0
    else:
        narrative = "Some cosmic glitch happened. Maybe the simulation is too witty for its own good."

    # Track streaks
    if user_choice == 0:  # Cooperate
        cooperate_streak += 1
        defect_streak = 0
    else:  # Defect
        defect_streak += 1
        cooperate_streak = 0

    # Check achievements
    new_achievements = []

    # Example achievements
    if cooperate_streak >= 3 and "Diplomacy Champ" not in achievements:
        achievements.append("Diplomacy Champ")
        new_achievements.append("Diplomacy Champ")

    if defect_streak >= 3 and "Arms Race Fanatic" not in achievements:
        achievements.append("Arms Race Fanatic")
        new_achievements.append("Arms Race Fanatic")

    if user_score >= 15 and "AI Mogul" not in achievements:
        achievements.append("AI Mogul")
        new_achievements.append("AI Mogul")

    # Compose final feedback
    full_message = result_message + narrative
    score_message = f"Your Score: {user_score} | AI Score: {ai_score}"

    # Achievement text
    if achievements:
        achievement_text = "Achievements: " + ", ".join(achievements)
    else:
        achievement_text = "Achievements: (None yet)"

    return full_message, score_message, achievement_text


if __name__ == '__main__':
    app.run_server(debug=True)
