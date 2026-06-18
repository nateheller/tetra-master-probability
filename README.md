---
title: Tetra Master Probability Simulator
emoji: 🎴
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
pinned: false
---

# Tetra Master Win Probability Simulator

A Monte Carlo simulator for the card-battle mini-game in Final Fantasy IX. Players have always had to guess which card matchups favor them. This tool runs 10,000 simulated battles and reports the empirical win rate.

## Why I built this

Tetra Master is famous among FF9 players for being opaque. Cards lose battles they statistically should have won, and the game offers no explanation; no rolled values, no formula, no probability shown. After enough seemingly-unfair losses, I wanted to know what was actually happening under the hood.

It turns out the game does a lot of hidden work for each battle: rolling within ranges, subtracting random penalties, picking which defense stat to use based on the attacker's class. None of that is visible to the player. The losses aren't bugs or bad luck in the way they feel, they're the result of probability distributions the game keeps hidden.

This simulator makes those distributions visible. Same rules, same math, just run thousands of times so you can see the actual odds.

## How Tetra Master works (briefly)

Tetra Master is a collectible card mini-game inside FF9. Each card has four stats, displayed as a 4-character hex code like `9P8A`:

- **First character: Power.** Used when the card attacks.
- **Second character: Attack Type.** One of `P` (Physical), `M` (Magical), `X` (Flexible), or `A` (All).
- **Third character: Physical Defense.**
- **Fourth character: Magic Defense.**

When two cards battle, the attacker rolls within its Power range, the defender rolls within whichever defense stat the attack type targets, and the higher final value wins. The Attack Type makes this non-obvious, an `X`-type attacker targets the *lower* of the defender's two defenses, and an `A`-type attacker targets the lowest of all three stats. Which defense gets used can change the outcome dramatically.

## What the simulator does

Enter two 4-character cards (for example: `9P8A` vs `6MA3`) and click **Run Simulation**. The app runs 10,000 battles and reports the empirical win rate, with a sample of 100 individual battles shown in a table below.

The **Swap** button reverses attacker and defender, useful for checking matchup symmetry, since which side attacks affects the outcome, or if you put the wrong card in the wrong box.

## Why 10,000 trials?

10,000 trials gives roughly a 1% margin of error on the win rate at the 95% confidence level. Plenty of precision for player decisions, and it runs in well under a second.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Then open the local URL Gradio prints to your terminal.

## Source

Game mechanics and stat formulas referenced from the [Final Fantasy Wiki's Tetra Master entry](https://finalfantasy.fandom.com/wiki/Tetra_Master_(minigame)), which compiles community-verified data mining and decompilation of the original game logic.

## Tech

Python · Gradio · pandas · Monte Carlo simulation
