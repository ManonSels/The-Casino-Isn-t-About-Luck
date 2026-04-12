import random
import numpy as np
import matplotlib.pyplot as plt

# ── Wheel Setup ──────────────────────────────
european_wheel = list(range(0, 37))
american_wheel = list(range(0, 38))     # (because 0 and 00)
red_numbers    = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

def spin(wheel):
    return random.choice(wheel)

def is_red(n):
    return n in red_numbers

# ── Probabilities ─────────────────────────────
eu_p = 18 / 37
am_p = 18 / 38

# ── Simulation ───────────────────────────────
N_SPINS   = 500
N_PLAYERS = 200
START     = 100

def simulate(wheel):
    balance = START
    history = [balance]
    for _ in range(N_SPINS):
        balance += 1 if is_red(spin(wheel)) else -1
        history.append(balance)
    return history

def convergence(wheel, n=5000):
    reds, props = 0, []
    for i in range(1, n + 1):
        if is_red(spin(wheel)):
            reds += 1
        props.append(reds / i)
    return props

eu_runs = [simulate(european_wheel) for _ in range(N_PLAYERS)]
am_runs = [simulate(american_wheel) for _ in range(N_PLAYERS)]

eu_avg = np.mean(eu_runs, axis=0)
am_avg = np.mean(am_runs, axis=0)

spins = np.arange(N_SPINS + 1)
eu_expected = START + spins * (eu_p - (1 - eu_p))
am_expected = START + spins * (am_p - (1 - am_p))

eu_conv = convergence(european_wheel)
am_conv = convergence(american_wheel)

eu_finals = [r[-1] for r in eu_runs]
am_finals = [r[-1] for r in am_runs]

# ── Plots ─────────────────────────────────────
fig, axes = plt.subplots(3, 2, figsize=(14, 15))
fig.suptitle("A coin that isnt fair - Roulette", fontsize=15, fontweight="bold")

labels = ["European Roulette (0)", "American Roulette (0 and 00)"]
runs   = [eu_runs, am_runs]
avgs   = [eu_avg, am_avg]
exps   = [eu_expected, am_expected]
convs  = [eu_conv, am_conv]
finals = [eu_finals, am_finals]
colors = ["steelblue", "tomato"]
probs  = [eu_p, am_p]

for col, (label, run, avg, exp, conv, final, color, p) in enumerate(
        zip(labels, runs, avgs, exps, convs, finals, colors, probs)):

    # Row 1: Bankroll over time
    ax = axes[0][col]
    for r in run[:60]:
        ax.plot(r, color=color, alpha=0.05, linewidth=0.8)
    ax.plot(avg, color=color, linewidth=2.5, label="Simulated average")
    ax.plot(exp, color="black", linewidth=1.5, linestyle="--", label="Theoretical expected value")
    ax.axhline(START, color="gray", linewidth=1, linestyle=":")
    ax.set_title(label)
    ax.set_xlabel("Spins")
    ax.set_ylabel("Balance (€)")
    ax.legend(fontsize=9)

    # Row 2: Convergence
    ax = axes[1][col]
    ax.plot(conv, color=color, linewidth=1, label="Simulated proportion")
    ax.axhline(p,   color="black", linewidth=1.5, linestyle="--", label=f"True P = {p:.4f}")
    ax.axhline(0.5, color="gray",  linewidth=1,   linestyle=":",  label="0.5 (fair)")
    ax.set_title(f"P(red) converging - {label}")
    ax.set_xlabel("Spins")
    ax.set_ylabel("Proportion of reds")
    ax.set_ylim(0.42, 0.58)
    ax.legend(fontsize=9)

    # Row 3: Final balance distribution
    ax = axes[2][col]
    ax.hist(final, bins=30, color=color, alpha=0.8)
    ax.axvline(START, color="black", linewidth=1.5, linestyle="--", label=f"Start €{START}")
    ax.axvline(np.mean(final), color=color, linewidth=2, linestyle="-", label=f"Mean €{np.mean(final):.1f}")
    ax.set_title(f"Final balances after {N_SPINS} spins - {label}")
    ax.set_xlabel("Final Balance (€)")
    ax.set_ylabel("Number of players")
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig("results/roulette.png", dpi=150)
plt.show()