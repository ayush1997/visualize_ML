'''parameters

'''

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif

plt.style.use('ggplot')
# df = pd.read_csv("train_new.csv")
df = pd.read_csv("train.csv")
# df = pd.read_csv("Train_75Dkybb.csv")
# df = pd.read_csv("Train_pjb2QcD.csv")

# print df[df["Business_Sourced"]==0]["Manager_Grade"]
a = np.array(df)

fig = plt.figure()
fig.subplots_adjust(bottom=0.04,left = 0.05,right=0.97,top=0.93,wspace = 0.28,hspace = 0.66)

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
        # print summary
        # print summary
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = df[col]
        y = np.float32(df[target_name])
        corr = pearson_correlation_cont_cont(x,y)
        # print "returnd",y

        # print x.shape,y.shape

        plt.xlabel(col+"\n count "+str(count)+"\n Corr: "+str(np.float32(corr[0])), fontsize=10)
        plt.ylabel(target_name, fontsize=10)
        plt.scatter(x,y)

        COUNTER +=1

    return plt,COUNTER


#Chi test it used to see association between catgorical vs categorical variables.
#Lower Pvalue are significant they should be < 0.05
#chi value = X^2 = summation [(observed-expected)^2/expected]
# The distribution of the statistic X2 is chi-square with (r-1)(c-1) degrees of freedom, where r represents the number of rows in the two-way table and c represents the number of columns. The distribution is denoted (df), where df is the number of degrees of freedom.
#pvalue = p(df>=x^2)
def evaluate_chi(x,y):
    chi,p_val = chi2(x,y)
    return chi,p_val
def bivariate_analysis_catg_catg(catg_catg_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE,bin_size="auto"):

    # print df.describe()
    clean_catg_catg_list = clean_str_list(df,catg_catg_list)
    print clean_catg_catg_list
    clean_df = df.dropna()

    target_classes =df[target_name].unique()
    label = [str(i) for i in target_classes]
    print target_classes
    c = 0
    for col in clean_catg_catg_list:
        summary = clean_df[col].describe()
        print summary
        binwidth = 0.7

        if bin_size == 'auto':
            bins_size =np.arange(min(clean_df[col].tolist()), max(clean_df[col].tolist()) + binwidth, binwidth)
        else:
            bins_size = bin_size
        # print summary
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = [np.array(clean_df[clean_df[target_name]==i][col]) for i in target_classes]
        y = np.float32(clean_df[target_name])

        print y
        print np.array(clean_df[col]).reshape(-1,1).shape

        chi,p_val = evaluate_chi(np.array(clean_df[col]).reshape(-1,1),y)
        print chi,p_val

        plt.xlabel(col+"\n chi: "+str(np.float32(chi[0]))+" / p_val: "+str(p_val[0]), fontsize=10)
        plt.ylabel("Frequency", fontsize=10)
        plt.hist(x,bins=bins_size,stacked=True,label = label)
        # print str(target_classes[c])
        plt.legend(prop={'size': 10})

        COUNTER +=1
        c+=1

    return plt,COUNTER

# Analysis of variance (ANOVA) is a collection of statistical models used to analyze the differences among group means and their associated procedures (such as "variation" among and between groups)
#  In its simplest form, ANOVA provides a statistical test of whether or not the means of several groups are equal, and therefore generalizes the t-test to more than two groups. ANOVAs are useful for comparing (testing) three or more means (groups or variables) for statistical significance.
# A one-way ANOVA is used to compare the means of more than two independent groups. A one-way ANOVA comparing just two groups will give you the same results at the independent t test
def evaluate_anova(x,y):
    F_value,pvalue = f_classif(x,y)
    return F_value,pvalue

# In descriptive statistics, a box plot or boxplot is a convenient way of graphically depicting groups of numerical data through their quartiles. Box plots may also have lines extending vertically from the boxes (whiskers) indicating variability outside the upper and lower quartiles, hence the terms box-and-whisker plot and box-and-whisker diagram.
def bivariate_analysis_cont_catg(cont_catg_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE):

    # print df.describe()
    clean_cont_catg_list = clean_str_list(df,cont_catg_list)
    print clean_cont_catg_list
    clean_df = df.dropna()



    for col in clean_cont_catg_list:

        col_classes =df[col].unique()

        summary = clean_df[col].describe()
        # print summary
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = [np.array(clean_df[clean_df[col]==i][target_name]) for i in col_classes]
        y = np.float32(clean_df[target_name])

        print y
        print np.array(clean_df[col]).reshape(-1,1).shape

        f_value,p_val = evaluate_anova(np.array(clean_df[col]).reshape(-1,1),y)
        print f_value,p_val
        #
        plt.xlabel(col+"\n f_value: "+str(np.float32(f_value[0]))+" / p_val: "+str(p_val[0]), fontsize=10)
        plt.ylabel(target_name, fontsize=10)
        plt.boxplot(x)

        COUNTER +=1

    return plt,COUNTER


def bivariate_analysis_catg_cont(catg_cont_list,df,target_name,sub_len,COUNTER,PLOT_ROW_SIZE):

    # print df.describe()
    clean_catg_cont_list = clean_str_list(df,catg_cont_list)
    print clean_catg_cont_list
    clean_df = df.dropna()



    for col in clean_catg_cont_list:

        col_classes =df[target_name].unique()

        summary = clean_df[col].describe()
        # print summary
        count = summary[0]
        mean = summary[1]
        std = summary[2]

        plt.subplot(PLOT_ROW_SIZE,PLOT_COLUMNS_SIZE,COUNTER)
        plt.title("mean "+str(np.float32(mean))+" std "+str(np.float32(std)),fontsize=10)

        x = [np.array(clean_df[clean_df[target_name]==i][col]) for i in col_classes]
        y = np.float32(clean_df[target_name])

        # print y
        print np.array(clean_df[col]).reshape(-1,1).shape

        f_value,p_val = evaluate_anova(np.array(clean_df[col]).reshape(-1,1),y)
        print f_value,p_val
        #
        plt.xlabel(target_name+"\n f_value: "+str(np.float32(f_value[0]))+" / p_val: "+str(p_val[0]), fontsize=10)
        plt.ylabel(col, fontsize=10)
        plt.boxplot(x)

        COUNTER +=1

    return plt,COUNTER



def plot(data_input,target_name="",categorical_name=[],bin_size="auto",bar_width=0.2,wspace=0.5,hspace=0.8):

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
        plot,count =  bivariate_analysis_catg_catg(catg_catg_list,data_input,target_name,subplot,count,PLOT_ROW_SIZE,bin_size=bin_size)
        plot,count =  bivariate_analysis_cont_catg(cont_catg_list,data_input,target_name,subplot,count,PLOT_ROW_SIZE)
        plot,count =  bivariate_analysis_catg_cont(catg_cont_list,data_input,target_name,subplot,count,PLOT_ROW_SIZE)

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


# plot(df,"Walc",["ID","Sex","Age","Address","Famsize","Pstatus","Medu","Fedu","Mjob","Fjob","Guardian","Failures","Schoolsup","Famsup","Activities","Nursery","Higher","Internet","Romantic","Famrel","Goout","Health","Grade","Walc"])

plot(df,"Survived",['PassengerId', 'Pclass','Sex','SibSp' ,'Parch',
 'Ticket', 'Cabin' ,'Embarked'])
# col = ['PassengerId' 'Survived' 'Pczlass' 'Name' 'Sex' 'Age' 'SibSp' 'Parch'
#  'Ticket' 'Fare' 'Cabin' 'Embarked']
