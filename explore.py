import pandas as pd
import numpy as np
from math import ceil
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# df = pd.read_csv("train_new.csv")
# df = pd.read_csv("train.csv")
# df = pd.read_csv("Train_75Dkybb.csv")



fig = plt.figure()

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
    rem=[]
    for i in lst:

        res = any(isinstance(n,str) for n in df[i])
        if res == True:
            rem.append(i)

    for j in rem:
        lst.remove(j)

    return lst


#Univariate analysis for continuous variables is done using histograms and graph summary.
def univariate_analysis_continous(cont_list,df,sub,COUNTER,bin_size,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE):

    clean_cont_list = clean_str_list(df,cont_list)
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
        print col+" plotted...."
        COUNTER +=1

    return plt,COUNTER


#Returns the frequecy table for a class
def get_catg_info(df,col):
    return df[col].value_counts()


#Univariate analysis for categotical variables is done using histograms and graph summary.
def univariate_analysis_categorical(catg_list,df,sub_len,COUNTER,bar_width,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE):
    # clean_catg_list = clean_str_list(df,catg_list)

    for col in catg_list:
        summary = df[col].dropna().describe()
        count = summary[0]
        mean = summary[1]
        std = summary[2]
        count_50 = summary[5]
        count_75 = summary[6]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=12)
        x = df.dropna()[col].unique()

        y = get_catg_info(df.dropna(),col)
        y = np.float32([y[i] for i in x])

        labels = y/y.sum() * 100

        plt.xlabel(col+"\n count "+str(count)+"\n50%: "+str(count_50)+" 75%: "+str(count_75), fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.bar(x,y,width=bar_width)

        for x,y, label in zip(x,y, np.around(np.float32(labels), decimals=2)):
            plt.text(x + bar_width/2,y + 5, label, ha='center', va='bottom',rotation=90)
        print col+" plotted...."
        COUNTER +=1

    return plt,COUNTER

#returns the total number of subplots to be made.
def total_subplots(df,lst):
    clean_df = df.dropna()
    total = [len(clean_str_list(clean_df,i)) for i in lst]
    return sum(total)

#This function returns new categotical list after removing drop values if in case they are written in both drop and categorical_name list.
def remove_drop_from_catglist(drop,categorical_name):
    for col in drop:
        if col in categorical_name:
            categorical_name.remove(col)
    return categorical_name
def plot(data_input,categorical_name=[],drop=[],PLOT_COLUMNS_SIZE = 4,bin_size=20,bar_width=0.2,wspace=0.5,hspace=0.8):

    """
    This is the main function to give Bivariate analysis between the target variable and the input features.

    Parameters
    -----------
    data_input  : Dataframe
            This is the input Dataframe with all data.

    categorical_name : list
            Names of all categorical variable columns with more than 2 classes, to distinguish with the continuous variables.

    drop : list
            Names of columns to be dropped.

    PLOT_COLUMNS_SIZE : int
            Number of plots to display vertically in the display window.The row size is adjusted accordingly.

    bin_size : int ;default="auto"
            Number of bins for the histogram displayed in the categorical vs categorical category.

    wspace : float32 ;default = 0.5
            Horizontal padding between subplot on the display window.

    hspace : float32 ;default = 0.5
            Vertical padding between subplot on the display window.

    -----------

    """
    if type(data_input).__name__ == "DataFrame" :

        # Column names
        columns_name = data_input.columns.values

        #To drop user specified columns.
        if is_present(columns_name,drop):
            data_input = data_input.drop(drop,axis=1)
            columns_name = data_input.columns.values
            categorical_name = remove_drop_from_catglist(drop,categorical_name)
        else:
            raise ValueError("Couldn't find it in the input Dataframe!")


        #Checks if the categorical_name are present in the orignal dataframe columns.
        categorical_is_present = is_present(columns_name,categorical_name)
        if categorical_is_present:
            category_dict,catg_list,cont_list = get_category(data_input,categorical_name,columns_name)


        #Subplot(Total number of graphs)
        total = total_subplots(data_input,[catg_list,cont_list])
        if total < PLOT_COLUMNS_SIZE:
            total = PLOT_COLUMNS_SIZE
        PLOT_ROW_SIZE = ceil(float(total)/PLOT_COLUMNS_SIZE)

        print "=",catg_list
        plot,count = univariate_analysis_continous(cont_list,data_input,total,COUNTER,bin_size,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE)
        plot,count = univariate_analysis_categorical(catg_list,data_input,total,count,bar_width,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE)

        fig.subplots_adjust(bottom=0.08,left = 0.05,right=0.97,top=0.93,wspace = wspace,hspace = hspace)
        plot.show()

    else:
        raise ValueError("The input doesn't seems to be Dataframe")



# col = ['ID', 'Office_PIN', 'Application_Receipt_Date', 'Applicant_City_PIN', 'Applicant_Gender', 'Applicant_BirthDate', 'Applicant_Marital_Status', 'Applicant_Occupation', 'Applicant_Qualification', 'Manager_DOJ', 'Manager_Joining_Designation', 'Manager_Current_Designation', 'Manager_Grade', 'Manager_Status', 'Manager_Gender', 'Manager_DoB', 'Manager_Num_Application', 'Manager_Num_Coded', 'Manager_Business', 'Manager_Num_Products', 'Manager_Business2', 'Manager_Num_Products2', 'Business_Sourced']
#
#
# col = ['ID', 'Applicant_Gender', 'Applicant_Occupation', 'Applicant_Qualification', 'Manager_Status', 'Manager_Gender', 'Manager_Num_Application', 'Manager_Business', 'Manager_Business2', 'Business_Sourced', 'App_age', 'Manager_age']
#
# # plot(df,"Business_Sourced",['ID', 'Applicant_Gender', 'Applicant_Occupation', 'Applicant_Qualification', 'Manager_Status', 'Manager_Gender','Business_Sourced'],PLOT_COLUMNS_SIZE=4,bin_size=10)
#
#
# # plot(df,["ID","Sex","Age","Address","Famsize","Pstatus","Medu","Fedu","Mjob","Fjob","Guardian","Failures","Schoolsup","Famsup","Activities","Nursery","Higher","Internet","Romantic","Famrel","Goout","Health","Grade","Walc"],drop=["ID","Fjob","Guardian"],PLOT_COLUMNS_SIZE=3,bin_size=10,bar_width=1.0,wspace=1.0,hspace=1.0)
#
# # plot(df,"Survived",['PassengerId', 'Pclass','Sex','SibSp' ,'Parch',
# #  'Ticket', 'Cabin' ,'Embarked'])
# # col = ['PassengerId' 'Survived' 'Pczlass' 'Name' 'Sex' 'Age' 'SibSp' 'Parch'
# #  'Ticket' 'Fare' 'Cabin' 'Embarked']
#
# df = pd.read_csv("train_black.csv")
#
# plot(df,['User_ID', 'Product_ID', 'Gender', 'Age', 'Occupation', 'City_Category','Marital_Status', 'Product_Category_1', 'Product_Category_2', 'Product_Category_3'],drop=["User_ID"],bin_size=10)
