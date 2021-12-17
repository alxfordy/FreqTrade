import glob
import subprocess
import json
import pandas as pd
import datetime

def run():
    test_strategies()
    results = process_results()
    return results


def test_strategies():
    for strategy_file in glob.glob('/mnt/g/Coding/Freqtrade/user_data/strategies/*'):
        print(strategy_file)
        try:
            with open(strategy_file) as class_file:
                for line in class_file:
                    if "class" in line:
                        class_name = line.split(" ")[1].split("(")[0]
                        print(class_name)
                        output = subprocess.check_output(f"docker-compose run --rm freqtrade backtesting --datadir user_data/data/binance --export trades --stake-amount 100 -s {class_name} -i 15m".split())
                        print(output)
        except subprocess.CalledProcessError as e:
            print(e.output)
        except Exception as e:
            print(e)

def process_results():
    strategies = dict()
    for result_file in glob.glob("/mnt/g/Coding/Freqtrade/user_data/backtest_results/*"):
        with open(result_file) as result_data:
            data = json.load(result_data)
            comparison_data = data.get("strategy_comparison")[0]
            strategies[comparison_data.get("key")] = {
                'trades': comparison_data.get("trades"),
                "profit_mean": comparison_data.get("profit_mean"),
                "profit_mean_pct": comparison_data.get("profit_mean_pct") ,
                "profit_sum": comparison_data.get("profit_sum"),
                "profit_sum_pct": comparison_data.get("profit_sum_pct"),
                "profit_total_abs": comparison_data.get("profit_total_abs"),
                "profit_total": comparison_data.get("profit_total"),
                "profit_total_pct": comparison_data.get("profit_total_pct"),
                "duration_avg": comparison_data.get("duration_avg"),
                "wins": comparison_data.get("wins"),
                "draws": comparison_data.get("draws"),
                "losses": comparison_data.get("losses"),
                "max_drawdown_per": comparison_data.get("max_drawdown_per"),
                "max_drawdown_abs": comparison_data.get("max_drawdown_abs")
            }
    return strategies

            



if __name__ == "__main__":
    results = run()
    df = pd.DataFrame.from_dict(results, orient='index')
    df.to_csv(f"Backtest_Results+{datetime.datetime.now()}.csv")
