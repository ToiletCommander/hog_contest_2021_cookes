import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from auth import OAuthSession
from baseline_strategy import baseline_strategy
from final_strategy import final_strategy
import final_strategy_train
from ucb import main

GOAL_SCORE = 100

ENDPOINT = "https://hog-calc.cs61a.org/api/compare_strategies"
STRATEGY_TO_COMPARE_TO = "last_before_ult"
STRATEGY_TO_COMPARE_TO_EPOCH = 10
COMP_STRAT_FILENAME = 'savedStrats/' + STRATEGY_TO_COMPARE_TO + "_" + str(STRATEGY_TO_COMPARE_TO_EPOCH) + ".pkl"
compstrat = final_strategy_train.loadStrategy(COMP_STRAT_FILENAME)

def export(strategy):
    out = []
    for i in range(100):
        out.append([])
        for j in range(100):
            out[-1].append(strategy(i, j))
    return out


def compare(strategy_1, strategy_2):
    data = {
        "strat0": json.dumps(export(strategy_1)),
        "strat1": json.dumps(export(strategy_2)),
        "token": OAuthSession().auth(),
    }
    request = Request(ENDPOINT, bytes(urlencode(data), "utf-8"))
    try:
        body = json.loads(urlopen(request).read().decode())
        win_rate = body["win_rate"]
        print("Win rate: {}".format(win_rate))
        return win_rate
    except HTTPError as e:
        message = e.read().decode()
        print("Error: {}".format(message))
        raise Exception(message)


@main
def main():
    compare(final_strategy, compstrat)