'''
This script will be employed to run all of the other scripts to calculate portfolio values and risk
'''

import tickerdatautil as td
import portfoliocalc as pc
import os
import pandas as pd
import report as rpt


#Allow for csv or pickle

portfolio_directory='E:/Portfolios/' #Include the trailing '/'
portfolio_name='mythree/'
data_subdirectory='data/'
ticker_sub_directory ='mythree/'
output_directory='output/'
report_root='reports/'
report_data_directory='data/'

portfolio_root=portfolio_directory+portfolio_name
portfolio_data=portfolio_root+data_subdirectory
portfolio_ticker=portfolio_data+ticker_sub_directory
portfolio_output=portfolio_root+output_directory
report_directory=portfolio_root+report_root
report_data_root=report_directory+report_data_directory

ticker_file='mythree.pickle'
output_file='mythree_portfolio.pickle'
reference_file='index.pickle'


data=pd.DataFrame(index=['Date'])
simulations=10000
risk_free_rate=4.0
delay=0.5     #Default Delay between downloads in seconds
start_date='2010-01-01'
end_date='2017-01-01'
interval='1d'
reference_ticker='^GSPC'


'''
Directory Structure:
    portfolio_directory
    -->portfolio_name
       -->output_directory
       -->data_subdirectory
          -->ticker_subdirectory


'''
#Create folder for the portfolio, with the portfolio name
if not os.path.exists(portfolio_root):
        os.makedirs(portfolio_root)
#Create data subdirectory
if not os.path.exists(portfolio_data):
        os.makedirs(portfolio_data)
#Create Ticker Subdirectory
if not os.path.exists(portfolio_ticker):
        os.makedirs(portfolio_ticker)
#Create output subdirectory
if not os.path.exists(portfolio_output):
        os.makedirs(portfolio_output)
#Create report subdirectory
if not os.path.exists(report_data_root):
        os.makedirs(report_data_root)
#Create report data subdirectory
if not os.path.exists(report_data_root):
        os.makedirs(report_data_root)

# Data Section

#Portfolio Tickers
df = pd.DataFrame(data=['AAPL','IBM','OLED'], columns=['Ticker']) 
td.convert_tickers_df_to_pickle(portfolio_data,ticker_file,df)
td.get_data_from_yahoo_specific(portfolio_data,ticker_sub_directory,ticker_file,start_date,
                                end_date,interval,False,False,0.5)
#Reference Tickers
df = pd.DataFrame(data=[reference_ticker], columns=['Ticker']) 
td.convert_tickers_df_to_pickle(portfolio_data,reference_file,df)
td.get_data_from_yahoo_specific(portfolio_data,ticker_sub_directory,reference_file,start_date,
                                end_date,interval,False,False,0.5)

tickers=pc.get_tickers(portfolio_data,ticker_file)
data=pc.load_data(portfolio_data,ticker_sub_directory,tickers,data)
pc.show_data(data,report_data_root)
returns=pc.calc_daily_returns(data)
pc.plot_daily_returns(returns,report_data_root)
pc.show_statistics(returns)
weights=pc.init_weights(tickers)
pc.calc_portfolio_return(returns,weights)
pc.calc_portfolio_variance(returns,weights)
preturns,pvariances=pc.create_portfolios(weights,returns,simulations,tickers)
pc.plot_portfolios(preturns,pvariances,report_data_root)
optimum=pc.optimize_portfolio(weights,returns,tickers)
pc.print_optimial_portfolio(optimum,returns)
ports=pc.save_optimial_portfolio_pickle(portfolio_output,output_file,optimum,returns,tickers)
pc.show_optimal_portfolio(optimum,returns,preturns,pvariances,report_data_root)
sharpe=-pc.statistics(weights,returns)[2]

reference_data=pc.load_ticker_data(portfolio_data,ticker_sub_directory,reference_ticker)
reference_data.index=pd.to_datetime(reference_data.index)

CAPMS=[]
for x in range(len(ports)):
    ticker_data=pc.load_ticker_data(portfolio_data,ticker_sub_directory,ports[x][0])
    ticker_data.index=pd.to_datetime(ticker_data.index)
    covmat,beta,alpha,expected_return=pc.capm(ticker_data,reference_data,risk_free_rate,ports[x][0],report_data_root)
    CAPMS.append([ports[x][0],covmat,beta,alpha,expected_return]) 


column_names=['ticker','weight','avg_ret','alpha','beta','exp_ret','weightB','SumPB','sharpe','reference']
report_data= pd.DataFrame(columns = column_names)
weight_data=[]


#copy weights that matter with ticker
for x in range(len(tickers)):
    if optimum['x'][x]>1.0e-3:
        weight_data.append([tickers[x],optimum['x'][x]])
        

SumPB=0
for x in range(len(CAPMS)):
    ticker=CAPMS[x][0]
    alpha=CAPMS[x][3]
    beta=CAPMS[x][2]
    exp_ret=CAPMS[x][4]
    if weight_data[x][0]==ticker:
        weight=weight_data[x][1].round(3)
        avg_ret=returns[ticker].mean()*252
        weighted_beta=weight*beta.round(3)
        SumPB+=weighted_beta
    report_data = report_data.append({'ticker':ticker,'weight':"%.3f"% weight,'avg_ret':"%.3f" % avg_ret,
                                      'alpha':"%.3f" % alpha,'beta': "%.3f" % beta,'exp_ret':"%.3f" % exp_ret,'weightB': "%.3f" % weighted_beta,
                                      'SumPB':"%.3f" % SumPB, 'sharpe':"%.3f" % sharpe,'reference':reference_ticker}, 
                                     ignore_index=True)    


    
rpt.create_report(report_directory,report_data)
    

'''
NOTES: 

    Portfolio beta = sum of the weights of each security in the portfolio*its beta

    Bp = Ba*Wa + Bb*Wb + Bc*Wc... Bn*Wn

    Get all scripts working inside of this script and then remove the defaults
    
    The script will: 
        -Download, Update, or Load the data for the desired stocks
        -An Optimized portfolio based on the stocks in the file, etc will be generated
        -The Capital Asset Pricing Model will be run to see what the overall Beta of the portfolio is
        -All generated files will be saved in an output directory
        -A report will be generated with all relavant information
        -Flags will be used to determine whether charts are created
        -??? An HTML file will be generated for the report
    
'''

