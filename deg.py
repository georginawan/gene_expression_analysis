#use non-smoker as reference, use smoker as test
from sklearn import preprocessing
import xlrd
import numpy as np 
from scipy import stats
from scipy.stats import rankdata
import matplotlib.pyplot as plt
#read excel file row by row,
#input file name,
#return a list of labels and an array of normalized data lists
def read_excel(file):
    labels = list()
    data = list()
    ids = list()
    wb = xlrd.open_workbook(filename=file)
    sheet1 = wb.sheet_by_index(0)
    row_num = 0
    while True:
        row_num += 1
        try:
            rows = sheet1.row_values(row_num)
            #if len(rows) > 0:   
           
            label = rows[1]
            if len(label) > 0:
                labels.append(label)   
                data.append(rows[3:]) 
                ids.append(rows[0])              
        except:
            break
    return labels,data,ids

#Function to calculate logFC
#input: list of data in one row
#return: log2(FC) value
def two_fold(rows):
    mean_ref = np.mean(rows[:20])
    mean_test = np.mean(rows[20:])
    fold_change = mean_test-mean_ref
    return fold_change

#Function to calculate p value using t test
#input: list of data in one row, total number of samples n
#return: p value
def ttest(rows):
    pvalue = stats.ttest_ind(rows[:20],rows[20:],equal_var=False)[1]
    return pvalue

def adj_pval(data):
    pvals = [ttest(row) for row in data]
    total = len(data)
    pval_rank = sorted(pvals)
    for i in range(len(pvals)):
        pvals[i] = -np.log10(pvals[i]*total/(pval_rank.index(pvals[i])+1))
    return pvals

#Function to draw output figure
def draw(logFC,ss,logFC_,ss_,h_t,label_FC,label_ss,label_label):
    plt.title("Volcano Plot")
    plt.subplot(121)
    deg_fc=[]
    deg_ss=[]
    nondeg_fc=[]
    nondeg_ss=[]
    for i in range(len(logFC)):
        if (logFC[i] < -2 or logFC[i] > 2) and ss[i] > h_t:
            deg_fc.append(logFC[i])
            deg_ss.append(ss[i])
        else:
            nondeg_fc.append(logFC[i])
            nondeg_ss.append(ss[i])
    plt.scatter(deg_fc,deg_ss,c='blue',label = 'DEGs')
    plt.scatter(nondeg_fc,nondeg_ss,s=2,c='grey',label='non-DEGs')
    plt.legend()
    plt.xlabel("biological significance [logFC]")
    plt.ylabel("statistical significance [-log(adj.P.value)]")
    plt.vlines(-2,0,8,linestyles="--")
    plt.vlines(2,0,8,linestyles="--")
    plt.hlines(h_t,-6,6,linestyles="--")
    '''
    plt.subplot(122)
    plt.scatter(logFC_,ss_,s=2)
    plt.xlabel("biological significance [logFC]")
    plt.ylabel("statistical significance [-log(adj.P.value)]")
    plt.vlines(-1,0,4,linestyles="--")
    plt.vlines(1,0,4,linestyles="--")
    plt.hlines(h_t,-1.5,3,linestyles="--")
    for i in range(len(label_FC)):
        plt.annotate(label_label[i],xy = (label_FC[i],label_ss[i]))
    '''
    plt.show()

#function to select some genes to draw a zoom-in figure as the second subplot
#t is the zoom-in threshold
def zoomin(logFC,ss,t,h_t,FC_t,labels,ids):
    #x value and y value of zoom-in figure
    logFC_ = list()
    ss_ = list()
    for i in range(len(logFC)):
        if ss[i] > t:     
            logFC_.append(logFC[i])
            ss_.append(ss[i])
    label_logFC = []
    label_ss = []
    label_label = []
    label_id = []
    for i in range(len(logFC)):
        if ss[i] > h_t:
            if logFC[i] > FC_t or logFC[i] < -FC_t:
                label_logFC.append(logFC[i])
                label_ss.append(ss[i])
                label_label.append(labels[i])
                label_id.append(ids[i])
    return logFC_,ss_,label_logFC,label_ss,label_label,label_id

def main():
    file = "C:\\Users\\surface\\Desktop\\Georgina\\BIFC\\final\\blank_del.xls"
    labelfile = open("C:\\Users\\surface\\Desktop\\Georgina\\BIFC\\final\\DEG_label_2.txt","w")
    labels,data,ids= read_excel(file)
    #data = preprocessing.normalize(data)
    #x value and y value of main figure
    logFC = [two_fold(row) for row in data]
    ss = adj_pval(data)
    h_t = -np.log10(0.05) #threshold set as 0.05
    logFC_,ss_,label_FC,label_ss,label_label,label_id = zoomin(logFC,ss,1,h_t,2,labels,ids)
    for label in label_label:
        labelfile.write(label+"\n")
    print(len(label_label))
    draw(logFC,ss,logFC_,ss_,h_t,label_FC,label_ss,label_id)
    labelfile.close()


main()
