#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 20, 2014

@author: michal
'''
import csv
from operator import itemgetter


 
def saveDict(fn,dict_rap):
    f=open(fn, "wb")
    w = csv.writer(f)
    for key, val in dict_rap.items():
        w.writerow([key, val])
    f.close()
     
def readDict(fn):
    import sys
    maxInt = sys.maxsize
    decrement = True
            
    f=open(fn,'rb')
    dict_rap={}
    while decrement:
        decrement = False          
        try:
            csv.field_size_limit(maxInt)
            for key, val in csv.reader(f):
                dict_rap[key]=eval(val)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True
        
    f.close()
    return(dict_rap)

def print_dict(d):
    for key in d.keys():
        print str(key) + ' : ' + str(d[key].round(4))
    return 

def print_dict_ordered_by_value(d):
    i=1
    for k, v in sorted(d.items(), key=itemgetter(1), reverse=True):
        #print str(i) + ':\t' + str(k) + '-\t' + str(v.round(4))
        print '(' + str(i) + ')\t' + str(k) + ':\t\t' + str(round(v,4))
        i+=1
    return

def write_dict_ordered_by_value_to_file(d,fn):
    i=1
    f=open(fn, "wb")
    w = csv.writer(f)
    for key, val in sorted(d.items(), key=itemgetter(1), reverse=True):
        w.writerow([i, key, val])
        i+=1
    f.close()
    return

def write_union_of_dicts_ordered_by_value_to_file_OLD(d1,d2,d3,fn):
    # d1 = dict where the output is order by its values!
    # d2 = dict where its value is added to the ordered d1 (as the input)
    # fn = file name (with full path) for the output
    i=1
    f=open(fn, "wb")
    w = csv.writer(f)
    for key, val in sorted(d1.items(), key=itemgetter(1), reverse=True):
        w.writerow([i, key, val, d2[key], '#', d3[key]])
        #w.writerow([i, key, round(val,4), round(d2[key],4), '#', round(d3[key],4)])
        i+=1
    f.close()
    return

def write_union_of_dicts_ordered_by_value_to_file(d,dicts_list,fn):
    # d = dict where the output is order by its values!
    # dicts_list = list of all dicts where its value is added to the ordered d (as the input)
    # IMPORTANT: dicts_list MUST include AT LEAST 2 dicts!!!
    # fn = file name (with full path) for the output
    i=1
    f=open(fn, "wb")
    w = csv.writer(f)
    for key, val in sorted(d.items(), key=itemgetter(1), reverse=True):
        w.writerow([key, val] + [dict_i[key] for dict_i in dicts_list[:-1]] + ['#', dicts_list[-1][key]])
        i+=1
    f.close()
    return
# general parameters:

def writeMatrixToFile(filePath, matrix):
    import os
    os.path.exists(filePath) and os.remove(filePath)
    target = open(filePath, 'a')
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            target.write(str(matrix[i][j])) ;
            target.write(str("\t")) ;
        target.write("\n")
    target.close();
                
    return 

def l1_norm_vector(V):
    # V is array
    return V/sum(V) 

def convert_all_matrix_zeros_to_val(M,val,stochastic_out=False):
    # M is a SPARSE matrix
    # val is the value you wish to fill instead all zeroes in M
    # is_sparse = is M sparse? (True/False)
    # stochastic_out = pass True if you wish the returned matrix be stochastic (each row sums to 1)
    # returns the new matrix M (with no zeros)
    from sklearn.preprocessing import normalize     # For normalizing matrix by row (sums to 1)

    '''if is_sparse:
        M = M.todense()
    P = np.asmatrix(M)'''
    M = M.todense()
    M += val
    '''for x in np.nditer(P,op_flags=['readwrite']):   #flags=['refs_ok'],
        x[...] = max(x,val)'''
    if stochastic_out:
        normalize(M, axis=1, norm='l1')   
    return M

def convert_upper_triangle_to_val(M,val):
    # M is a SPARSE matrix
    # val is the value you wish to fill instead all zeroes in M
    for i in range(M.shape[0]-1):
        for j in range(i+1,M.shape[0]-1-i):
            if not M[i,j]: M[i,j] = val
    return M

def convert_SL_and_CN_weights_to_val(M,val,CN_idx,stochastic_out=False):
    # M is a SPARSE matrix
    # val is the value you wish to fill instead all zeroes in M
    # is_sparse = is M sparse? (True/False)
    # stochastic_out = pass True if you wish the returned matrix be stochastic (each row sums to 1)
    # returns the new matrix M (with no zeros)
    import sys
    from datetime import datetime
    startTime = datetime.now()       
    import scipy.sparse as sps
                     

    print '\n\t~~~~~~ generalMethods: convert_SL_and_CN_weights_to_val (M, val='+str(val)+', CN_idx='+str(CN_idx)+', stochastic_out='+str(stochastic_out)+') ~~~~~~'; sys.stdout.flush()
    '''for i in xrange(M.shape[0]-1):
        #if not M[i,i]: M[i,i] = val
        if not M[CN_idx,i]: M[CN_idx,i] = val
        if not M[i, CN_idx]: M[i, CN_idx] = val
    '''
    from sklearn.preprocessing import normalize     # For normalizing matrix by row (sums to 1)

    M = sps.lil_matrix(M)   # just for updating the sparse matrix M (changing csr_matrix is expensive!)
    for i in xrange(M.shape[0]):  
        M[CN_idx, i] = max(val, M[CN_idx, i])
        M[i, CN_idx] = max(val, M[CN_idx, i])
    M = sps.csr_matrix(M)
    print '\n--- generalMethods: convert_SL_and_CN_weights_to_val: for loop took: ' + str(datetime.now()-startTime); sys.stdout.flush()
    #M = convert_upper_triangle_to_val(M,val)
    if stochastic_out:
        return normalize(M, axis=1, norm='l1', copy=False)   
    return M

def check_if_stochastic_matrix(np_mat):
    # np_mat is a numpy matrix, which its elements are FLOAT and  NOT INT!!!
    # returns: True/False
    is_stochastic = True
    for i in range(len(np_mat)):
        if str(np_mat[i].sum()) != '1.0':
            is_stochastic = False
            break
    return is_stochastic    
        
def write_graph_to_file(G,fn):
    import pickle
    pickle.dump(G, open(fn, 'w'))
    return

def read_graph_from_file(fn):
    import pickle
    return pickle.load(open(fn))

def write_object_to_file(obj,fn):
    import pickle
    pickle.dump(obj, open(fn, 'w'))
    return

def read_object_from_file(fn):
    import pickle
    return pickle.load(open(fn))

def get_percentiles(src_dict):
    from scipy.stats import stats as spst
    K,V = zip(*(list(sorted(src_dict.items(), key=itemgetter(1))))) #unzip the ordered src_dict
    u_pct = [spst.percentileofscore(V,v,kind='weak') for v in V]    # upper percentile list (under OR EQUAL)
    l_pct = [spst.percentileofscore(V,v,kind='strict') for v in V]  # lower percentile list (under)
    u_pct_dict = dict(zip(K,map(float,u_pct)))
    l_pct_dict = dict(zip(K,map(float,l_pct)))
    return u_pct_dict, l_pct_dict

def histogram_of_dict(d,fn,bins=200):
    from matplotlib import pyplot as plt
    d = clean_scores_dict(d,fn)
    print max(d.values())
    #plt.bar(range(0,10),d)#.values())
    #, range, normed, weights, cumulative, bottom, histtype, align, orientation, rwidth, log, color, label, stacked, hold)
    #print d;
    plt.hist(d.values(), bins=bins, normed=True, log=True)#stacked=True, cumulative=False)
    plt.show()
    
    return

def clean_scores_dict(d,fn):
    with open(fn,'r') as f:
        remove_keys = f.readlines()
    remove_keys = [k.rstrip() for k in remove_keys]
    for k in remove_keys:
        del d[k]
    return d
    
def create_max_dict_from_dicts(dicts_list,fn=None):
    # dicts_list = list of dictionaries WHICH HAVE THE SAME KEIS!!!!!
    # fn = output file path
    d = {}
    for key in dicts_list[0]:
        d[key] = max([dict_i[key] for dict_i in dicts_list])
    if fn:
        write_dict_ordered_by_value_to_file(d,fn)
    return d

def create_avg_dict_from_dicts(dicts_list,n=None,fn=None):
    # dicts_list = list of dictionaries WHICH HAVE THE SAME KEIS!!!!!
    # n = the average is made from the top n values
    # fn = output file path
    import numpy as np
    
    d = {}
    if not n:
        n = len(dicts_list)
    for key in dicts_list[0]:
        d[key] = np.mean(sorted([dict_i[key] for dict_i in dicts_list],reverse=True)[0:n])  # [0:n] is NOT including n!!!
    if fn:
        write_dict_ordered_by_value_to_file(d,fn)
    return d

def write_dict_of_dicts_to_file(d,fn,first_col_name='domain'):
    # d is a dict of dicts
    # fn is the full path of the output file
    import csv
    #fn = '/home/michal/SALSA_files/tmp/test2.csv'
    d = {'one':{'a':1,'b':6,'c':3,'d':5},'two':{'a':2,'b':7,'c':4,'d':6},'three':{'a':3,'b':8,'c':5,'d':7}}
    n = 'doamin'
    sorted_dom_list = sorted(d)
    
    with open(fn, "a") as f:
        w = csv.writer(f)
        w.writerow(['---------------------------------'])
        w.writerow([n]+[attr for attr in sorted(d[sorted_dom_list[0]])])
        for k in sorted_dom_list:
            #print zip(*sorted(d.items()))[1]
            #w.writerow([k]+[attr for attr in sorted(d[k])])
            w.writerow([k]+list(zip(*sorted(d[k].items()))[1]))
    return

epsilon = 1e-4 #0.0001