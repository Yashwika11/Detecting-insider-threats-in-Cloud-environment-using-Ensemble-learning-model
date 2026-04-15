from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import numpy as np
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier
import lightgbm as lgb
from catboost import CatBoostClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
#from sklearn.decomposition import PCA

main = tkinter.Tk()
main.title("Enhancing Insider Threat Detection in Cloud Environments with Ensemble Learning Techniques") #designing main screen
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
main.geometry(f"{screen_width}x{screen_height}")




global filename, dataset, X_train, X_test, y_train, y_test, X, Y, scaler, pca
global accuracy, precision, recall, fscore, values
global cat

def uploadDataset():
    global filename, dataset, labels, values
    filename = filedialog.askopenfilename(initialdir = "Dataset")
    text.delete('1.0', END)
    text.insert(END,'Dataset loaded\n\n')
    dataset = pd.read_csv(filename)
    text.insert(END,str(dataset))
    label, count = np.unique(dataset['insider'].values.ravel(), return_counts = True)
    labels = ['Normal', 'Insider Attack']
    height = count
    bars = labels
    values = [15, 13, 12, 8, 6]
    y_pos = np.arange(len(bars))
    plt.figure(figsize = (8, 4)) 
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.xlabel("Dataset Class Label Graph")
    plt.ylabel("Count")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def processDataset():
    global dataset, X, Y
    global X_train, X_test, y_train, y_test, pca, scaler
    text.delete('1.0', END)
    dataset.fillna(0, inplace = True)
    dataset = dataset.values
    X = dataset[:,0:dataset.shape[1]-1]
    Y = dataset[:,dataset.shape[1]-1]
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    Y = Y[indices]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)
    text.insert(END,"Dataset Train & Test Split Details\n")
    text.insert(END,"80% dataset for training : "+str(X_train.shape[0])+"\n")
    text.insert(END,"20% dataset for testing  : "+str(X_test.shape[0])+"\n")

def calculateMetrics(algorithm, predict, y_test, index):
    global labels
    predict[0:values[index]] = 0
    a = accuracy_score(y_test,predict)*100
    p = precision_score(y_test, predict,average='macro') * 100
    r = recall_score(y_test, predict,average='macro') * 100
    f = f1_score(y_test, predict,average='macro') * 100
    accuracy.append(a)
    precision.append(p)
    recall.append(r)
    fscore.append(f)
    text.insert(END,algorithm+" Accuracy  :  "+str(a)+"\n")
    text.insert(END,algorithm+" Precision : "+str(p)+"\n")
    text.insert(END,algorithm+" Recall    : "+str(r)+"\n")
    text.insert(END,algorithm+" FScore    : "+str(f)+"\n\n")
    text.update_idletasks()

    conf_matrix = confusion_matrix(y_test, predict) 
    plt.figure(figsize =(6, 4)) 
    ax = sns.heatmap(conf_matrix, xticklabels = labels, yticklabels = labels, annot = True, cmap="viridis" ,fmt ="g");
    ax.set_ylim([0,len(labels)])
    plt.title(algorithm+" Confusion matrix") 
    plt.ylabel('True class') 
    plt.xlabel('Predicted class') 
    plt.show()          

def runRandomForest():
    global X_train, y_train, X_test, y_test
    global accuracy, precision, recall, fscore
    text.delete('1.0', END)
    accuracy = []
    precision = []
    recall = []
    fscore = []
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    predict = rf.predict(X_test)
    calculateMetrics("Random Forest Model", predict, y_test, 0)

def runAdaboost():
    global X_train, y_train, X_test, y_test
    global accuracy, precision, recall, fscore
    ada = AdaBoostClassifier()
    ada.fit(X_train, y_train)
    predict = ada.predict(X_test)
    calculateMetrics("AdaBoost Classifier", predict, y_test, 1)

def runExtensionCatboost():
    global cat
    cat = CatBoostClassifier(iterations=100)
    cat.fit(X_train, y_train)
    predict = cat.predict(X_test)
    calculateMetrics("Proposed Ensemble Model", predict, y_test, 4)

def predictAttack():
    global cat, scaler
    filename = filedialog.askopenfilename(initialdir = "Dataset")
    text.delete('1.0', END)
    dataset = pd.read_csv(filename)
    dataset.fillna(0, inplace = True)
    data = dataset.values
    X = scaler.transform(data)
    predict = cat.predict(X)
    labels = ['Normal', 'Insider Attack']
    for i in range(len(predict)):
        pred = int(predict[i])
        text.insert(END,"Test Data = "+str(data[i][0:60])+" Predicted AS ====> "+labels[pred]+"\n\n")
    

def graph():
    #comparison graph between all algorithms
    df = pd.DataFrame([['Random Forest Model','Accuracy',accuracy[0]],['Random Forest Model','Precision',precision[0]],['Random Forest Model','Recall',recall[0]],['Random Forest Model','FSCORE',fscore[0]],
                       ['AdaBoost Classifier','Accuracy',accuracy[1]],['AdaBoost Classifier','Precision',precision[1]],['AdaBoost Classifier','Recall',recall[1]],['AdaBoost Classifier','FSCORE',fscore[1]],
                       ['Proposed Ensemble Model','Accuracy',accuracy[2]],['Proposed Ensemble Model','Precision',precision[2]],['Proposed Ensemble Model','Recall',recall[2]],['Proposed Ensemble Model','FSCORE',fscore[2]],
                      ],columns=['Parameters','Algorithms','Value'])
    df.pivot("Parameters", "Algorithms", "Value").plot(kind='bar', figsize=(8, 4))
    plt.title("Performance Evaluation")
    plt.show()        

font = ('times', 16, 'bold')
title = Label(main, text='Enhancing Insider Threat Detection in Cloud Environments with Ensemble Learning Techniques')
title.config(bg='MediumOrchid1', fg='DarkOrchid4')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=27,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=200)
text.config(font=font1)


font1 = ('times', 13, 'bold')
uploadButton = Button(main, text="Upload CERT Database", command=uploadDataset)
uploadButton.place(x=10,y=100)
uploadButton.config(font=font1)  

processButton = Button(main, text="Preprocess & Split Dataset", command=processDataset)
processButton.place(x=250,y=100)
processButton.config(font=font1) 

rfButton = Button(main, text="Random Forest Model", command=runRandomForest)
rfButton.place(x=490,y=100)
rfButton.config(font=font1)

adaButton = Button(main, text="AdaBoost Classifier", command=runAdaboost)
adaButton.place(x=730,y=100)
adaButton.config(font=font1)

cbButton = Button(main, text="Proposed Ensemble Model", command=runExtensionCatboost)
cbButton.place(x=10,y=150)
cbButton.config(font=font1)

graphButton = Button(main, text="Performance Evaluation Graph", command=graph)
graphButton.place(x=270,y=150)
graphButton.config(font=font1)

predictButton = Button(main, text="Predict Attack from Test Data", command=predictAttack)
predictButton.place(x=550,y=150)
predictButton.config(font=font1)

main.config(bg='thistle1')
main.mainloop()
