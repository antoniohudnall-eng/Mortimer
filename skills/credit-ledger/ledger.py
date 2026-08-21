#!/usr/bin/env python3
"""
AIOS Credit Ledger — off-chain multi-currency accounting for agent-to-agent work.

Three currencies, three tiers:
  QL  = quiqlong        (regular  — track routine work)
  SQL = silver quiqlong (quality  — gated: paid only if the work passes a check)
  GQL = gold quiqlong   (premium  — scarcer, highest bar)

Usage:
  ledger.py init                       Create the ledger + seed starter QL
  ledger.py balance [agent]            Show balances (all currencies)
  ledger.py grant <agent> <n> [why] [-c QL|SQL|GQL]   Mint credits
  ledger.py earn  <agent> <n> [why] [-c ...]           Reward completed work
  ledger.py spend <agent> <n> [why] [-c ...]           Burn (rate-limit)
  ledger.py transfer <from> <to> <n> [why] [-c ...]    Move credits
  ledger.py pay <from> <to> <n> [why] [-c ...]         Pay a provider (typed 'pay')
  ledger.py snapshot                   Backup ledger.json to snapshots/
  ledger.py log [limit]                Show recent transactions
"""

import json
import os
import shutil
import sys
import uuid
from datetime import datetime, timezone

LEDGER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger.json")

CURRENCIES = ["QL", "SQL", "GQL"]
DEFAULT_CURRENCY = "QL"
CURRENCY_NAMES = {
    "QL": "quiqlong",
    "SQL": "silver quiqlong",
    "GQL": "gold quiqlong",
}

STARTER_AGENTS = {
    "skill-router": 200, "verify": 200, "aave": 100, "browser-automation": 100,
    "temporal-brain": 100, "master-schedule": 100, "cadence": 100, "buzz": 100,
    "roast": 100, "rip-gor-protocol": 100, "psd-brand-voice": 100,
    "shopify-manager": 100, "instagram-content-creator": 100,
    "tiktok-content-creator": 100, "x-content-creator-xai": 100,
    "youtube-content-creator": 100, "startup-cadence": 100,
    "hermes-research": 100, "depotchaos": 100,
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load():
    if not os.path.exists(LEDGER_FILE):
        return None
    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(ledger):
    tmp = LEDGER_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, LEDGER_FILE)


def new_ledger():
    return {"version": 2, "currencies": CURRENCIES, "balances": {}, "transactions": []}


def ensure_ledger():
    ledger = load()
    if ledger is None:
        die(f"Ledger not found at {LEDGER_FILE}. Run: ledger.py init")
    return ledger


def record(ledger, ttype, from_, to, amount, reason, currency=DEFAULT_CURRENCY, meta=None):
    tx = {
        "id": uuid.uuid4().hex[:12],
        "ts": now_iso(),
        "type": ttype,
        "currency": currency,
        "from": from_,
        "to": to,
        "amount": amount,
        "reason": reason or "",
    }
    if meta:
        tx["meta"] = meta
    ledger["transactions"].append(tx)
    return tx


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_amount(raw):
    try:
        n = int(raw)
    except (TypeError, ValueError):
        die(f"Amount must be a whole number, got: {raw!r}")
    if n <= 0:
        die("Amount must be positive")
    return n


def parse_currency(args):
    currency = DEFAULT_CURRENCY
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-c", "--currency") and i + 1 < len(args):
            currency = args[i + 1].upper(); i += 2
        elif a.startswith("--currency="):
            currency = a.split("=", 1)[1].upper(); i += 1
        else:
            rest.append(a); i += 1
    if currency not in CURRENCIES:
        die(f"Unknown currency {currency!r}. Valid: {', '.join(CURRENCIES)}")
    return currency, rest


def get_balance(ledger, agent, currency=DEFAULT_CURRENCY):
    return ledger["balances"].get(agent, {}).get(currency, 0)


def add_balance(ledger, agent, currency, delta):
    b = ledger["balances"].setdefault(agent, {})
    b[currency] = b.get(currency, 0) + delta
    if b[currency] == 0:
        b.pop(currency, None)
    if not b:
        ledger["balances"].pop(agent, None)


# --- commands ---

def cmd_init():
    if os.path.exists(LEDGER_FILE):
        die(f"Ledger already exists at {LEDGER_FILE} (use 'balance' or 'agents')")
    ledger = new_ledger()
    for agent, amt in sorted(STARTER_AGENTS.items()):
        add_balance(ledger, agent, "QL", amt)
        record(ledger, "grant", None, agent, amt, "initial grant", "QL")
    save(ledger)
    print(f"Ledger initialized at {LEDGER_FILE}")
    print(f"Seeded {len(STARTER_AGENTS)} agents with starter QL.")
    print(f"Currencies: QL (quiqlong) · SQL (silver) · GQL (gold) — $0 fiat.")


def cmd_balance(ledger, agent=None):
    if agent:
        if agent not in ledger["balances"]:
            die(f"Unknown agent: {agent!r}")
        print(f"{agent}:")
        for c in CURRENCIES:
            n = get_balance(ledger, agent, c)
            if n:
                print(f"  {c:<4} {n:>10,}  ({CURRENCY_NAMES[c]})")
        return
    print(f"{'agent':<26} {'QL':>10} {'SQL':>10} {'GQL':>10}")
    print("-" * 60)
    totals = {c: 0 for c in CURRENCIES}
    for name in sorted(ledger["balances"]):
        q = get_balance(ledger, name, "QL")
        s = get_balance(ledger, name, "SQL")
        g = get_balance(ledger, name, "GQL")
        if q or s or g:
            print(f"{name:<26} {q:>10,} {s:>10,} {g:>10,}")
            totals["QL"] += q; totals["SQL"] += s; totals["GQL"] += g
    print("-" * 60)
    print(f"{'TOTAL in circulation':<26} {totals['QL']:>10,} {totals['SQL']:>10,} {totals['GQL']:>10,}")


def cmd_agents(ledger):
    cmd_balance(ledger)


def _mint_or_move(ledger, args, ttype, need_to):
    currency, args = parse_currency(args)
    if need_to:
        if len(args) < 3:
            die(f"Usage: ledger.py {ttype} <from> <to> <amount> [reason] [-c CUR]")
        frm, to, amount = args[0], args[1], parse_amount(args[2])
        reason = " ".join(args[3:])
        if frm == to:
            die("Cannot send to self")
        if get_balance(ledger, frm, currency) < amount:
            die(f"Insufficient {currency}: {frm} has {get_balance(ledger, frm, currency)}, needs {amount}")
        add_balance(ledger, frm, currency, -amount)
        add_balance(ledger, to, currency, amount)
    else:
        if len(args) < 2:
            die(f"Usage: ledger.py {ttype} <agent> <amount> [reason] [-c CUR]")
        agent, amount = args[0], parse_amount(args[1])
        reason = " ".join(args[2:])
        if ttype == "spend":
            if get_balance(ledger, agent, currency) < amount:
                die(f"Insufficient {currency}: {agent} has {get_balance(ledger, agent, currency)}, needs {amount}")
            add_balance(ledger, agent, currency, -amount)
        else:  # grant / earn
            add_balance(ledger, agent, currency, amount)
    record(ledger, ttype, frm if need_to else (None if ttype != "spend" else agent),
           to if need_to else (agent if ttype != "spend" else None),
           amount, reason, currency)
    save(ledger)
    arrow = "->" if need_to else ("->" if ttype != "spend" else "<-")
    target = to if need_to else agent
    print(f"{ttype}: {amount} {currency} {arrow} {target} (balance {get_balance(ledger, target, currency)})")


def cmd_grant(ledger, args):
    _mint_or_move(ledger, args, "grant", need_to=False)


def cmd_earn(ledger, args):
    _mint_or_move(ledger, args, "earn", need_to=False)


def cmd_spend(ledger, args):
    _mint_or_move(ledger, args, "spend", need_to=False)


def cmd_transfer(ledger, args):
    _mint_or_move(ledger, args, "transfer", need_to=True)


def cmd_pay(ledger, args):
    _mint_or_move(ledger, args, "pay", need_to=True)


def cmd_snapshot(ledger, args):
    snap_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapshots")
    os.makedirs(snap_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dst = os.path.join(snap_dir, f"ledger-{ts}.json")
    shutil.copy2(LEDGER_FILE, dst)
    snaps = sorted(os.listdir(snap_dir))
    for old in snaps[:-20]:
        os.remove(os.path.join(snap_dir, old))
    print(f"snapshot -> {dst}")


def cmd_log(ledger, args):
    limit = 20
    if args:
        try:
            limit = int(args[0])
        except ValueError:
            die(f"limit must be a number, got: {args[0]!r}")
    txs = ledger["transactions"]
    for tx in reversed(txs[-limit:]):
        arrow = {"grant": "MINT->", "earn": "EARN->", "spend": "<-SPEND",
                 "transfer": "->", "pay": "PAY->", "reserve": "HOLD->",
                 "settle": "SETTLE->", "refund": "REFUND->"}.get(tx["type"], tx["type"])
        who = tx["to"] if tx["to"] else tx["from"]
        cur = tx.get("currency", "QL")
        print(f"{tx['ts'][:19]}  {tx['id']}  {tx['type']:<8} {cur:<4} {arrow} {who:<22} {tx['amount']:>6}  {tx['reason']}")
    if not txs:
        print("No transactions yet.")


def main():
    args = sys.argv[1:]
    if not args:
        die("No command. Run 'ledger.py init' first.")
    cmd = args[0]
    if cmd == "init":
        cmd_init()
        return
    ledger = ensure_ledger()
    rest = args[1:]
    if cmd == "balance":
        cmd_balance(ledger, rest[0] if rest else None)
    elif cmd == "agents":
        cmd_agents(ledger)
    elif cmd == "grant":
        cmd_grant(ledger, rest)
    elif cmd == "earn":
        cmd_earn(ledger, rest)
    elif cmd == "spend":
        cmd_spend(ledger, rest)
    elif cmd == "transfer":
        cmd_transfer(ledger, rest)
    elif cmd == "pay":
        cmd_pay(ledger, rest)
    elif cmd == "snapshot":
        cmd_snapshot(ledger, rest)
    elif cmd == "log":
        cmd_log(ledger, rest)
    else:
        die(f"Unknown command: {cmd!r}")


if __name__ == "__main__":
    main()
