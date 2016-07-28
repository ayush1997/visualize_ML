'''parameters

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# df = pd.read_csv("train_new.csv")
# df = pd.read_csv("train.csv")
df = pd.read_csv("Train_75Dkybb.csv")
# print df.head()
# print type(df["Applicant_BirthDate"][0])
# print df.shape
# print type(df.ix[:,10]).__name__
# print df.ix[:,8].dtype
# print pd.__name__
a = np.array(df)

fig = plt.figure()
fig.subplots_adjust(bottom=0.04,left = 0.05,right=0.97,top=0.93,wspace = 0.28,hspace = 0.41)


# fig = plt.figure(figsize=())

PLOT_COLUMNS_SIZE = 4
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
        res = any(isinstance(n,str) for n in df[i])
        # if i == "Cabin":
        #     print "found"
        #     print [type(n) for n in df[i]]
        print res
        if res == True:
            rem.append(i)

    for j in rem:
        lst.remove(j)

    return lst



def univariate_analysis_continous(cont_list,df,sub,COUNTER,bin_size,PLOT_ROW_SIZE):
    # res = all(isinstance(n,str) for n in df["Age"])
    # print res
    # print isinstance(df["Name"][0],str)


    # print df.describe()
    clean_cont_list = clean_str_list(df,cont_list)
    print clean_cont_list
    for col in cont_list:
        summary = df[col].dropna().describe()
        count = summary[0]
        mean = summary[1]
        std = summary[2]
        count_50 = summary[5]
        count_75 = summary[6]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean: "+str(np.float32(mean))+" std: "+str(np.float32(std)),fontsize=12)
        x = np.array(df[col].dropna())
        plt.xlabel(col+"\n count "+str(count)+"\n50%: "+str(count_50)+" 75%: "+str(count_75), fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.hist(x,bins=bin_size)
        COUNTER +=1

    return plt,COUNTER
        # print x

#Returns the frequecy table for a class
def get_catg_info(df,col):



    return df[col].value_counts()



def univariate_analysis_categorical(catg_list,df,sub_len,COUNTER,bar_width,PLOT_ROW_SIZE):

    # print df.describe()
    clean_catg_list = clean_str_list(df,catg_list)
    print clean_catg_list
    for col in catg_list:
        summary = df[col].dropna().describe()
        # print summary
        count = summary[0]
        mean = summary[1]
        std = summary[2]
        count_50 = summary[5]
        count_75 = summary[6]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=12)
        x = df.dropna()[col].unique()

        y = get_catg_info(df.dropna(),col)
        print y
        y = np.float32([y[i] for i in x])

        print "returnd",y
        labels = y/y.sum() * 100
        print labels
        # print "inout",x
        print x.shape,y.shape

        plt.xlabel(col+"\n count "+str(count)+"\n50%: "+str(count_50)+" 75%: "+str(count_75), fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.bar(x,y,width=bar_width)

        for x,y, label in zip(x,y, np.around(np.float32(labels), decimals=2)):
            plt.text(x + bar_width/2,y + 5, label, ha='center', va='bottom',rotation=90)
        COUNTER +=1

    return plt,COUNTER
        # print x




def plot(data_input,categorical_name=[],bin_size=20,bar_width=0.2,wspace=0.5,hspace=0.8):

    if type(data_input).__name__ == "DataFrame" :

        # Column names
        columns_name = data_input.columns.values
        print columns_name
        #Subplot(Total number of graphs)
        subplot = len(columns_name)
        if subplot < PLOT_COLUMNS_SIZE:
            subplot = PLOT_COLUMNS_SIZE
        PLOT_ROW_SIZE = subplot/PLOT_COLUMNS_SIZE
        PLOT_ROW_SIZE = 5


        #Checks if the categorical_name are present in the orignal dataframe columns.
        categorical_is_present = is_present(columns_name,categorical_name)
        if categorical_is_present:
            category_dict,catg_list,cont_list = get_category(data_input,categorical_name,columns_name)


        plot,count = univariate_analysis_continous(cont_list,data_input,subplot,COUNTER,bin_size,PLOT_ROW_SIZE)
        plot,count = univariate_analysis_categorical(catg_list,data_input,subplot,count,bar_width,PLOT_ROW_SIZE)

        # p.autoscale(True)
        plot.subplots_adjust(wspace = wspace,hspace=hspace)
        # plot.tight_layout()
        plot.show()
        #The DataFrame is converted to numpy array
        data_input_new = dataframe_to_numpy(data_input)
        # print type(data_input_new)
        # print data_input_new
        #Converted the numpy to its transpose for better access
        data_input_new = data_input_new.T
        # print data_input_new



col = ['ID', 'Office_PIN', 'Application_Receipt_Date', 'Applicant_City_PIN', 'Applicant_Gender', 'Applicant_BirthDate', 'Applicant_Marital_Status', 'Applicant_Occupation', 'Applicant_Qualification', 'Manager_DOJ', 'Manager_Joining_Designation', 'Manager_Current_Designation', 'Manager_Grade', 'Manager_Status', 'Manager_Gender', 'Manager_DoB', 'Manager_Num_Application', 'Manager_Num_Coded', 'Manager_Business', 'Manager_Num_Products', 'Manager_Business2', 'Manager_Num_Products2', 'Business_Sourced']

# print df.columns.values.tolist()
# ['ID', 'Applicant_Gender', 'Applicant_Occupation', 'Applicant_Qualification', 'Manager_Status', 'Manager_Gender', 'Manager_Num_Application', 'Manager_Business', 'Manager_Business2', 'Business_Sourced', 'App_age', 'Manager_age'

plot(df)


# print df["Manager_Status"].value_counts()
# print type(df["Manager_Status"].value_counts())
# print df["Manager_Status"].unique()
# print type(df["Manager_Status"].unique())
