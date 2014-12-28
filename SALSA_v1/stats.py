'''
Created on Nov 11, 2014

@author: michal
'''
import numpy as np

class stats_alg_atributes():
    num_of_mal = 'num_of_mal'
    min = 'min'
    max = 'max'
    avg = 'avg'
    median = 'median'
    std = 'std'
    g80 = '#>80'
    pct_g80 = '%>80'
    g85 = '#>85'
    pct_g85 = '%>85'
    g90 = '#>90'
    pct_g90 = '%>90'
    g95 = '#>95'
    pct_g95 = '%>95'
    auc = 'auc'
    num_of_test_domains = 'num_of_test_domains'
    
    
class stats():
        
    def __init__(self,algs_list,Lpct_dicts_list,label_list=[],scores_list=[]):
        # the order of Lpct_dicts should be as the algs_list order!!
        self.atr = stats_alg_atributes()
        self.test_labels = np.asarray(label_list)
        self.stats = {} 
        for idx,alg in enumerate(algs_list):
            alg_Lpct_dict = Lpct_dicts_list[idx]
            # Lpct_val_list - list of the alg Lpct values ordered by domain
            self.stats[alg] = {'Lpct_dict' : alg_Lpct_dict,\
                               'Lpct_val_list' : np.array(zip(*sorted(alg_Lpct_dict.items()))[1]),\
                               'test_scores_list': np.asarray(scores_list[idx])}    
        self.domains_list = zip(*sorted(alg_Lpct_dict.items()))[0] # last alg_Lpct_dict (of the last alg)- all algs should have the exact same domains
        return
    
    def calc_stats(self):
        import generalMethods as gm
        from sklearn.metrics import roc_auc_score
        for k,v in self.stats.items():
            Lpct_val_list = np.array(v['Lpct_val_list'])
            self.stats[k][self.atr.num_of_mal] = len(Lpct_val_list)
            self.stats[k][self.atr.min] = min(Lpct_val_list)
            self.stats[k][self.atr.max] = max(Lpct_val_list)
            self.stats[k][self.atr.avg] = np.average(Lpct_val_list)
            self.stats[k][self.atr.median] = np.median(Lpct_val_list)
            self.stats[k][self.atr.std] = np.std(Lpct_val_list)
            self.stats[k][self.atr.g80] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,80)
            self.stats[k][self.atr.pct_g80] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,80,pct_flag=True)
            self.stats[k][self.atr.g85] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,85)
            self.stats[k][self.atr.pct_g85] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,85,pct_flag=True)
            self.stats[k][self.atr.g90] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,90)
            self.stats[k][self.atr.pct_g90] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,90,pct_flag=True)
            self.stats[k][self.atr.g95] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,95)
            self.stats[k][self.atr.pct_g95] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,95,pct_flag=True)
            self.stats[k][self.atr.auc] = roc_auc_score(self.test_labels, v['test_scores_list'])
            self.stats[k][self.atr.num_of_test_domains] = len(v['test_scores_list'])
        return
    
    '''def auc_evaluation(self,algs_list,test=[]):#,fn=None):
        '''''' calculates the AUC measure for each algorithm
        Parameters
        ----------
        algs_list = list of algorithms , ['salsa','hits',...]
        test = 
        #fn = (string) full path name of output file
        
        
        Returns
        -------
        algs_auc = dict of algoritm-AUC , {'hits_auth':0.87,'pagerank_auth':0.59,...}''''''
        from sklearn.metrics import roc_auc_score
        algs_auc = {}
        if len(test):
            for alg in algs_list:
                alg_scores = [ self.G.node[k][self.alg_auth_Lpct[alg]] for k in test[0] ]
                algs_auc['_'.join([alg,'auth'])] = roc_auc_score(test[1], alg_scores)
                if alg in self.alg_hub_Lpct:    #hits or salsa
                    alg_scores = [ self.G.node[k][self.alg_hub_Lpct[alg]] for k in test[0] ]
                    algs_auc['_'.join([alg,'hub'])] = roc_auc_score(test[1], alg_scores)
            algs_auc['num_of_mal'] = sum(test[1])
            algs_auc['num_of_domains'] = len(test[1])
        return algs_auc'''
    
    def export_info(self,fn,raw_flag=False):
        ''' writes the stats object info to file
        Parameters
        ----------
        fn = (string) full path name of output file
        raw_flag = (bool) is True for writing the raw data as well (Lpct values) 
        
        Returns
        -------
        None'''
        import csv
        ordered_atr = [self.atr.min,self.atr.max,self.atr.avg,self.atr.median,self.atr.std,\
                        self.atr.g80,self.atr.g85,self.atr.g90,self.atr.g95,\
                        self.atr.pct_g80,self.atr.pct_g85,self.atr.pct_g90,self.atr.pct_g95,\
                        self.atr.num_of_mal,self.atr.num_of_test_domains,self.atr.auc] 
        f=open(fn, "wb")
        w = csv.writer(f)
        np.set_printoptions(precision=3)    # For printing numpy objects- prints 3 decimal after the point.
        w.writerow(['Algorithm'] + ordered_atr)
        for k,v in self.stats.items():
            w.writerow([k] + ["%.3f"%v[atr] for atr in ordered_atr])
        if raw_flag:    # writing the domains-Lpct dict
            w.writerow([' ']); w.writerow(['Lpct values'])
            w.writerow(['Domain']+sorted(self.stats))
            for d in self.domains_list:
                w.writerow([d]+["%.3f"%v['Lpct_dict'][d] for alg,v in sorted(self.stats.items())])
            
        f.close()
        return
    
       
def stats_union(stats_list,fn,raw_flag=False):
    ''' union several stats objects into one object (and write its info to a file at the end)
        Parameters
        ----------
        stats_list = a list of stats objects
        fn = (string) full path name of output file
        raw_flag = (bool) is True for writing the raw data as well (Lpct values) 
        
        Returns
        -------
        None'''
    if len(stats_list) == 1:    #In cases of NO K fold cross validation (evaluated domains list is empty)
        u_s = stats_list[0]
    else:   #K fold cross validation
        s = stats_list[0]
        u_obj = s.stats
        algs_list = u_obj.keys()
        u_dicts_list = [ u_obj[alg]['Lpct_dict'] for alg in algs_list ]
        u_test_label_list = stats_list[0].test_labels
        u_test_scores_list = [ u_obj[alg]['test_scores_list'] for alg in algs_list ]
        accum_aucs_list = [ u_obj[alg][s.atr.auc]*len(s.test_labels) for alg in algs_list ]
        
        for idx,alg in enumerate(algs_list):   # concatenate all Lpct dicts to the one of first object for each alg (saved as list of those dicts- u_dicts_list)
            for s in stats_list[1:]:    # stats_list[0] already in u_dicts_list
                u_dicts_list[idx].update(s.stats[alg]['Lpct_dict'])  
                u_test_scores_list[idx] = np.concatenate([u_test_scores_list[idx],s.stats[alg]['test_scores_list']])
                accum_aucs_list[idx] += s.stats[alg][s.atr.auc]*len(s.test_labels)
                if not idx: #enter for the first algorithm only- for each object in stats_list
                    u_test_label_list = np.concatenate([u_test_label_list,s.test_labels])
        u_s = stats(algs_list,u_dicts_list,u_test_label_list,u_test_scores_list)
        u_s.calc_stats()
        # calc averaged aucs and update u_s accordingly (the auc of the union stats is not correct, cause you cannot compare the Lpct scores of different domains from different runs of the same algorithm, basically it got worse auc values than actual average)
        num_of_domains = len(u_s.test_labels)
        for idx,alg in enumerate(algs_list):
            u_s.stats[alg][u_s.atr.auc] = accum_aucs_list[idx]/num_of_domains
    u_s.export_info(fn,raw_flag)
    return
    
            