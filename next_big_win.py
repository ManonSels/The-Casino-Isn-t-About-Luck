import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Setup ─────────────────────────────────────
P_WIN     = 1 / 50  # 2% chance of "big win"
N_SIMULATIONS = 10000

def simulate_streak(starting_streak):
    additional_spins = 0
    while True:
        additional_spins += 1
        if random.random() < P_WIN:
            return additional_spins

# ── Simulation: Compare fresh players vs. players on losing streaks ──
fresh_players_wait = []
streak_players_wait = []
streak_50_wait = []

for _ in range(N_SIMULATIONS):
    fresh_players_wait.append(simulate_streak(0))
    streak_players_wait.append(simulate_streak(30))
    streak_50_wait.append(simulate_streak(50))

# ── Calculate "quit before winning" percentages ──
quit_after_more = [10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 500]

quit_percentages_fresh = []
quit_percentages_streak = []
quit_percentages_streak_50 = []

for q in quit_after_more:
    # % of players who would quit before winning if they quit after q spins
    pct_fresh = sum(1 for w in fresh_players_wait if w > q) / N_SIMULATIONS * 100
    pct_streak = sum(1 for w in streak_players_wait if w > q) / N_SIMULATIONS * 100
    pct_streak_50 = sum(1 for w in streak_50_wait if w > q) / N_SIMULATIONS * 100
    
    quit_percentages_fresh.append(pct_fresh)
    quit_percentages_streak.append(pct_streak)
    quit_percentages_streak_50.append(pct_streak_50)

# ── Find the "99%" point ──
for i, q in enumerate(quit_after_more):
    if quit_percentages_fresh[i] >= 99:
        spins_to_99_fresh = q
        pct_at_99_fresh = quit_percentages_fresh[i]
        break
else:
    spins_to_99_fresh = ">500"
    pct_at_99_fresh = quit_percentages_fresh[-1]

# ── Create the visualization ──
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('"99% of Gamblers Quit Before Their Next Big Win"', 
             fontsize=14, fontweight="bold")

# ── Plot 1: Distribution of wait times ──
ax = axes[0]
bins = range(0, 250, 5)
ax.hist(fresh_players_wait, bins=bins, alpha=0.5, density=True, 
        label="Fresh players", color="steelblue", edgecolor="none")
ax.hist(streak_players_wait, bins=bins, alpha=0.5, density=True, 
        label="Players on 30-loss streak", color="tomato", edgecolor="none")
ax.axvline(50, color="gray", linestyle="--", linewidth=1, label="Expected wait (50 spins)")
ax.set_title("Wait time until next win is the same regardless of past losses", fontsize=11)
ax.set_xlabel("Additional spins until win")
ax.set_ylabel("Density (probability)")
ax.set_xlim(0, 250)
ax.legend()

# ── Plot 2: Past losses dont matter ──
ax = axes[1]
ax.plot(quit_after_more, quit_percentages_fresh, 'o-', color="steelblue", 
        linewidth=2.5, label="Fresh players", markersize=6)
ax.plot(quit_after_more, quit_percentages_streak, 's-', color="tomato", 
        linewidth=2.5, label="Players on 30-loss streak", markersize=6, alpha=0.8)
ax.plot(quit_after_more, quit_percentages_streak_50, '^-', color="purple", 
        linewidth=2.5, label="Players on 50-loss streak", markersize=6, alpha=0.8)

ax.set_title("Past losses dont matter", fontsize=11)
ax.set_xlabel("Number of additional spins before quitting")
ax.set_ylabel("Percentage who would quit before winning (%)")
ax.set_xscale('log')
ax.set_xticks(quit_after_more)
ax.set_xticklabels([str(q) for q in quit_after_more], rotation=45)
ax.set_ylim(0, 105)
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout(rect=[0, 0.08, 1, 0.95])
plt.savefig("results/next_big_win.png", dpi=150)
plt.show()