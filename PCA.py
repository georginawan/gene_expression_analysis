import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from sklearn.preprocessing import normalize
import xlrd
import numpy as np 

def read_excel(file):
    data = list()
    wb = xlrd.open_workbook(filename=file)
    sheet1 = wb.sheet_by_index(0)
    row_num = 0
    while True:
        row_num += 1
        try:
            rows = sheet1.row_values(row_num)   
            data.append(rows[3:])         
        except:
            break
    return data

file = "C:\\Users\\surface\\Desktop\\Georgina\\BIFC\\final\\blank_del.xls"
data = read_excel(file)
y = []
for i in range(20):
    y.append(0)
for i in range(20):
    y.append(1)

x = np.transpose([i for i in data])
#x = normalize(x)
pca = PCA(n_components=2)
reduced_x=pca.fit_transform(x)
non_x,non_y=[],[]
deg_x,deg_y=[],[]

for i in range(len(reduced_x)):
    if y[i]==0:
        non_x.append(reduced_x[i][0])
        non_y.append(reduced_x[i][1])
    else:
        deg_x.append(reduced_x[i][0])
        deg_y.append(reduced_x[i][1])


plt.scatter(non_x,non_y,c='r',label='non-TNBC')
plt.scatter(deg_x,deg_y,c='b',label='TNBC')
plt.legend()
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title("PCA of all samples")
plt.show()

