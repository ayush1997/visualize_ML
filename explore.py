'''parameters

'''

import pandas as pd
import numpy as np

df = pd.read_csv("train.csv")
print df.head()
# print df.shape
# print type(df.ix[:,10]).__name__
# print df.ix[:,8].dtype
print pd.__name__
a = np.array(df)
# print a
# print a.T
# print a.shape
# print a.T.shape

import matplotlib.pyplot as plt

PLOT_COLUMNS_SIZE = 3
COUNTER = 1
def dataframe_to_numpy(df):
    return np.array(df)

#Return the category dictionary,categorical variables list and continuous list for every colum in dataframe.
def get_category(df,categorical_name,columns_name):
    cat_dict = {}
    categorical = []
    continous = []
    for col in columns_name:
        if len(df[col].unique())<=2:
            cat_dict[col] = "categorical"
            categorical.append(col)
        elif col in categorical_name:
            cat_dict[col] = "categorical"
            categorical.append(col)
        else:
            cat_dict[col] = "continous"
            continous.append(col)
    print cat_dict
    return cat_dict,categorical,continous

#Return True if the categorical_name are present in the orignal dataframe columns.
def is_present(columns_name,categorical_name):
    ls = [i for i in categorical_name if i not in columns_name]
    if len(ls)==0:
        return True
    else:
        raise ValueError(i+" is not present as a column in the data,Please check the name")

#function removes any column with string values which cannt be plotted
def clean_str_list(df,lst):
    print lst
    rem=[]
    for i in lst:
        # print df[i]
        res = all(isinstance(n,str) for n in df[i])
        print res
        if res == True:
            rem.append(i)

    for j in rem:
        lst.remove(j)

    return lst

def univariate_analysis_continous(cont_list,df,sub,COUNTER):
    # res = all(isinstance(n,str) for n in df["Age"])
    # print res
    # print isinstance(df["Name"][0],str)

    clean_cont_list = clean_str_list(df,cont_list)
    print clean_cont_list


    for col in cont_list:
        plt.subplot(3,4,COUNTER)
        x = np.array(df[col].dropna())
        plt.xlabel(col, fontsize=12)
        plt.ylabel("count", fontsize=12)
        plt.hist(x,bins=100)
        COUNTER +=1

    return plt,COUNTER
        # print x




def plot(data_input,data_output,categorical_name):
    # if isinstance(data_input, DataFrame):
    if type(data_input).__name__ == "DataFrame" :

        # Column names
        columns_name = data_input.columns.values
        print columns_name
        #Subplot(Total number of graphs)
        subplot = len(columns_name)

        #Checks if the categorical_name are present in the orignal dataframe columns.
        categorical_is_present = is_present(columns_name,categorical_name)
        if categorical_is_present:
            category_dict,catg_list,cont_list = get_category(data_input,categorical_name,columns_name)


        plt,count = univariate_analysis_continous(cont_list,data_input,subplot,COUNTER)

        plt.show()
        #The DataFrame is converted to numpy array
        data_input_new = dataframe_to_numpy(data_input)
        # print type(data_input_new)
        # print data_input_new
        #Converted the numpy to its transpose for better access
        data_input_new = data_input_new.T
        # print data_input_new





plot(df,df.ix[:,:8],["Sex","Survived","Pclass","SibSp","Parch","Ticket","Cabin","Embarked"])
