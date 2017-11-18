import sqlite3
import numpy
from datetime import date
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn import preprocessing
import itertools


def str2date(datestr):
    (y,m,d) = datestr.split('-')
    return date(int(y), int(m), int(d))


def single_stock_data(data, name):
    data_mean = numpy.mean(data)
    data_median = numpy.median(data)
    data_stddev = numpy.std(data)
    data_var = numpy.var(data)
    data_min = numpy.amin(data)
    data_max = numpy.amax(data)
    ret_string = ''.join([
        "Stock {} \n".format(name),
        "Mean price : {:.2f}\n".format(data_mean),
        "Median price {:.2f}\n".format(data_median),
        "Max price : {:.2f}\n".format(data_max),
        "Min price : {:.2f}\n".format(data_min),
        "Variance : {:.2f}\n".format(data_var),
        "Std Dev  : {:.2f}\n\n".format(data_stddev)
    ])
    return ret_string

def print_dual_scatter(x_name, y_name, x_stock, y_stock2 ):
    colors = [float(days/ len(x_stock)) for days in range(len(x_stock))]
    plt.scatter(x_stock, y_stock2, alpha=.5, c=colors, cmap=plt.cm.get_cmap(name='YlGnBu'))
    plt.xlabel(x_name, fontsize=14)
    plt.ylabel(y_name, fontsize=14)
    plt.title("Stock Comparison")
    plt.plot()
    plt.grid(True)
    plt.subplots_adjust(right=1.4, hspace=.2)

def print_distro(data, name, standard=False):
    if(standard is False):
        standardized = preprocessing.scale(data)
    else:
        standardized = data
    normal = norm.fit(standardized)
    x = numpy.linspace(-3.5, 3.5, 100)
    pdf = norm.pdf(x, loc=normal[0], scale=normal[1])
    plt.hist(standardized, normed=True, bins=50)

    plt.title("{} Distribution".format(name))
    plt.plot(x, pdf, 'r-')
    plt.grid(True)
    plt.subplots_adjust(right=1.4, hspace=.5)


def print_graphs(name_1, name_2, stk_1, stk_2 ):
    std_1 = preprocessing.scale(stk_1)
    std_2 = preprocessing.scale(stk_2)

    #
    plt.subplot(321)
    print_dual_scatter(name_1, name_2, stk_1, stk_2 )

    plt.subplot(323)
    print_distro(stk_1, name_1)

    plt.subplot(325)
    print_distro(stk_2, name_2)

    sidebar = single_stock_data(stk_1, name_1) \
              + single_stock_data(stk_2, name_2) \
              + "Covariance Matrix \n" \
              + str(numpy.cov(std_1, std_2))
    plt.text(4.2, .55, sidebar)

def query_pair(sym_1, sym_2):
    # Build query
    start_date = '2012-09-14'
    end_date = '2017-09-14'
    query = "SELECT " \
            "   s1.sdate, " \
            "   s1.sym, " \
            "   s1.open, " \
            "   s2.sym, " \
            "   s2.open " \
            "FROM stock s1 " \
            "JOIN stock s2 ON 1=1 " \
            "   AND s1.sdate = s2.sdate " \
            "WHERE 1=1 " \
            "   AND s1.sym = \"{}\" " \
            "   AND s2.sym = \"{}\" " \
            "   AND s1.open != \"null\" " \
            "   AND s2.open != \"null\" " \
            "   AND s1.sdate BETWEEN \'{}\' AND \'{}\' " \
            "ORDER BY s1.sdate ASC"

    cursr.execute(query.format(sym_1, sym_2, start_date, end_date))
    prices = cursr.fetchall()
    prices_1 = [row[2] for row in prices]
    prices_2 = [row[4] for row in prices]
    return prices_1, prices_2





# Connect to DB
storage = 'sqlite_data/'
database = storage + 'stocks.db'
conn = sqlite3.connect(database)
cursr = conn.cursor()

# Get all stock symbols
# BABA corrupted the db for some reason,fix later
query = "SELECT sym FROM stock WHERE sym != 'BABA' GROUP BY sym "
cursr.execute(query)
symbols = [row[0] for row in cursr.fetchall()]



# Run query on all data, find combos with highest and lowest correlation
high_corr = 0
anti_corr = low_corr = 1
high_combo = anti_combo = low_combo = tuple()

prices1 = []
prices2 = []
for combo in itertools.combinations(symbols, 2):
    (stock1, stock2) = combo
    prices1, prices2 = query_pair(stock1, stock2)

    std_1 = preprocessing.scale(prices1)
    std_2 = preprocessing.scale(prices2)
    covar = numpy.cov(std_1, std_2)
    corr = covar[0][1]
    if(corr > high_corr):
        high_corr = corr
        high_combo = combo
    if(corr < anti_corr):
        anti_corr = corr
        anti_combo = combo
    if(float(abs(corr)) < low_corr):
        low_corr = corr
        low_combo = combo

# Pull data for anti combo
(stock1,stock2) = anti_combo
prices1, prices2 = query_pair(stock1, stock2)
#Graph anti correlation figure
fig1 = plt.figure()
fig1.canvas.set_window_title('Anti Correlation')
print_graphs(stock1, stock2, prices1, prices2)

#Pull data for high combo
(stock1,stock2) = high_combo
prices1, prices2 = query_pair(stock1, stock2)
#Graph high correlation figure
fig2 = plt.figure()
fig2.canvas.set_window_title('High Correlation')
print_graphs(stock1, stock2, prices1, prices2)

#Pull data for low combo
(stock1,stock2) = low_combo
prices1, prices2 = query_pair(stock1, stock2)
#Graph low correlation figure
fig3 = plt.figure()
fig3.canvas.set_window_title('Low Correlation')
print_graphs(stock1, stock2, prices1, prices2)
plt.show()


