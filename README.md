\---

title: Tetra Master Probability Simulator

emoji: 🎴

colorFrom: blue

colorTo: purple

sdk: gradio

sdk\_version: 4.44.0

app\_file: app.py

pinned: false

\---

\# Tetra Master Win Probability Simulator

A Monte Carlo simulator for the card-battle mini-game in Final Fantasy IX. Players have always had to guess which card matchups favor them — this tool runs 10,000 simulated battles and reports the empirical win rate.

\## What it does

Each Tetra Master card has four hex-encoded stats: Power, Attack Type, Physical Defense, and Magic Defense. Battle outcomes depend on:

1\. A random roll from the attacker's Power range

2\. A random penalty subtracted from that roll (FF9's hidden degradation mechanic)

3\. The same process applied to the defender's relevant defense stat — \*which\* defense stat is used depends on the attacker's class:

&#x20;  - \*\*P (Physical)\*\* — uses defender's Physical Defense

&#x20;  - \*\*M (Magical)\*\* — uses defender's Magic Defense

&#x20;  - \*\*X (Flexible)\*\* — uses the lower of Physical or Magic Defense

&#x20;  - \*\*A (All)\*\* — uses the lowest of Power, Physical, or Magic Defense

The branching logic makes win probability hard to estimate by inspection. Monte Carlo simulation cuts through it.

\## How to use

Enter two 4-character cards (for example: `9P8A` vs `6MA3`) and click \*\*Run Simulation\*\*. The app runs 10,000 battles and reports the empirical win rate, with a sample of 100 individual battles shown in a table below.

The \*\*Swap\*\* button reverses attacker and defender — useful for checking matchup symmetry, since which side attacks affects the outcome.

\## Why 10,000 trials?

10,000 trials gives roughly a 1% margin of error on the win rate at the 95% confidence level. That's plenty of precision for player decisions, and it runs in well under a second.

\## Run locally

```bash

pip install -r requirements.txt

python app.py

```

Then open the local URL Gradio prints to your terminal.

## Source

Game mechanics and stat formulas referenced from the [Final Fantasy Wiki's Tetra Master entry](https://finalfantasy.fandom.com/wiki/Tetra_Master_(minigame)), which compiles community-verified data mining and decompilation of the original game logic.

## Tech

Python · Gradio · pandas · Monte Carlo simulation


