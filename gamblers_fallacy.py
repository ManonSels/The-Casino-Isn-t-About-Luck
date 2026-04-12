import random
import numpy as np
import matplotlib.pyplot as plt

# ── Wheel Setup ──────────────────────────────
european_wheel = list(range(0, 37))
red_numbers    = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

def spin():
    return random.choice(european_wheel)

def is_red(n):
    return n in red_numbers

true_p = 18 / 37

# ── Simulation 1: P(red) after streak of reds ─
def p_red_after_streak(streak_length, trials=100000):
    spins = [is_red(spin()) for _ in range(trials)]
    reds_after, found = 0, 0
    for i in range(len(spins) - streak_length - 1):
        if all(spins[i:i + streak_length]):
            found += 1
            if spins[i + streak_length]:
                reds_after += 1
    return reds_after / found if found > 0 else 0

streaks     = list(range(1, 7))
simulated_p = [p_red_after_streak(s) for s in streaks]

# ── Simulation 2: Streak distribution ────────
def get_streaks(n_spins=50000):
    streaks, current = [], 1
    last = is_red(spin())
    for _ in range(n_spins - 1):
        result = is_red(spin())
        if result == last:
            current += 1
        else:
            streaks.append(current)
            current = 1
            last    = result
    return streaks

all_streaks = get_streaks()

# ── Plots ─────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(11, 10))
fig.suptitle("The Gambler's Fallacy",
             fontsize=14, fontweight="bold")

# Plot 1: P(red) stays flat after streaks
ax = axes[0]
ax.plot(streaks, simulated_p, "o-", color="tomato", linewidth=2.5,
        markersize=9, label="Simulated P(red | last N spins were red)")
ax.axhline(true_p, color="black", linewidth=1.5, linestyle="--",
           label=f"True P(red) = 18/37 = {true_p:.4f}")
ax.axhline(0.5, color="gray", linewidth=1, linestyle=":",
           label="0.5 (fair coin)")
ax.set_title("Does a streak of reds change the next probability?", fontsize=12)
ax.set_xlabel("Length of red streak before next spin")
ax.set_ylabel("P(red on next spin)")
ax.set_xticks(streaks)
ax.set_xticklabels([f"{s} reds in a row" for s in streaks])
ax.set_ylim(0.35, 0.65)
ax.legend(fontsize=10)

# Plot 2: Streak distribution
ax = axes[1]
max_s = min(max(all_streaks), 10)
bins  = np.arange(1, max_s + 2) - 0.5
ax.hist(all_streaks, bins=bins, color="steelblue", alpha=0.8, edgecolor="white")
ax.set_title("Streak lengths across 50,000 spins ", fontsize=12)
ax.set_xlabel("Streak length")
ax.set_ylabel("Frequency")
ax.set_xticks(range(1, max_s + 1))

for n in range(1, max_s + 1):
    count = sum(1 for s in all_streaks if s == n)
    ax.text(n, count + 100, f"P={true_p**n:.3f}", ha="center", fontsize=8)

plt.tight_layout()
plt.savefig("results/gamblers_fallacy.png", dpi=150)
plt.show()