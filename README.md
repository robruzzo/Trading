# Trading

Utilities and Machine Learning Scripts for Trading - Work In Progress

portfolio analysis - This script drives the rest, it is an example. Though with the use of tickerdatautil various methods 
of data acquisition is possible, in the example a small anticipated portfolio of 3 tickers is given. The script checks grabs
the data from the dates listed if they dont already exist. It then simulates n simulations, in this case 10000 of random 
weights for each of the tickers for a total of 100 percent of the portfolio. Afterwards, it finds the optimal portfolio
and runs CAPM upon it and writes a report. In the process, several charts are created and saved, as well as an HTML file
with the output of the script. Updates will follow.

portfoliocalc- This script is responsible for all of the calculations that are run from portfolio analysis.

tickerdatautil - responsible for obtaining and saving data. This is subject to change drastically. Retrospectively,
it doesnt seem necessary or worthwhile to use pickle files for portfolio lists. All files with respect to this script
will be changed to a .csv format and the pickle files will be no more.

report - This script creates a simple HTML output, which is subject to change. It is composed of a table which each ticker
that made it to the portfolio, statistics about each ticker, and overall portfolio information. This will include links to
each of the charts in the future, as well as additional information and new formatting. 


