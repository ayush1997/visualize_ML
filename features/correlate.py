'''parameters

'''

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
plt.style.use('ggplot')
# df = pd.read_csv("train_new.csv")
# df = pd.read_csv("train.csv")
df = pd.read_csv("Train_75Dkybb.csv")
# df = pd.read_csv("Train_pjb2QcD.csv")

# print df[df["Business_Sourced"]==0]["Manager_Grade"]
a = np.array(df)

fig = plt.figure()
fig.subplots_adjust(bottom=0.04,left = 0.05,right=0.97,top=0.93,wspace = 0.28,hspace = 0.41)

# target_classes = [0,1]
# df =df.dropna()
# x = [np.array(df[df["Business_Sourced"]==i]["Manager_Grade"]) for i in target_classes]
# print x
# plt.hist(x,stacked=True)
# plt.show()

# fig = plt.figure(figsize=())

PLOT_COLUMNS_SIZE = 4
COUNTER = 1
def dataframe_to_numpy(df):
    return np.array(df)

#Return the category dictionary,categorical variables list and continuous list for every colum in dataframe.
#The categories are assigned as x vs y axis i.e target(x)- feature(y)
def get_category(df,target_name,categorical_name,columns_name):
    cat_dict = {}
    fin_cat_dict = {}
    catg_catg = []
    cont_cont = []
    catg_cont = []
    cont_catg = []
    for col in columns_name:
        if len(df[col].unique())<=2:
            cat_dict[col] = "categorical"
        elif col in categorical_name:
            cat_dict[col] = "categorical"
        else:
            cat_dict[col] = "continous"
    print cat_dict

    for col in cat_dict:
        if cat_dict[col]=="categorical" and cat_dict[target_name]=="categorical":
            fin_cat_dict[col] = "catg_catg"
            catg_catg.append(col)
        elif cat_dict[col]=="continous" and cat_dict[target_name]=="continous":
            fin_cat_dict[col] = "cont_cont"
            cont_cont.append(col)
        elif cat_dict[col]=="continous" and cat_dict[target_name]=="categorical":
            fin_cat_dict[col] = "catg_cont"
            catg_cont.append(col)
        else:
            fin_cat_dict[col] = "cont_catg"
            cont_catg.append(col)
    return fin_cat_dict,catg_catg,cont_cont,catg_cont,cont_catg

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

def pearson_correlation_cont_cont(x,y):
    return pearsonr(x, y)
# This function is for the bivariate analysis between two continous varibale
def bivariate_analysis_cont_cont(cont_cont_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE):

    # print df.describe()
    clean_cont_cont_list = clean_str_list(df,cont_cont_list)
    print clean_cont_cont_list
    clean_df = df.dropna()
    for col in clean_cont_cont_list:
        summary = clean_df[col].describe()
        print summary
        # print summary
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = df[col]
        y = np.float32(df[target_name])
        corr = pearson_correlation_cont_cont(x,y)
        print "returnd",y

        print x.shape,y.shape

        plt.xlabel(col+"\n count "+str(count)+"\n Corr: "+str(cor), fontsize=10)
        plt.ylabel(target_name, fontsize=10)
        plt.scatter(x,y)

        COUNTER +=1

    return plt,COUNTER

def bivariate_analysis_catg_catg(catg_catg_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE):

    # print df.describe()
    clean_catg_catg_list = clean_str_list(df,catg_catg_list)
    print clean_catg_catg_list
    clean_df = df.dropna()

    target_classes =df[target_name].unique()

    for col in clean_catg_catg_list:
        summary = clean_df[col].describe()
        print summary
        # print summary
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = [np.array(clean_df[clean_df[target_name]==i][col]) for i in target_classes]
        if col == "Studytime":
            print x
        y = np.float32(df[target_name])
        # corr = pearson_correlation_cont_cont(x,y)
        # print "returnd",y

        plt.xlabel(col, fontsize=10)
        plt.ylabel("Frequency", fontsize=10)
        plt.hist(x,stacked=True)

        COUNTER +=1

    return plt,COUNTER





def plot(data_input,target_name="",categorical_name=[],bin_size=20,bar_width=0.2,wspace=0.5,hspace=0.8):

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
            fin_cat_dict,catg_catg_list,cont_cont_list,catg_cont_list,cont_catg_list = get_category(data_input,target_name,categorical_name,columns_name)
        print fin_cat_dict

        plot,count =  bivariate_analysis_cont_cont(cont_cont_list,data_input,target_name,subplot,COUNTER,PLOT_ROW_SIZE)
        plot,count =  bivariate_analysis_catg_catg(catg_catg_list,data_input,target_name,subplot,count,PLOT_ROW_SIZE)

        # p.autoscale(True)
        # plot.subplots_adjust(wspace = wspace,hspace=hspace)
        # plot.tight_layout()
        plot.show()
        #The DataFrame is converted to numpy array
        data_input_new = dataframe_to_numpy(data_input)
        # print type(data_input_new)
        # print data_input_new
        #Converted the numpy to its transpose for better access
        data_input_new = data_input_new.T
        # print data_input_new



col = ['ID', 'Applicant_Gender', 'Applicant_Occupation', 'Applicant_Qualification', 'Manager_Status', 'Manager_Gender', 'Manager_Num_Application', 'Manager_Business', 'Manager_Business2', 'Business_Sourced', 'App_age', 'Manager_age']

# plot(df,"Business_Sourced",['ID', 'Applicant_Gender', 'Applicant_Occupation', 'Applicant_Qualification', 'Manager_Status', 'Manager_Gender','Business_Sourced'])


plot(df,"Walc",["ID","Sex","Age","Address","Famsize","Pstatus","Medu","Fedu","Mjob","Fjob","Guardian","Traveltime","Studytime","Failures","Schoolsup","Famsup","Activities","Nursery","Higher","Internet","Romantic","Famrel","Freetime","Goout","Health","Absences","Grade","Walc"])
