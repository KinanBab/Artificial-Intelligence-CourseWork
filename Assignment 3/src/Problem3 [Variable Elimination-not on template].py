""""
    @author: Kinan Dak Al Bab
    @date:   26/10/2013
    
    This file contains the solution to problem 3
    It reads the CPTs from "BN.txt" and computes the desired probability combination (passed by command line)
    
"""

class Factor:
    """
    AF:
        -count :  the number of variables in this factor
        -legend : list containing strings, legend[i] contains the variable name for which the column i represents, i.e.
            each factor represents P(X|Y) : X, Y both are subsets of legend
        -table :  list of lists (2 dimension list):
            columns [0: count-1]  contain either 0 or 1, s.t. for 0 it means -legend[i] and for 1 it means +legend[i]
            column [count]        contain the probability of the combination of variables in this row indicated by values in columns[0: count-1] 
    """ 
    def __init__(self, legend, table):
        """
        REQUIRES:    legend and table are not null.
        EFFECTS:     Creates a new factor with the following table and legend.
        
        """
        self.legend = legend
        self.table = table
        self.count = len(legend)
                
    def containsVar(self, var):
        """
        REQUIRES:   ... 
        EFFECTS:    Returns true if self.table has entries about this var,
                    false otherwise.
        """
        return var in self.legend
    
    def product(self, factor, var):
        """
        REQUIRES:    factors is not null, var is mutual between self and factor.
        EFFECTS:     returns a new factor that is the sum over var of the product of factors.
        
        """
        prod = Factor([], [])
        
        legends = self.legend    #combining all variables in the factors
        legends = legends + factor.legend
        legends = list(set(legends))    #removing duplicates 
        prod.legend = legends
        
        for i in range(0,2):
            first = self.get(var, i)
            second = factor.get(var, i)            
            for fline in first:
                fline = fline[1:]
                for sline in second:
                    tline = fline[:-1] + sline
                    tline[-1] = sline[-1] * fline[-1]
                    prod.table.append(tline)

        return prod
        
    def sum(self, var):
        """
        REQUIRES:    ...
        EFFECTS:     sum entries over var then remove var from representation
        MODIFIES:    this
        """ 
        column = self.legend.index(var)
        i = 0
        while i < len(self.table):
            j = i + 1
            while j < len(self.table):
                iline = self.table[i]
                jline = self.table[j]
                flag = 1
                for k in (0,len(iline)-2):
                    if k != column and iline[k] != jline[k]:
                        flag = 0
                        break
                    
                if flag == 1:
                    self.table[i][-1] = iline[-1] + jline[-1]
                    self.table.pop(j)
                    j= j - 1
                    
                j = j + 1
                
            self.table[i].pop(column)
            i = i + 1
            
        self.legend.pop(column)
    
    def get(self, var, value):
        """
        REQUIRES:    ...
        EFFECTS:     returns a sub table of self.table where the value representing if var was true or false is equal to value.
                     the ordering of column is changed, all columns are shifted to the right however the column representing var
                     becomes the first column.
        """
        result = []
        column = self.legend.index(var)
        for line in self.table:
            if line[column] == value:
                result.append([])
                result[-1].append(line[column])
                for i in range(0, self.count):
                    if not i == column:
                        result[-1].append(line[i])
                        
                result[-1].append(line[self.count])
                
        return result
        
class BayesNet:
    """
    Represents a Bayes network, it contains a list of Factors, each factor represents one of the conditional probability tables that 
        are usually provided with the Bayes network (similar to the tables provided in problem1 word file).
    """
    def __init__(self):
        """
        REQUIRES:   ...
        EFFECTS:    creates a new BayesNet, filled with the data from BN.txt 
                    
        """
        #self.factors = []
        self.vars = ["b", "c", "e"]
        l1 = [0, 0, 0.5]
        l2 = [1, 0, 0.4]
        l11 = [0, 1, 0.05]
        l22 = [1, 1, 0.05]
        f = Factor(["b", "e"], [l1, l2, l11, l22]) 
        self.factors = [f]
        
        
        l3 = [0, 0, 0.02]
        l4 = [0, 1, 0.05]
        l5 = [1, 0, 0.03]
        l6 = [1, 1, 0.9]
        ff = Factor(["b", "c"], [l3,l4,l5,l6])
        self.factors.append(ff)
       
        l7 = [0, 0.9]
        l8 = [1, 0.1]
        f2 = Factor(["e"], [l7, l8]) 
        self.factors = [f2]
    
    def proccess(self, query, evidence):
        """
        REQUIRES:    ...
        EFFECTS:     calculates the requested probability
        MODIFIES:    this
        """
        pool = set(self.vars) - set(query)
        pool = pool - set(evidence)
        for var in pool:
            self.eliminate(var)
            
        prod = self.factors[0]
        if len(self.factors) > 1:
            for i in (1, len(self.factors)):
                prod = prod.product(self.factors[i], query[0])
                
        sum = 0
        for line in prod.table:
            sum += line[-1]
        
        for line in prod.table:
            line[-1] = line[-1] / sum
            print line        
        
    
    def eliminate(self, var):
        """
        REQUIRES:    ...
        EFFECTS:     eliminates var from the factors of this basyen network.
        MODIFIES:    this
        """
        pool = []
        prod = 0
        print var
        for factor in self.factors:
            if factor.containsVar(var):
                if len(pool) == 0:
                    prod = factor
                    pool.append(factor)
                else:
                    prod = factor.product(prod, var)
                    pool.append(factor)
                
        prod.sum(var)
        
        for factor in pool:
            self.factors.remove(factor)
        
        self.factors.append(prod)
        
if __name__ == '__main__':
    """main function:"""
    b = BayesNet()
    b.proccess("b", [])