import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as opt
import pickle
import os as os


def get_tickers(data_directory,fileName):
    with open(data_directory + fileName,"rb") as f:
            tickers=pickle.load(f)
    return tickers

def show_data(data,report_data_dir):
    data.plot(figsize=(10,5))
    graph_name = "Ticker_Data.png"
    if not os.path.isdir(report_data_dir):
        os.makedirs(report_data_dir)
    plt.savefig(report_data_dir + graph_name)
    plt.clf()

def load_data(data_directory,ticker_sub_directory,tickers, data):
    for ticker in tickers:
        ticker_data = pd.read_csv(data_directory+ticker_sub_directory+ticker+'.csv',parse_dates=True)
        ticker_data['Date']=pd.to_datetime(ticker_data['Date'])
        ticker_data['Date']=ticker_data['Date'].dt.strftime('%m/%d/%Y')
        ticker_data.set_index(['Date'],inplace=True)
        ticker_data=ticker_data[['Close']]
        ticker_data.rename(columns={'Close':"{}".format(ticker)}, inplace=True)
        data = pd.concat([data, ticker_data], axis=1, sort=False)
        data=data.dropna()
    return data

def load_ticker_data(data_directory,ticker_sub_directory,ticker):
    ticker_data = pd.read_csv(data_directory+ticker_sub_directory+ticker+'.csv',parse_dates=True)
    ticker_data['Date']=pd.to_datetime(ticker_data['Date'])
    ticker_data['Date']=ticker_data['Date'].dt.strftime('%m/%d/%Y')
    ticker_data.set_index(['Date'],inplace=True)
    '''
    ticker_data=ticker_data[['Close']]
    ticker_data.rename(columns={'Close':"{}".format(ticker)}, inplace=True)
    data = pd.concat([data, ticker_data], axis=1, sort=False)
    data=data.dropna()
    '''
    return ticker_data

def calc_daily_returns(data):
    returns=np.log(data/data.shift(1))
    return returns;

def plot_daily_returns(returns,report_data_dir):
    returns.plot(figsize=(10,5))
    graph_name = "daily_returns.png"
    if not os.path.isdir(report_data_dir):
        os.makedirs(report_data_dir)
    plt.savefig(report_data_dir + graph_name)
    plt.clf()

def show_statistics(returns):
    print("\nAverage Returns:")
    print(returns.mean()*252)
    print("\nCovariance Matrix:")
    print(returns.cov()*252)

'''
Function Name: init_weights()
Purpose: This function randomly initializes the weights of the
         stocks as it relates to their weight in the portfolio
'''
def init_weights(tickers):
    weights =np.random.random(len(tickers))
    weights /= np.sum(weights)
    return weights

'''
Function Name: calc_portfolio_return(returns, weights)
Purpose: This function will calculate the overall estimated return of
         the portfolio based on the average returns of the stocks.
'''
def calc_portfolio_return(returns, weights):
    portfolio_return=np.sum(returns.mean()*weights)*252
    print("Expected portfolio return: ", portfolio_return)
    return portfolio_return

'''
Function Name: calculate portfolio_variance(returns, weights)
Purpose: Calculate the variance in the portfolio, or average risk
'''
def calc_portfolio_variance(returns, weights):
    portfolio_variance = np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252, weights)))
    print("Expected portfolio variance: ",portfolio_variance)
    return portfolio_variance

def create_portfolios(weights,returns,simulations,tickers):
    preturns=[]
    pvariances=[]
    #Monte Carlo Simulation
    for i in range(simulations):
        weights = np.random.random(len(tickers))
        weights/=np.sum(weights)
        preturns.append(np.sum(returns.mean()*weights)*252)
        pvariances.append(np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252, weights))))
    preturns=np.array(preturns)
    pvariances=np.array(pvariances)
    #print("Elapsed Time: ",time.time()-start_time)
    return preturns, pvariances

def plot_portfolios(returns,variances,report_data_dir):
    plt.figure_size=(10,6)
    plt.scatter(variances, returns,c=returns/variances,marker='o')
    plt.grid(True)
    plt.xlabel("Expected Volatility")
    plt.ylabel("Expected Return")
    plt.colorbar(label='Sharpe Ratio')
    graph_name = "Random_Portfolios.png"
    if not os.path.isdir(report_data_dir):
        os.makedirs(report_data_dir)
    plt.savefig(report_data_dir + graph_name)
    plt.clf()


def statistics(weights,returns):
    portfolio_return=np.sum(returns.mean()*weights)*252
    portfolio_volatility=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
    return np.array([portfolio_return,portfolio_volatility,portfolio_return/portfolio_volatility])

def min_sharpe(weights,returns):
    return -statistics(weights,returns)[2]

def optimize_portfolio(weights,returns,tickers):
    constraints=({'type':'eq','fun':lambda x: np.sum(x)-1}) #constrain the weights to a sum of 1
    bounds = tuple((0,1) for x in range(len(tickers)))
    optimum=opt.minimize(fun=min_sharpe, x0=weights, args=returns, method='SLSQP',bounds=bounds, constraints=constraints)
    return optimum

def print_optimial_portfolio(optimum, returns):
    print("Optimal Weights: ", optimum['x'].round(3))
    print("Expected Return:, volatility and Sharpe Ratio:", statistics(optimum['x'].round(3),returns))
'''
def save_optimial_portfolio(optimum, returns):
    print("Optimal Weights: ", optimum['x'].round(3))
    print("Expected Return:, volatility and Sharpe Ratio:", statistics(optimum['x'].round(3),returns))
    print("Saving Optimum Portfolio")
    with open(data_directory + output_portfolio_name,"wb") as f:
        pickle.dump(optimum['x'].round(3),f)
'''

def save_optimial_portfolio_pickle(output_directory,output_portfolio_name,optimum, returns,tickers):
    x=0
    port=[]
    print("Saving Optimum Portfolio")
    for ticker in tickers:
        if optimum['x'][x].round(3) > 0.0:
            print("Ticker: ",ticker, "\tWeight: ",optimum['x'][x].round(3))
            port.append([ticker,optimum['x'][x].round(3)])
        x+=1
    with open(output_directory + output_portfolio_name,"wb") as f:
        pickle.dump(port,f)
    return port


def show_optimal_portfolio(optimum,returns,preturns,pvariances,report_data_dir):
    plt.figure(figsize=(10,6))
    plt.scatter(pvariances,preturns,c=preturns/pvariances,marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.plot(statistics(optimum['x'],returns)[1],statistics(optimum['x'], returns)[0], 'g*',markersize=20.0)
    graph_name = "Optimum_portfolio.png"
    if not os.path.isdir(report_data_dir):
        os.makedirs(report_data_dir)
    plt.savefig(report_data_dir + graph_name)
    plt.clf()
    

def capm(ticker_data,reference_data,risk_free_rate,ticker_name,report_data_dir):

    #we prefer monthly returns instead of daily returns
    ticker_data = ticker_data.resample('M').last()
    reference_data = reference_data.resample('M').last()

    #creating a dataFrame from the data - Adjusted Closing Price is used as usual
    data = pd.DataFrame({'s_adjclose' : ticker_data['Close'], 'm_adjclose' : reference_data['Close']}, index=ticker_data.index)
    #natural logarithm of the returns
    data[['s_returns', 'm_returns']] = np.log(data[['s_adjclose','m_adjclose']]/data[['s_adjclose','m_adjclose']].shift(1))
    #no need for NaN/missing values values so let's get rid of them
    data = data.dropna()

    #covariance matrix: the diagonal items are the vairances - off diagonals are the covariances
    #the matrix is symmetric: cov[0,1] = cov[1,0] !!!
    covmat = np.cov(data["s_returns"], data["m_returns"])
    print(covmat)
    
    #calculating beta according to the formula
    beta = covmat[0,1]/covmat[1,1]
    print("Beta from formula:", beta)

    #using linear regression to fit a line to the data [stock_returns, market_returns] - slope is the beta
    beta,alpha = np.polyfit(data["m_returns"], data['s_returns'], deg=1)
    print("Beta from regression:", beta)
    
    #plot
    fig,axis = plt.subplots(1,figsize=(20,10))
    axis.scatter(data["m_returns"], data['s_returns'], label="Data points")
    axis.plot(data["m_returns"], beta*data["m_returns"] + alpha, color='red', label="CAPM Line")
    plt.title('Capital Asset Pricing Model, finding alphas and betas for {}'.format(ticker_name))
    plt.xlabel('Market return $R_m$', fontsize=18)
    plt.ylabel('Stock return $R_a$')
    plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
    plt.legend()
    plt.grid(True)
    graph_name = "{}_CAPM_Regression_Plot.png".format(ticker_name)
    if not os.path.isdir(report_data_dir):
        os.makedirs(report_data_dir)
    plt.savefig(report_data_dir + graph_name)
    plt.clf()
    
    
    #calculate the expected return according to the CAPM formula
    expected_return = risk_free_rate + beta*(data["m_returns"].mean()*12-risk_free_rate)
    print("Expected return:", expected_return)
    return covmat,beta,alpha,expected_return

    