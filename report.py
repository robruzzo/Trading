# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 22:31:59 2020

@author: robru
"""


filename = 'portfolio.html'
data_directory = 'data/'

start_html="""   
<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 6px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>

<h2>Optimum Portfolio</h2>

<table>
<tr>
    <th>Ticker</th>
    <th>Weight</th>
    <th>Average Return</th>
    <th>Alpha</th>
    <th>Beta</th>
    <th>Expected Return</th>
    <th>Weighted Beta (Portfolio)</th>
  </tr>
"""

end_html="""
</table>

</body>
</html>
"""



def create_report(report_root,report_data):
    with open(report_root + filename, 'w')as f:
        f.write(start_html)
        for x in range(len(report_data)):
            row=str("<tr>\n\t<th>"+report_data['ticker'][x]+"</th>\n\t<th>"+report_data['weight'][x]+"</th>"+   
            "\n\t<th>"+report_data['avg_ret'][x]+"</th>\n\t<th>"+report_data['alpha'][x]+"</th>"+
            "\n\t<th>"+report_data['beta'][x]+"</th>\n\t<th>"+report_data['exp_ret'][x]+"</th>"+"\n\t<th>"+report_data['weightB'][x]+"</th>\n</tr>\n")
            f.write(row)
        sumRow=str("<tr>\n\t<th>Sharpe:</th>\n\t<th>"+report_data['sharpe'][x]+"</th>\n\t<th></th>\n\t<th></th>\n\t<th></th>\n\t<th>Portfolio Beta:</th>\n\t<th>"+report_data['SumPB'][x]+"</th>\n</tr>\n")
        f.write(sumRow)
        f.write(end_html)
        f.close()
        
