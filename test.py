import numpy as np
from matplotlib import mlab
import csv

columns = ['a', 'b', 'c']
data = [[1, 2, 3], [4, 5, 6]]
fname = 'my_data.csv'

np.savetxt(fname, data, delimiter=',')


f = open('my_data_1.csv', 'wb')
w = csv.writer(f)
w.writerow(columns)
for row in data:
    w.writerow(row)
f.close()

rdata = np.loadtxt(fname, delimiter=',')
print rdata

