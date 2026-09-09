from pathlib import Path
import sqlite3

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots


PROJECT_DIR = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_DIR / "data" / "match_analysis.sqlite3"
CHART_PATH = (
    PROJECT_DIR
    / "reports"
    / "xg_difference_by_game_state.png"
)

RAW_TABLE = "events_raw"

    
def get_game_state(team_score, opponent_score):
    if team_score > opponent_score:
        return "winning"

    if team_score < opponent_score:
        return "losing"

    return "drawing"


def get_opponent_state(game_state):

    opposite_states = {
        "winning": "losing",
        "losing": "winning",
        "drawing": "drawing",
    }

    return opposite_states[game_state]


def load_unique_shots(connection):

    query = f"""
        SELECT DISTINCT
            id,
            "index" AS event_index,
            period,
            minute,
            second,
            team_name,
            player_name,
            statsbomb_xg,
            outcome_name
        FROM {RAW_TABLE}
        WHERE event_type_name = 'Shot'
        ORDER BY event_index
    """

    return pd.read_sql_query(query, connection)


def assign_game_states(shots):
    teams = shots["team_name"].drop_duplicates().tolist()

    scores = {
        teams[0]: 0,
        teams[1]: 0,
    }

    shot_records = []

    for shot in shots.itertuples(index=False):
        shooting_team = shot.team_name

        opponent = next(
            team for team in teams
            if team != shooting_team
        )

        team_score_before = scores[shooting_team]
        opponent_score_before = scores[opponent]

        game_state = get_game_state(
            team_score_before,
            opponent_score_before,
        )

        shot_records.append(
            {
                "event_id": shot.id,
                "event_index": shot.event_index,
                "period": shot.period,
                "minute": shot.minute,
                "second": shot.second,
                "team_name": shooting_team,
                "opponent_name": opponent,
                "player_name": shot.player_name,
                "statsbomb_xg": shot.statsbomb_xg,
                "outcome_name": shot.outcome_name,
                "team_score_before": team_score_before,
                "opponent_score_before": opponent_score_before,
                "game_state": game_state,
                "opponent_game_state": get_opponent_state(game_state),
            }
        )

        if shot.outcome_name == "Goal":
            scores[shooting_team] += 1

    return pd.DataFrame(shot_records)


def calculate_xg_difference(shot_states):
    
    teams = shot_states["team_name"].drop_duplicates().tolist()
    game_states = ["drawing", "winning", "losing"]

    results = []

    for team in teams:
        for game_state in game_states:
            team_shots = shot_states[
                (shot_states["team_name"] == team)
                & (shot_states["game_state"] == game_state)
            ]

            opponent_shots = shot_states[
                (shot_states["opponent_name"] == team)
                & (
                    shot_states["opponent_game_state"]
                    == game_state
                )
            ]

            xg_for = team_shots["statsbomb_xg"].sum()
            xg_against = opponent_shots["statsbomb_xg"].sum()

            results.append(
                {
                    "team_name": team,
                    "game_state": game_state,
                    "shots_for": len(team_shots),
                    "shots_against": len(opponent_shots),
                    "xg_for": xg_for,
                    "xg_against": xg_against,
                    "xg_difference": xg_for - xg_against,
                }
            )

    return pd.DataFrame(results)

def display_xg_chart(results):

    game_states = [
        ("losing", "LOSING"),
        ("drawing", "DRAWING"),
        ("winning", "WINNING"),
    ]

    team_colors = {
        "Pogoń Grodzisk Mazowiecki": "#D62828",
        "Polonia Bytom": "#7B2CBF",
}

    teams = results["team_name"].drop_duplicates().tolist()

    fig = make_subplots(
        rows=1,
        cols=3,
        shared_yaxes=True,
        subplot_titles=[
            label for _, label in game_states
        ],
        horizontal_spacing=0.07,
    )

    max_difference = results["xg_difference"].abs().max()
    axis_limit = max_difference * 1.35

    for column_number, (game_state, label) in enumerate(
        game_states,
        start=1,
    ):
        state_data = results[
            results["game_state"] == game_state
        ]

        for team in teams:
            row = state_data[
                state_data["team_name"] == team
            ].iloc[0]

            difference = row["xg_difference"]

            fig.add_trace(
                go.Bar(
                    x=[difference],
                    y=[team],
                    orientation="h",
                    name=team,
                    legendgroup=team,
                    showlegend=column_number == 1,
                    marker_color=team_colors[team],
                    text=[f"{difference:+.3f}"],
                    textposition="outside",
                    cliponaxis=False,
                    customdata=[[
                        row["xg_for"],
                        row["xg_against"],
                        row["shots_for"],
                        row["shots_against"],
                    ]]
                ),
                row=1,
                col=column_number,
            )

        fig.add_vline(
            x=0,
            line_width=1,
            line_color="#777777",
            row=1,
            col=column_number,
        )

        fig.update_xaxes(
            range=[-axis_limit, axis_limit],
            tickformat="+.2f",
            zeroline=False,
            gridcolor="#E5E5E5",
            row=1,
            col=column_number,
        )

    fig.update_yaxes(
        autorange="reversed",
        title=None,
    )

    fig.update_layout(
        title={
            "text": (
                "<b>xG difference in each game state</b><br>"
                "<sup>"
                "Polonia Bytom 2–2 Pogoń Grodzisk Mazowiecki 22.08.2026"
                "</sup>"
            ),
            "x": 0.02,
            "xanchor": "left",
        },
        width=1200,
        height=500,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={
            "family": "Arial",
            "color": "#202333",
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.07,
            "xanchor": "right",
            "x": 1,
        },
        margin={
            "l": 210,
            "r": 60,
            "t": 130,
            "b": 70,
        },
        bargap=0.45,
    )

    fig.add_annotation(
        text="Expected goals difference",
        x=0.5,
        y=-0.15,
        xref="paper",
        yref="paper",
        showarrow=False,
    )
    
    fig.write_image(
    CHART_PATH,
    width=1200,
    height=500,
    scale=2,
)


def main():
    with sqlite3.connect(DATABASE_PATH) as connection:
        shots = load_unique_shots(connection)

        print(f"Total number of shots: {len(shots)}")

        shot_states = assign_game_states(shots)
        results = calculate_xg_difference(shot_states)

    print("\nxG Difference in each Game State:")
    print(results.round(3).to_string(index=False))
    display_xg_chart(results)


if __name__ == "__main__":
    main()
