import pandas as pd
import numpy as np
from numpy import corrcoef
import matplotlib.pyplot as plt
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif
from math import *
plt.style.use('ggplot')

fig = plt.figure()
COUNTER = 1

#Return the category dictionary,categorical variables list and continuous list for every column in dataframe.
#The categories are assigned as "target(type)_feature(type)"
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
        raise ValueError(str(ls)+" is not present as a column in the data,Please check the name")

#Function returns list of columns with non-numeric data.
def clean_str_list(df,lst):
    rem=[]
    for i in lst:

        res = any(isinstance(n,str) for n in df[i])
        if res == True:
            rem.append(i)

    for j in rem:
        lst.remove(j)

    return lst

#Returns the Pearson Correlation Coefficient for the continous data columns.
def pearson_correlation_cont_cont(x,y):

    return corrcoef(x,y)


# This function is for the bivariate analysis between two continous varibale.Plots scatter plots and shows the coeff for the data.
def bivariate_analysis_cont_cont(cont_cont_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE):

    clean_cont_cont_list = clean_str_list(df,cont_cont_list)

    if len(clean_str_list(df,[target_name])) == 0 and len(cont_cont_list)>0:
        raise ValueError("You seem to have a target variable with string values.")
    clean_df = df.dropna()
    for col in clean_cont_cont_list:
        summary = clean_df[col].describe()
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = clean_df[col]
        y = np.float32(clean_df[target_name])
        corr = pearson_correlation_cont_cont(x,y)

        plt.xlabel(col+"\n count "+str(count)+"\n Corr: "+str(np.float32(corr[0][1])), fontsize=10)
        plt.ylabel(target_name, fontsize=10)
        plt.scatter(x,y)

        print (col+" vs "+target_name+" plotted....")
        COUNTER +=1

    return plt,COUNTER


#Chi test is used to see association between catgorical vs categorical variables.
#Lower Pvalue are significant they should be < 0.05
#chi value = X^2 = summation [(observed-expected)^2/expected]
# The distribution of the statistic X2 is chi-square with (r-1)(c-1) degrees of freedom, where r represents the number of rows in the two-way table and c represents the number of columns. The distribution is denoted (df), where df is the number of degrees of freedom.
#pvalue = p(df>=x^2)

def evaluate_chi(x,y):
    chi,p_val = chi2(x,y)
    return chi,p_val
def bivariate_analysis_catg_catg(catg_catg_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,bin_size="auto"):

    clean_catg_catg_list = clean_str_list(df,catg_catg_list)

    clean_df = df.dropna()

    target_classes =df[target_name].unique()
    label = [str(i) for i in target_classes]

    c = 0
    for col in clean_catg_catg_list:
        summary = clean_df[col].describe()
        binwidth = 0.7

        if bin_size == 'auto':
            bins_size =np.arange(min(clean_df[col].tolist()), max(clean_df[col].tolist()) + binwidth, binwidth)
        else:
            bins_size = bin_size

        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = [np.array(clean_df[clean_df[target_name]==i][col]) for i in target_classes]
        y = clean_df[target_name]

        chi,p_val = evaluate_chi(np.array(clean_df[col]).reshape(-1,1),y)

        plt.xlabel(col+"\n chi: "+str(np.float32(chi[0]))+" / p_val: "+str(p_val[0]), fontsize=10)
        plt.ylabel("Frequency", fontsize=10)
        plt.hist(x,bins=bins_size,stacked=True,label = label)
        plt.legend(prop={'size': 10})

        print (col+" vs "+target_name+" plotted....")

        COUNTER +=1
        c+=1

    return plt,COUNTER

# Analysis of variance (ANOVA) is a collection of statistical models used to analyze the differences among group means and their associated procedures (such as "variation" among and between groups)
#  In its simplest form, ANOVA provides a statistical test of whether or not the means of several groups are equal, and therefore generalizes the t-test to more than two groups. ANOVAs are useful for comparing (testing) three or more means (groups or variables) for statistical significance.
# A one-way ANOVA is used to compare the means of more than two independent groups. A one-way ANOVA comparing just two groups will give you the same results as the independent t test.
def evaluate_anova(x,y):
    F_value,pvalue = f_classif(x,y)
    return F_value,pvalue

# In descriptive statistics, a box plot or boxplot is a convenient way of graphically depicting groups of numerical data through their quartiles. Box plots may also have lines extending vertically from the boxes (whiskers) indicating variability outside the upper and lower quartiles, hence the terms box-and-whisker plot and box-and-whisker diagram.
# Quartile: In descriptive statistics, the quartiles of a ranked set of data values are the three points that divide the data set into four equal groups, each group comprising a quarter of the data
def bivariate_analysis_cont_catg(cont_catg_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE):

    clean_cont_catg_list = clean_str_list(df,cont_catg_list)

    if len(clean_str_list(df,[target_name])) == 0 and len(cont_catg_list)>0:
        raise ValueError("You seem to have a target variable with string values.")
    clean_df = df.dropna()

    for col in clean_cont_catg_list:

        col_classes =clean_df[col].unique()

        summary = clean_df[col].describe()
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = [np.array(clean_df[clean_df[col]==i][target_name]) for i in col_classes]
        y = np.float32(clean_df[target_name])

        f_value,p_val = evaluate_anova(np.array(clean_df[col]).reshape(-1,1),y)

        plt.xlabel(col+"\n f_value: "+str(np.float32(f_value[0]))+" / p_val: "+str(p_val[0]), fontsize=10)
        plt.ylabel(target_name, fontsize=10)
        plt.boxplot(x)

        print (col+" vs "+target_name+" plotted....")

        COUNTER +=1

    return plt,COUNTER


# This function is for the bivariate analysis between categorical vs continuous varibale.Plots box plots.
def bivariate_analysis_catg_cont(catg_cont_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE):

    # No need to remove string varible as they are handled by chi2 function of sklearn.
    # clean_catg_cont_list = clean_str_list(df,catg_cont_list)
    clean_catg_cont_list = catg_cont_list
    clean_df = df.dropna()

    for col in clean_catg_cont_list:

        col_classes =df[target_name].unique()

        summary = clean_df[col].describe()
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = [np.array(clean_df[clean_df[target_name]==i][col]) for i in col_classes]
        y = clean_df[target_name]

        f_value,p_val = evaluate_anova(np.array(clean_df[col]).reshape(-1,1),y)

        plt.xlabel(target_name+"\n f_value: "+str(np.float32(f_value[0]))+" / p_val: "+str(p_val[0]), fontsize=10)
        plt.ylabel(col, fontsize=10)
        plt.boxplot(x)

        print (col+" vs "+target_name+" plotted....")

        COUNTER +=1

    return plt,COUNTER

#returns the total number of subplots to be made.
def total_subplots(df,lst):
    clean_df = df.dropna()
    total = [len(clean_str_list(clean_df,i)) for i in lst]
    return sum(total)

# This function returns new categotical list after removing drop values if in case they are written in both drop and categorical_name list.
def remove_drop_from_catglist(drop,categorical_name):
    for col in drop:
        if col in categorical_name:
            categorical_name.remove(col)
    return categorical_name

def plot(data_input,target_name="",categorical_name=[],drop=[],PLOT_COLUMNS_SIZE = 4,bin_size="auto",wspace=0.5,hspace=0.8):
    """
    This is the main function to give Bivariate analysis between the target variable and the input features.

    Parameters
    -----------
    data_input  : Dataframe
            This is the input Dataframe with all data.

    target_name : String
            The name of the target column.

    categorical_name : list
            Names of all categorical variable columns with more than 2 classes, to distinguish with the continuous variables.

    drop : list
            Names of columns to be dropped.

    PLOT_COLUMNS_SIZE : int
            Number of plots to display vertically in the display window.The row size is adjusted accordingly.

    bin_size : int ;default="auto"
            Number of bins for the histogram displayed in the categorical vs categorical category.

    wspace : int ;default = 0.5
            Horizontal padding between subplot on the display window.

    hspace : int ;default = 0.5
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

        if target_name == "":
            raise ValueError("Please mention a target variable")

        #Checks if the categorical_name are present in the orignal dataframe columns.
        categorical_is_present = is_present(columns_name,categorical_name)
        target_is_present = is_present(columns_name,[target_name])
        if categorical_is_present:
            fin_cat_dict,catg_catg_list,cont_cont_list,catg_cont_list,cont_catg_list = get_category(data_input,target_name,categorical_name,columns_name)

        #Subplot(Total number of graphs)
        total = total_subplots(data_input,[cont_cont_list,catg_catg_list,catg_cont_list,cont_catg_list])
        if total < PLOT_COLUMNS_SIZE:
            total = PLOT_COLUMNS_SIZE

        PLOT_ROW_SIZE = ceil(float(total)/PLOT_COLUMNS_SIZE)

        #Call various functions
        plot,count =  bivariate_analysis_cont_cont(cont_cont_list,data_input,target_name,total,COUNTER,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE)
        plot,count =  bivariate_analysis_catg_catg(catg_catg_list,data_input,target_name,total,count,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,bin_size=bin_size)
        plot,count =  bivariate_analysis_cont_catg(cont_catg_list,data_input,target_name,total,count,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE)
        plot,count =  bivariate_analysis_catg_cont(catg_cont_list,data_input,target_name,total,count,PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE)

        fig.subplots_adjust(bottom=0.08,left = 0.05,right=0.97,top=0.93,wspace = wspace,hspace = hspace)
        plot.show()

    else:
        raise ValueError("Make sure input data is a Dataframe.")
