visualize\_ML
=============

visualize\_ML is a python package made to visualize some of the steps involved while dealing with a Machine Learning problem. It is build on libraries like matplotlib for visualization and sklearn,scipy for statistical computations.

Table of content:
~~~~~~~~~~~~~~~~~

-  Requirements
-  Install
-  Let’s code

   -  explore module
   -  relation module

-  contribute
-  Licence
-  Copyright

Let’s Code
----------

When we start dealing with a Machine Learning problem some of the
initial steps involved are data exploration,analysis followed by feature
selection.Below are the modules for these tasks.

1) Data Exploration
~~~~~~~~~~~~~~~~~~~

At this stage, we explore variables one by one using **Uni-variate
Analysis** which depends on whether the variable type is categorical or
continuous .To deal with this we have the **explore** module.

>>>explore module
~~~~~~~~~~~~~~~~~~

::

    visualize_ML.explore.plot(data_input,categorical_name=[],drop=[],PLOT_COLUMNS_SIZE=4,bin_size=20,
    bar_width=0.2,wspace=0.5,hspace=0.8)

**Continuous Variables** : In case of continous variables it plots the
*Histogram* for every variable and gives descriptive statistics for
them.

**Categorical Variables** : In case on categorical variables with 2 or
more classes it plots the *Bar chart* for every variable and gives
descriptive statistics for them.

+---------------------+-----------------+---------------------------------------+
| Parameters          | Type            | Description                           |
+=====================+=================+=======================================+
| data\_input         | Dataframe       | This is the input Dataframe with all  |
|                     |                 | data.(Right now the input can be only |
|                     |                 | be a dataframe input.)                |
+---------------------+-----------------+---------------------------------------+
| categorical\_name   | list (default=[ | Names of all categorical variable     |
|                     | ])              | columns with more than 2 classes, to  |
|                     |                 | distinguish them with the continuous  |
|                     |                 | variablesEmply list implies that      |
|                     |                 | there are no categorical features     |
|                     |                 | with more than 2 classes.             |
+---------------------+-----------------+---------------------------------------+
| drop                | list default=[  | Names of columns to be dropped.       |
|                     | ]               |                                       |
+---------------------+-----------------+---------------------------------------+
| PLOT\_COLUMNS\_SIZE | int (default=4) | Number of plots to display vertically |
|                     |                 | in the display window.The row size is |
|                     |                 | adjusted accordingly.                 |
+---------------------+-----------------+---------------------------------------+
| bin\_size           | int             | Number of bins for the histogram      |
|                     | (default=“auto” | displayed in the categorical vs       |
|                     | )               | categorical category.                 |
+---------------------+-----------------+---------------------------------------+
| wspace              | float32         | Horizontal padding between subplot on |
|                     | (default = 0.5) | the display window.                   |
+---------------------+-----------------+---------------------------------------+
| hspace              | float32         | Vertical padding between subplot on   |
|                     | (default = 0.8) | the display window.                   |
+---------------------+-----------------+---------------------------------------+

**Code Snippet**

.. code :: python

    /* The data set is taken from famous Titanic data(Kaggle)*/

    import pandas as pd
    from visualize_ML import explore
    df = pd.read_csv("dataset/train.csv")

    explore.plot(df,["Survived","Pclass","Sex","SibSp","Ticket","Embarked"],drop=["PassengerId","Name"])

.. figure:: /images/explore1.png?raw=true
   :alt: Optional Title

   Graph made using explore module using matplotlib.

see the [dataset](https://www.kaggle.com/c/titanic/data)

**Note:** While plotting all the rows with **NaN** values and columns
with **Character** values are removed only numeric data is plotted.

2) Feature Selection
~~~~~~~~~~~~~~~~~~~~

This is one of the challenging task to deal with for a ML task.Here we
have to do **Bi-variate Analysis** to find out the relationship between
two variables. Here, we look for association and disassociation between
variables at a pre-defined


**relation** module helps in visualizing the analysis done on various
combination of variables and see relation between them.

>>>relation module
~~~~~~~~~~~~~~~~~~~

::

    visualize_ML.relation.plot(df,"Sex",["Survived","Pclass","Sex","SibSp","Ticket","Embarked"],drop=["PassengerId","Name"],bin_size=10)

**Continuous vs Continuous variables:** To do the Bi-variate analysis
*scatter plots* are made as their pattern indicates the relationship
between variables. To indicates the strength of relationship amongst
them we use Correlation between them.

The graph displays the correlation coefficient along with other
information.

::

    Correlation = Covariance(X,Y) / SQRT( Var(X)*Var(Y))

-  -1: perfect negative linear correlation
-  +1:perfect positive linear correlation and
-  0: No correlation

**Categorical vs Categorical variables**: *Stacked Column Charts* are
made to visualize the relation.\ **Chi square test** is used to derive
the statistical significance of relationship between the variables. It
returns *probability* for the computed chi-square distribution with the
degree of freedom. For more information on Chi Test see `this`_

Probability of 0: It indicates that both categorical variable are
dependent

Probability of 1: It shows that both variables are independent.

The graph displays the *p\_value* along with other information. If it is
leass than **0.05** it states that the variables are dependent.

**Categorical vs Continuous variables:** To explore the relation between
categorical and continuous variables,box plots re drawn at each level of
categorical variables. If levels are small in number, it will not show
the statistical significance. **ANOVA test** is used to derive the
statistical significance of relationship between the variables.

The graph displays the *p\_value* along with other information. If it is
leass than **0.05** it states that the variables are dependent.

For more information on ANOVA test see
`this <https://onlinecourses.science.psu.edu/stat200/book/export/html/66>`__

+----------------+-----------+-------------------------------------------------+
| Parameters     | Type      | Description                                     |
+================+===========+=================================================+
| data\_input    | Dataframe | This is the input Dataframe with all            |
|                |           | data.(Right now the input can be only be a      |
|                |           | dataframe input.)                               |
+----------------+-----------+-------------------------------------------------+
| target\_name   | String    | The name of the target column.                  |
+----------------+-----------+-------------------------------------------------+
| categorical\_n | list      | Names of all categorical variable columns with  |
| ame            | (default= | more than 2 classes, to distinguish them with   |
|                | [         | the continuous variablesEmply list implies that |
|                | ])        | there are no categorical features with more     |
|                |           | than 2 classes.                                 |
+----------------+-----------+-------------------------------------------------+
| drop           | list      | Names of columns to be dropped.                 |
|                | default=[ |                                                 |
|                | ]         |                                                 |
+----------------+-----------+-------------------------------------------------+
| PLOT\_COLUMNS\ | int       | Number of plots to display vertically in the    |
| _SIZE          | (default= | display window.The row size is adjusted         |
|                | 4)        | accordingly.                                    |
+----------------+-----------+-------------------------------------------------+
| bin\_size      | int       | Number of bins for the histogram displayed in   |
|                | (default= | the categorical vs categorical category.        |
|                | “auto”)   |                                                 |
+----------------+-----------+-------------------------------------------------+
| wspace         | float32   | Horizontal padding between subplot on the       |
|                | (default  | display window.                                 |
|                | = 0.5)    |                                                 |
+----------------+-----------+-------------------------------------------------+
| hspace         | float32   | Vertical padding between subplot on the display |
|                | (default  | window.                                         |
|                | = 0.8)    |                                                 |
+----------------+-----------+-------------------------------------------------+

**Code Snippet**

.. code :: python

    /* The data set is taken from famous Titanic data(Kaggle)*/
    import pandas as pd
    from visualize_ML import relation
    df = pd.read_csv("dataset/train.csv")

    relation.plot(df,"Survived",["Survived","Pclass","Sex","SibSp","Ticket","Embarked"],drop=["PassengerId","Name"],bin_size=10)

.. figure:: /images/relation1.png?raw=true
   :alt: Optional Title

   Graph made using relation module using matplotlib.

see the [dataset](https://www.kaggle.com/c/titanic/data)

**Note:** While plotting all the rows with **NaN** values and columns
with **Non numeric** values are removed only numeric data is
plotted.Only categorical taget variable with string values are allowed.

Contribute
----------

If you want to contribute and add new feature feel free to send Pull
request `here`_

This project is still under development so to report any bugs or request new features, head over to the Issues page

Licence
-------
Licensed under `The MIT License (MIT)`_.

Copyright
---------
ayush1997(c) 2016

.. _here: https://github.com/ayush1997/visualize_ML
.. _The MIT License (MIT): https://github.com/ayush1997/visualize_ML/blob/master/LICENSE.txt
