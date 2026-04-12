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

true_p_lose = 19 / 37
base_bet    = 10
table_limit = 500
START       = 500

# ── Simulation 1: Single player ───────────────
def martingale_single(n_spins=200, start=START):
    balance  = start
    bet      = base_bet
    history  = [balance]
    bet_hist = [bet]
    for _ in range(n_spins):
        if balance <= 0:
            history.append(0)
            bet_hist.append(0)
            continue
        bet = min(bet, table_limit, balance)
        if is_red(spin()):
            balance += bet
            bet      = base_bet
        else:
            balance -= bet
            bet     *= 2
        history.append(balance)
        bet_hist.append(bet)
    return history, bet_hist

# ── Simulation 2: Survival rate ───────────────
def martingale_run(n_spins=300, start=START):
    balance = start
    bet     = base_bet
    history = [balance]
    for _ in range(n_spins):
        if balance <= 0:
            history.append(0)
            continue
        bet = min(bet, table_limit, balance)
        if is_red(spin()):
            balance += bet
            bet      = base_bet
        else:
            balance -= bet
            bet     *= 2
        history.append(balance)
    return history

N_PLAYERS = 500
N_SPINS   = 300
runs      = [martingale_run(N_SPINS) for _ in range(N_PLAYERS)]

# survival: % of players still solvent at each spin
survival  = [
    sum(1 for r in runs if r[i] > 0) / N_PLAYERS * 100
    for i in range(N_SPINS + 1)
]

# ── Simulation 3: Losing streak probability ──
streaks    = list(range(1, 11))
theory_p   = [(true_p_lose ** n) * 100 for n in streaks]
bets_after = [base_bet * (2 ** n) for n in streaks]

# ── Plots ─────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(11, 15))
fig.suptitle("Chapter 3: Martingale Strategy",
             fontsize=14, fontweight="bold")

# ── Plot 1: Single player balance ──
history, bet_hist = martingale_single()
ax = axes[0]
ax.plot(history, color="steelblue", linewidth=2, label="Player balance")
ax.axhline(START, color="gray", linewidth=1, linestyle=":", label=f"Starting balance €{START}")

ax.fill_between(range(len(history)), history, START,
                where=[h < START for h in history],
                color="tomato", alpha=0.15, label="Below starting balance")
ax.set_title("One player balance over time", fontsize=12)
ax.set_xlabel("Spins")
ax.set_ylabel("Balance (€)")
ax.legend(fontsize=10)

# ── Plot 2: Survival rate ──
ax = axes[1]
ax.plot(survival, color="steelblue", linewidth=2.5)
ax.fill_between(range(N_SPINS + 1), survival, alpha=0.15, color="steelblue")
ax.axhline(50, color="tomato", linewidth=1.5, linestyle="--", label="50% of players broke")

# find when survival first drops below 50%
below_50 = next((i for i, s in enumerate(survival) if s < 50), None)
if below_50:
    ax.axvline(below_50, color="tomato", linewidth=1, linestyle=":")

ax.set_title(f"% of players still alive - {N_PLAYERS} players", fontsize=12)
ax.set_xlabel("Spins")
ax.set_ylabel("% of players with balance > €0")
ax.set_ylim(0, 105)
ax.legend(fontsize=10)

# ── Plot 3: Losing streak probability ──
ax    = axes[2]
ax_r  = ax.twinx()
ax.bar(streaks, theory_p, color="tomato", alpha=0.7, label="P(losing streak) %")
ax_r.plot(streaks, bets_after, "o-", color="black", linewidth=2,
          markersize=7, label="Required bet (€)")
ax_r.axhline(table_limit, color="gray", linewidth=1.2, linestyle="--")
ax_r.text(9, table_limit + 15, f"Table limit €{table_limit}", fontsize=9, color="gray")
ax.set_title("Probability of a losing streak vs the bet it forces you to make", fontsize=12)
ax.set_xlabel("Losses in a row")
ax.set_ylabel("Probability (%)", color="tomato")
ax_r.set_ylabel("Required bet (€)", color="black")
ax.set_xticks(streaks)
ax.legend(loc="upper right", fontsize=10)
ax_r.legend(loc="center right", fontsize=10)

plt.tight_layout()
plt.savefig("results/martingale_strategy.png", dpi=150)
plt.show()