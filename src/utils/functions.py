import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import LearningCurveDisplay, learning_curve, KFold, cross_val_score
import seaborn as sns
from numpy.typing import ArrayLike
import pandas as pd

def cleanData(df):
    '''
    Args:
            df (Pandas DataFrame): A pandas DataFrame to be cleaned and split

    Returns:
            X_train (Pandas DataFrame): Pandas DataFrame with a portion of 80% of the dataframe through *train_test_split* sklearn method 
            X_test (Pandas DataFrame): Pandas DataFrame with a portion of 20% of the dataframe through *train_test_split* sklearn method 
            y_train (Pandas Series): Pandas Series with a portion of 80% of the dataframe through *train_test_split* sklearn method
            y_test (Pandas Series): Pandas Series with a portion of 20% of the dataframe through *train_test_split* sklearn method


    '''
    df.rename(columns={"Unnamed: 0": "ID",
                            "RevolvingUtilizationOfUnsecuredLines": "balance_divided_creditlimit", 
                            "NumberOfTime60-89DaysPastDueNotWorse": "number_times_latepay60-89"}, inplace=True)

    df.dropna(inplace=True)
    df= df[df['age'] >=18 ]
    df= df[df['NumberOfTime30-59DaysPastDueNotWorse']<96  ]
    df= df[df['balance_divided_creditlimit']<=1]

    
    garbage_columns= ["ID","SeriousDlqin2yrs", "NumberOfTime30-59DaysPastDueNotWorse"]
    X_train, X_test, y_train, y_test = train_test_split( df.drop(garbage_columns, axis=1), df["SeriousDlqin2yrs"], test_size=0.2)
    return X_train, X_test, y_train, y_test


def overSampling(X: pd.DataFrame | ArrayLike, y: pd.Series | ArrayLike):
    '''
    Args:
        X (Pandas DataFrame | ArrayLike): Pandas DataFrame to use a Over-sampling technique to avoid unbalanced dataset
        Y (Pandas Series | ArrayLike): Pandas Series to use a Over-sampling technique to avoid unbalanced dataset
    Returns:
        X (Pandas DataFrame | ArrayLike): Pandas DataFrame with over-sampling aplied
        Y (Pandas Series | ArrayLike): Pandas Series with over-sampling aplied

    '''
    ros = RandomOverSampler(random_state=0)
    X_resampled, y_resampled = ros.fit_resample(X, y)
    
    return X_resampled, y_resampled



def plot_roc(y_true: pd.Series | ArrayLike, y_score: pd.Series | ArrayLike):
    '''
    Args:
        y_true (Pandas Series | Numpy Array | ArrayLike): Actual Y from your dataset
        y_score (Pandas Series | Numpy Array | ArrayLike): Probabily estimator of your dataset
    Returns:
        A Roc/Auc graph from your dataset

    '''


    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = roc_auc_score(y_true, y_score)
    
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.show()



def plot_learningCurve(model, X_train: pd.DataFrame | ArrayLike, y_train: pd.Series | ArrayLike):
    '''
    Args:
        model (estimator): object type that implements the “fit” method
        X_train (Pandas DataFrame | ArrayLike): your training data without actual Y
        y_train (Pandas Series | ArrayLike): your training Y data
    Returns:
        A plot of a graph of your leaning curve through epochs
    
    '''

    train_sizes, train_scores, test_scores = learning_curve(
        model, X_train, y_train)
    display = LearningCurveDisplay(train_sizes=train_sizes,
        train_scores=train_scores, test_scores=test_scores, score_name="Score")
    display.plot()
    plt.show()


def plot_confussion(Y: pd.Series | ArrayLike, y_pred: pd.Series | ArrayLike):
    '''
    Args:
        Y (Pandas Series | ArrayLike): Actual Y from your dataset
        y_pred (Pandas Series | ArrayLike): Y predicted of your model
    Returns:
        A plot of a graph of the confussion matrix at *sns.heatmap* with percentage
    
    '''
    confi = confusion_matrix(Y, y_pred)
    plt.figure(figsize=(10, 10))

    confi = (confi/confi.sum())*100
    print(confi)
    formatted_confi = np.vectorize(lambda x: f"{x:.2f}%")(confi)
    sns.heatmap(confi, annot=formatted_confi, fmt="", linewidths=.5, cmap='cividis', xticklabels=[ 'FN','TN'], yticklabels=['TP', 'FN'])
    

    plt.show()

def plot_confussion_subplots(Y: pd.Series | ArrayLike, y_pred: pd.Series | ArrayLike, ax=0):
    '''
    Args:
        Y (Pandas Series | ArrayLike): Actual Y from your dataset
        y_pred (Pandas Series | ArrayLike): Y predicted of your model
        ax (int) : The number or a list to use while plotting more than 1 chart (like axs[1,0])
    Returns:
        Plots a chart of the confussion matrix at *sns.heatmap* with percentage
    
    '''
    confi = confusion_matrix(Y, y_pred)
    confi = (confi/confi.sum())*100
    formatted_confi = np.vectorize(lambda x: f"{x:.2f}%")(confi)
    sns.heatmap(confi, annot=formatted_confi, fmt="", linewidths=.5, cmap='cividis', xticklabels=[ 'FN','TN'], yticklabels=['TP', 'FN'], ax=ax)
    
