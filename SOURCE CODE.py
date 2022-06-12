def simple_moving_average(arr, window_size, weights=None):
    from sklearn.metrics import mean_squared_error
    import math
    import numpy as np
    import pandas as pd
    i = 0
    len_array = len(arr)+1
    answer = [None] * len_array ; computation = [None] * len_array 
    row = window_size
    # Initialize an empty list to store moving averages
    moving_averages = []

    # Loop through the array t o
    #consider every window of size 3
    while i < len(arr) - window_size + 1:

        # Calculate the average of current window
        if weights ==None:
            array_values = arr[i:i+window_size]
            window_average = round(np.sum(array_values) / window_size, 3)
#             print(f"window_average_of_{window_size} = sum({array_values}) / ({window_size})  =  {window_average}") 
            answer[row] = window_average
            computation[row] = (f" sum({array_values}) / ({window_size})  =  {window_average}")
            row+=1
        else:
            array_values = arr[i:i+window_size]
            array_values_multiplied = [a * b for a, b in zip(array_values, weights)]
            array_values_multiplied = [round(num, 4) for num in array_values_multiplied]
            window_average = round(np.sum(array_values_multiplied), 4)
#             print(f"window_average_of_{window_size} = sum({array_values_multiplied}) =  {window_average}") 
            answer[row] = window_average
            computation[row] = (f"sum({array_values_multiplied}) =  {window_average}") 
            row+=1
        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
        # Shift window to right by one position
        i += 1
    arr.append(None)
    d = {'Actual': arr, f'Forecasted, w={window_size}':answer, 'Computation':computation}
    df_result = pd.DataFrame(d)
    
    print(f"Forecasted result: {answer[-1]}")
    
    df_metric =  df_result.dropna()
    y_actual = df_metric['Actual'].values.tolist()
    y_predicted  = df_metric[f'Forecasted, w={window_size}'].values.tolist()

    MSE = mean_squared_error(y_actual, y_predicted)
    RMSE = math.sqrt(MSE)
    print(f"MSE = {MSE}")
    print(f"RMSE = {RMSE}")
    
    return df_result


def exponential_weighted(df, Y):
    from sklearn.metrics import mean_squared_error
    import math
    import numpy as np
    first_time_index = df.iloc[0][Y]
    df['f_t'] = first_time_index
    df['computation'] = np.nan
    df.loc[df.shape[0]] = np.nan
    temp = 2
    alpha=0.7
    while temp+1 <= len(df):
        value = ((df.iloc[temp-1][Y])*alpha) +((1-alpha)*(df.iloc[temp-1]['f_t']))
        df.loc[temp,'f_t'] = value
        df.loc[temp,'computation'] = f"({(df.iloc[temp-1][Y])} * {alpha}) + ({round(1-alpha,2)} * {(df.iloc[temp-1]['f_t'])})"
        temp+=1
    print(f"Forecasted Answer: {df.iloc[-1]['f_t']}")
    df_metric =  df.dropna()
    y_actual = df_metric[Y].values.tolist()
    y_predicted  = df_metric['f_t'].values.tolist()

    MSE = mean_squared_error(y_actual, y_predicted)
    RMSE = math.sqrt(MSE)
    print(f"MSE = {MSE}")
    print(f"RMSE = {RMSE}")
    print()
    return df

def least_square(df, time, Y, plot=False):


    from sympy import symbols, Eq, solve
    from sympy.parsing.sympy_parser import parse_expr
    import numpy as np
    import math
    from sklearn.metrics import mean_squared_error
    from IPython.display import display

    t = df[time].tolist()
    diff_list = np.diff(t)
    print(f"diff_list = {diff_list}")
    diff = np.diff(t).mean()
    print(f"interval of time = {diff}")

    first_time_index = df.iloc[0][time]
    bench_time_index = first_time_index - diff
    print(f"bench_time_index = {bench_time_index}")
    print()

    ###

    X = f'deviation from {int(bench_time_index)} (X)'
    df[X] = df[time] - bench_time_index
    df['XY'] = df[X] * df[Y]
    df['X Squared'] = df[X] * df[X]
    
    display(df)
    
    ###
    N = len(df) ; print(f"N = {N}")
    Sum_of_X = df[X].sum() ; print(f"Sum_of_X = {Sum_of_X}")
    Sum_of_Y = df[Y].sum() ; print(f"Sum_of_Y = {Sum_of_Y}")
    Sum_of_XY = df["XY"].sum() ; print(f"Sum_of_XY = {Sum_of_XY}")
    Sum_of_X_Squared = df["X Squared"].sum() ; print(f"Sum_of_X_Squared = {Sum_of_X_Squared}")
    print()

    ###
    print(f"{'Sum_of_Y'} = {'N'}*a + {'Sum_of_X'}*b")
    print(f"{Sum_of_Y} = {N}*a + {Sum_of_X}*b")
    print()
    print(f"{'Sum_of_XY'} = {'Sum_of_X'}*a + {'Sum_of_X_Squared'}*b")
    print(f"{Sum_of_XY} = {Sum_of_X}*a + {Sum_of_X_Squared}*b")

    if Sum_of_Y >=0:
        eq1_text = f"{N}*a + {Sum_of_X}*b - {Sum_of_Y}"
    else:
        eq1_text = f"{N}*a + {Sum_of_X}*b + {Sum_of_Y}"

    if Sum_of_XY>=0:
        eq2_text = f"{Sum_of_X}*a + {Sum_of_X_Squared}*b - {Sum_of_XY}"
    else:
        eq2_text = f"{Sum_of_X}*a + {Sum_of_X_Squared}*b + {Sum_of_XY}"
    
    a, b = symbols('a b')
    eq1 = Eq(parse_expr(eq1_text), 0)
    eq2 = Eq(parse_expr(eq2_text), 0)
    
    
    print()
    print(eq1_text)
    print(eq2_text)
    print()
    ###
    forecast_time_index = df.iloc[-1][time] +diff
    print("Final equation after solving 'a' and 'b'")
    print(f"Y_{int(forecast_time_index)} = a + b*({forecast_time_index- bench_time_index})")
    answer_d = solve((eq1,eq2), (a, b))
#     [{k: round(v, 2) for k, v in dct.items()} for dct in answer_d]
    print()
    
    print(f"the answer: {answer_d}")
    df['Y_c'] = answer_d[a] + (answer_d[b] *df[X])
    display(df)
    print()
    
    print(f"Y_{int(forecast_time_index)} = {answer_d[a]} + {answer_d[b]} *{forecast_time_index- bench_time_index}")
    print(f"Y_{int(forecast_time_index)} = {answer_d[a] + (answer_d[b] *(forecast_time_index- bench_time_index))}")
    
    ###############
    df_metric =  df.dropna()
    y_actual = df_metric[Y].values.tolist()
    y_predicted  = df_metric['Y_c'].values.tolist()

    MSE = mean_squared_error(y_actual, y_predicted)
    RMSE = math.sqrt(MSE)
    print(f"MSE = {MSE}")
    print(f"RMSE = {RMSE}")
        
    return solve((eq1,eq2), (a, b))
