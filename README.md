# visualize_ML

visualize_ML is a python package made to visualize some of the steps involved while dealing with a Machine Learning problem.


## What to visialize


ddc


## Let's Code

When we start dealing with a Machine Learning problem some of the initial steps involved are data exploration,analysis followed by feature selection.Below are the modules for these tasks.

### 1) Data Exploration
At this stage, we explore variables one by one using **Uni-variate Analysis** which depends on whether the variable type is categorical or continuous .To deal with this we have the **explore** module.

### >>> explore module
	visualize_ML.explore.plot(data_input,categorical_name=[],drop=[],PLOT_COLUMNS_SIZE=4,bin_size=20,
	bar_width=0.2,wspace=0.5,hspace=0.8)
**Continuous Variables** : In case of continous variables it plots the *Histogram* for every variable and gives descriptive statistics for them.

**Categorical Variables** : In case on categorical variables with 2 or more classes it plots the *Bar chart* for every variable and gives descriptive statistics for them.

Parameters | Type | Description
------------ | -------------|------------------------------------------------------------------------
data_input  | Dataframe	| This is the input Dataframe with all data.(Right now the input can be only be a dataframe input.)
categorical_name| list (default=[ ])| Names of all categorical variable columns with more than 2 classes, to distinguish them with the continuous variablesEmply list implies that there are no categorical features with more than 2 classes.
drop | list default=[ ]|Names of columns to be dropped.
PLOT_COLUMNS_SIZE| int (default=4)|Number of plots to display vertically in the display window.The row size is adjusted accordingly.
bin_size |int (default="auto") | Number of bins for the histogram displayed in the categorical vs categorical category.
wspace | float32 (default = 0.5) |Horizontal padding between subplot on the display window.
hspace | float32 (default = 0.8) |Vertical padding between subplot on the display window.


**Code Snippet**
```
/* The data set is taken from famous Titanic data(Kaggle)*/
In [1]: import pandas as pd
In [2]: from visualize_ML import explore
In [3]: df = pd.read_csv("dataset/train.csv")
In [4]: explore.plot(df,["Survived","Pclass","Sex","SibSp","Ticket","Embarked"],drop=["PassengerId","Name"])
```
see this example for better understanding.

### 2) Feature Selection
This is one of the challenging task to deal with for a ML task.Here we have to do **Bi-variate Analysis** to find out the relationship between two variables. Here, we look for association and disassociation between variables at a pre-defined significance level.

**relation** module helps in visualizing the analysis done on various combination of variables and see relation between them. 
        
### >>> relation module
	visualize_ML.relation.plot(df,"Sex",["Survived","Pclass","Sex","SibSp","Ticket","Embarked"],drop=["PassengerId","Name"],bin_size=10)
