# stock-comparison

**A Simple Comparison and Visualization of Stock Data**
This program makes use of the numpy, scipy, and sklearn libraries to find relations between pairs of stock indecies. For each index we have at most 5 years of data on openning and closing prices. 

Before testing correlation between the pairs it was necessary to  standardize the price data for each index. Because the indecies trade at different volumes, the standardization allowed us to see a better picure of the correlation (i.e. we want to know the relative changes in price not the actual). After standardiazation, simply get the covariance matrix for whichever pair of stocks and find the correlation 

Finally, the program takes the highest, lowest, and most opposingly correlated stocks and prints their price data to a scatter plot that is collored for time. The color scale below can serve as a reference (yellow is earlier dates,  dark blue is later).
![index.png]({{site.baseurl}}/index.png)

Finally we plotted the distribution of stock prices and fit a gaussian normal.

The end product was a matpoltlib visualization for each pair that looked like this...

![screen.png]({{site.baseurl}}/screen.png)

