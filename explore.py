'''parameters

'''

import pandas as pd
import numpy as np

df = pd.read_csv("train.csv")
# print df.head()
# print df.shape
print type(df.ix[:,10]).__name__
print df.ix[:,8].dtype
print pd.__name__
a = np.array(df)
print a
# print a.T
# print a.shape
# print a.T.shape

import matplotlib.pyplot as plt

def dataframe_to_numpy(df):
    return np.array(df)

#Return the category dictionary for every colum in dataframe.
def get_category(df,categorical_name,columns_name):
    cat_dict = {}
    for col in columns_name:
        if len(df[col].unique())<=2:
            cat_dict[col] = "categorical"
        elif col in categorical_name:
            cat_dict[col] = "categorical"
        else:
            cat_dict[col] = "continous"
    print cat_dict
    return cat_dict

#Return True if the categorical_name are present in the orignal dataframe columns.
def is_present(columns_name,categorical_name):
    ls = [i for i in categorical_name if i not in columns_name]
    if len(ls)==0:
        return True
    else:
        raise ValueError(i+" is not present as a column in the data,Please check the name")


def plot(data_input,data_output,categorical_name):
    # if isinstance(data_input, DataFrame):
    if type(data_input).__name__ == "DataFrame" :

        # Column names
        columns_name = data_input.columns.values
        # print columns_name

        #Checks if the categorical_name are present in the orignal dataframe columns.
        categorical_is_present = is_present(columns_name,categorical_name)
        if categorical_is_present:
            category_dict = get_category(data_input,categorical_name,columns_name)

        #The DataFrame is converted to numpy array
        data_input_new = dataframe_to_numpy(data_input)
        # print type(data_input_new)
        # print data_input_new
        #Converted the numpy to its transpose for better access
        data_input_new = data_input_new.T
        # print data_input_new





plot(df,df.ix[:,:8],["Sex"])
