## Creating a strategy

In the user_data folder there is a strategies directory. In there you can make different Strategies.

## Running in Sandbox

There is a command in the docker compose file. When you do docker-compose up it will run that command. For sandbox use this -
```
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade.log
      --db-url sqlite:////freqtrade/user_data/tradesv3.sqlite
      --config /freqtrade/user_data/config.json
      --strategy BBRSINaiveStrategy
```
Then run
```
docker-compose up -d 
docker-compose logs -f 
```

## Running Live
Change the config file to have the API Keys etc then define the Strategy in the Docker-Compose file under command
`


## Getting Pairs Data

The RM is used here as we don't want this container to stay built, we're simply using Freqtrade to download the pairs, then the container will stop because it's finished and we then remove it to free up space

`docker-compose run --rm freqtrade download-data --exchange binance -t 15m --pairs-file ./user_data/data/binance/pairs.json`

## Backtesting
`docker-compose run --rm freqtrade backtesting --datadir user_data/data/binance --export trades --stake-amount 100 -s BBRSINaiveStrategy -i 15m`

### Plotting
You can then plot these results
`docker-compose run --rm freqtrade plot-dataframe --strategy BBRSINaiveStrategy -p ALGO/USDT -i 15m`

Once the plot is ready you will see the message Stored plot as /freqtrade/user_data/plot/freqtrade-plot-ALGO_USDT-15m.html which you can open in a browser window.


## Optimising - Guide is outdated, need new HyperOpt Guide

To optimize the strategy we will use the Hyperopt module of freqtrade. First up we need to create a new hyperopt file from a template:

`docker-compose run --rm freqtrade new-hyperopt --hyperopt BBRSIHyperopt`

Now add desired definitions for buy/sell guards and triggers to the Hyperopt file. Then run the optimization like so (NOTE: set the time interval and the number of epochs to test using the `-i` and `-e` flags:

`docker-compose run --rm freqtrade hyperopt --hyperopt BBRSIHyperopt --hyperopt-loss SharpeHyperOptLoss --strategy BBRSINaiveStrategy -i 15m`

## Alex way
Pull new strategies from here: https://github.com/freqtrade/freqtrade-strategies
Run the TestAllStrategies.py file to See which is the best performing strat
Then optimise it using HyperOpt
`docker-compose run --rm freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy GodStraNew -i 15m -e 500`

Then

## Misc Freqtrade Commands

### Find Pairs Freqtrade has download
`docker-compose run --rm freqtrade list-data --exchange binance`

## Resources

Very good video here: https://www.youtube.com/watch?v=wq3uLSDJxUQ
with Github here : https://github.com/devbootstrap/optimize-trading-strategy-using-freqtrade/blob/main/README.md

## Strategies
Github full of Strats here: https://github.com/freqtrade/freqtrade-strategies


