
# A package to make common predictive analysis easier

**Objective**: To make common analysis easier and more expressive.

To install the package

```
pip install predictive-analytic==0.0.2
```

Let me show you how the package works

## (1) Simple Averaging method, with dynamic window size
**Input [1]**:

```python
from predictive_tools import predictive as p
import pandas as pd

arr = [20, 25, 33, 30, 27, 35, 40, 43, 35, 32, 37, 48, 50, 37, 45]
len_array = len(arr)
answer = [None] * len_array
window_size = 3
p.simple_moving_average(arr, window_size)
```

**Output [1]**:

```
Forecasted result: 44.0
MSE = 54.16461116666665
RMSE = 7.359661076888436
+----+----------+-------------------+------------------------------------+
|    |   Actual |   Forecasted, w=3 | Computation                        |
|----+----------+-------------------+------------------------------------|
|  0 |       20 |           nan     |                                    |
|  1 |       25 |           nan     |                                    |
|  2 |       33 |           nan     |                                    |
|  3 |       30 |            26     | sum([20, 25, 33]) / (3)  =  26.0   |
|  4 |       27 |            29.333 | sum([25, 33, 30]) / (3)  =  29.333 |
|  5 |       35 |            30     | sum([33, 30, 27]) / (3)  =  30.0   |
|  6 |       40 |            30.667 | sum([30, 27, 35]) / (3)  =  30.667 |
|  7 |       43 |            34     | sum([27, 35, 40]) / (3)  =  34.0   |
|  8 |       35 |            39.333 | sum([35, 40, 43]) / (3)  =  39.333 |
|  9 |       32 |            39.333 | sum([40, 43, 35]) / (3)  =  39.333 |
| 10 |       37 |            36.667 | sum([43, 35, 32]) / (3)  =  36.667 |
| 11 |       48 |            34.667 | sum([35, 32, 37]) / (3)  =  34.667 |
| 12 |       50 |            39     | sum([32, 37, 48]) / (3)  =  39.0   |
| 13 |       37 |            45     | sum([37, 48, 50]) / (3)  =  45.0   |
| 14 |       45 |            45     | sum([48, 50, 37]) / (3)  =  45.0   |
| 15 |      nan |            44     | sum([50, 37, 45]) / (3)  =  44.0   |
+----+----------+-------------------+------------------------------------+
```
## (2) Weighted Averaging Methods, with dynamic window size
**Input [2]**:
```python
arr = [18,19,18,19,26,30]
window_size = 3
weights = [0.2,0.3,0.5] # it has more weights in later period, which is designed in ascending order. Take note that the size must equal to the window size.
p.simple_moving_average(arr, window_size, weights)
```

**Output [2]**:
```
Forecasted result: 26.6
MSE = 37.690000000000005
RMSE = 6.1392181912683315

+----+----------+-------------------+-------------------------------+
|    |   Actual |   Forecasted, w=3 | Computation                   |
|----+----------+-------------------+-------------------------------|
|  0 |       18 |             nan   |                               |
|  1 |       19 |             nan   |                               |
|  2 |       18 |             nan   |                               |
|  3 |       19 |              18.3 | sum([3.6, 5.7, 9.0]) =  18.3  |
|  4 |       26 |              18.7 | sum([3.8, 5.4, 9.5]) =  18.7  |
|  5 |       30 |              22.3 | sum([3.6, 5.7, 13.0]) =  22.3 |
|  6 |      nan |              26.6 | sum([3.8, 7.8, 15.0]) =  26.6 |
+----+----------+-------------------+-------------------------------+
```
## (3) Exponential smoothing Method
**Input [3]**:
```python
d = {'year':[2000,2001,2002,2003,2004,2005], 'Y':[18,19,18,19,26,30]}
df = pd.DataFrame(d)
p.exponential_weighted(df, 'Y')
```

**Output [2]**:
```
Forecasted Answer: 28.148670000000003
MSE = 22.892686052500004
RMSE = 4.784630189732536

+----+--------+-----+---------+-------------------------------------------+
|    |   year |   Y |     f_t | computation                               |
|----+--------+-----+---------+-------------------------------------------|
|  0 |   2000 |  18 | 18      | nan                                       |
|  1 |   2001 |  19 | 18      | nan                                       |
|  2 |   2002 |  18 | 18.7    | (19.0 * 0.7) + (0.3 * 18.0)               |
|  3 |   2003 |  19 | 18.21   | (18.0 * 0.7) + (0.3 * 18.7)               |
|  4 |   2004 |  26 | 18.763  | (19.0 * 0.7) + (0.3 * 18.21)              |
|  5 |   2005 |  30 | 23.8289 | (26.0 * 0.7) + (0.3 * 18.762999999999998) |
|  6 |    nan | nan | 28.1487 | (30.0 * 0.7) + (0.3 * 23.8289)            |
+----+--------+-----+---------+-------------------------------------------+

```


## (4) Least Squared Method
**Input [3]**:
```python
d = {'year':[1991,1992,1993,1994,1995], 'Y':[8,9,8,9,16]}
df = pd.DataFrame(d)
p.least_square(df, 'year', 'Y')
```
**Output [3]**:
```
diff_list = [1 1 1 1]
interval of time = 1.0
bench_time_index = 1990.0

N = 5
Sum_of_X = 15.0
Sum_of_Y = 50
Sum_of_XY = 166.0
Sum_of_X_Squared = 55.0

Sum_of_Y = N*a + Sum_of_X*b
50 = 5*a + 15.0*b

Sum_of_XY = Sum_of_X*a + Sum_of_X_Squared*b
166.0 = 15.0*a + 55.0*b

5*a + 15.0*b - 50
15.0*a + 55.0*b - 166.0

Final equation after solving 'a' and 'b'
Y_1996 = a + b*(6.0)

the answer: {a: 5.20000000000000, b: 1.60000000000000}
Y_1996 = 5.20000000000000 + 1.60000000000000 *6.0
Y_1996 = 14.8000000000000
MSE = 4.080000000000002
RMSE = 2.019900987672416
```

This is contributed by [Morris Lee](http://www.morris-lee.com/).
