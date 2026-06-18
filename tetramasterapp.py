"""
Tetra Master Win Probability Simulator
--------------------------------------
A Monte Carlo simulator for the Tetra Master card game from Final Fantasy IX.
Each card has 4 hex-encoded stats (Power, Attack Type, Physical Defense, Magic Defense).
Battle outcomes are non-trivial because the defense stat used depends on the attacker's
type, and FF9 reduces each rolled stat by a random penalty from 0 to base value.

This simulator runs 10,000 battles per matchup and reports the empirical win rate.
"""

import random
import pandas as pd
import gradio as gr


# Convert a hex character (0–F) to its numeric stat range.
# FF9 stores stats in 16-value bands, so hex digit N maps to N*16 .. N*16+15.
def hexrange(char: str) -> tuple[int, int]:
    value = int(char, 16)
    return value * 16, value * 16 + 15


# Roll a stat, then subtract a random penalty (FF9's hidden degradation mechanic).
# The penalty represents the way the game effectively "rolls twice" against you.
def roll_stat(min_val: int, max_val: int) -> tuple[int, int, int]:
    base = random.randint(min_val, max_val)
    penalty = random.randint(0, base)
    return base - penalty, base, penalty


def avg(rng: tuple[int, int]) -> float:
    return (rng[0] + rng[1]) / 2


# Pick which defense stat applies based on the attacker's class.
# P = Physical, M = Magical, X = Flexible (uses lower of P/M), A = All (lowest of all three).
def select_defense(attacker_type: str, defender: str) -> tuple[tuple[int, int], str]:
    pwr_val = hexrange(defender[0])
    pd_val = hexrange(defender[2])
    md_val = hexrange(defender[3])

    if attacker_type == "P":
        return pd_val, "Physical"
    elif attacker_type == "M":
        return md_val, "Magical"
    elif attacker_type == "X":
        return (pd_val if avg(pd_val) < avg(md_val) else md_val), "Lowest of P/M"
    elif attacker_type == "A":
        return min([pwr_val, pd_val, md_val], key=avg), "Lowest of A/P/M"
    else:
        raise ValueError(f"Invalid attack type: {attacker_type}")


# Simulate one battle round.
def simulate_battle(attacker: str, defender: str) -> dict:
    atk_min, atk_max = hexrange(attacker[0])
    atk_final, atk_base, atk_penalty = roll_stat(atk_min, atk_max)

    (def_min, def_max), _ = select_defense(attacker[1], defender)
    def_final, def_base, def_penalty = roll_stat(def_min, def_max)

    return {
        "Result": "Win" if atk_final > def_final else "Lose",
        "Dif": f"+{atk_final - def_final}" if atk_final > def_final else f"{atk_final - def_final}",
        "Score": f"{atk_final} vs {def_final}",
        f"Attacker: {attacker}": f"{atk_base} - {atk_penalty} = {atk_final}",
        f"Defender: {defender}": f"{def_base} - {def_penalty} = {def_final}",
    }


# Run many simulations and return win rate plus a sample of battle outcomes.
def run_simulation(attacker: str, defender: str, count: int = 10000):
    attacker = attacker.strip().upper()
    defender = defender.strip().upper()
    if len(attacker) != 4 or len(defender) != 4:
        return "⚠️ Please enter valid 4-character cards like 9P8A.", pd.DataFrame()

    wins = 0
    samples = []
    for i in range(count):
        result = simulate_battle(attacker, defender)
        if result["Result"] == "Win":
            wins += 1
        if i < 100:
            samples.append(result)

    df = pd.DataFrame(samples)
    percent = round((wins / count) * 100, 2)
    return f"🧮 Win chance for {attacker} vs {defender}: {percent}%", df


def swap_and_run(attacker: str, defender: str):
    return run_simulation(defender, attacker) + (defender, attacker)


# Gradio UI
CSS = """
body, .gradio-container {
  background: linear-gradient(to left, rgba(70, 89, 220, 1), rgba(56, 44, 118, 1)) !important;
  min-height: 100vh;
  color: white;
}
h1, h2, h3, h4, h5, h6, p, .gr-markdown { color: white; }
"""

with gr.Blocks(css=CSS) as app:
    gr.Markdown("## 🎴 Tetra Master Win Probability Simulator")
    gr.Markdown("Enter two 4-character cards (e.g. `9P8A`, `6MA3`) to simulate 10,000 battles.")

    with gr.Row():
        attacker = gr.Textbox(label="Attacker Card")
        swap_btn = gr.Button("🔁 Swap")
        defender = gr.Textbox(label="Defender Card")

    run_btn = gr.Button("Run Simulation")
    output_text = gr.Textbox(label="Result (Top 100 samples shown below)", interactive=False)
    table = gr.Dataframe()

    run_btn.click(fn=run_simulation, inputs=[attacker, defender], outputs=[output_text, table])
    swap_btn.click(fn=swap_and_run, inputs=[attacker, defender], outputs=[output_text, table, attacker, defender])


if __name__ == "__main__":
    app.launch()