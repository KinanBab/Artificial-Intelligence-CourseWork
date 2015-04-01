import sys

#Method that returns true if the string s is not a number
#Might be useful in reading the file.
def isalpha(s):
    try:
        float(s)
        return False
    except ValueError:
        return True

#Method that take an integer n and a number of bits d
#it returns the d bits representation of n as string
def toBin(n,d):
    s2=''
    
    while(d>0):
        x= str(n%2)
        s2=x+s2
        n=n/2
        d-=1
    return s2

"""
fullJoint calculates the full joint probability 
of any possible combination of ALL Nodes
s is the list of variables to calculate joint
e.g: s=['+a','+e','-b','+j','+mary']
cpt is the dictionary of CPTs
""" 
def fullJoint(s,cpt):    
    product = float(1)
    
    vals = {}
    i = 0
    while i < len(s):   #change + to 0 and - to 1 to match the stored data format
        if s[i][0] == '+':
            vals[s[i][1:]] = 0
        else:
            vals[s[i][1:]] = 1
            
        s[i] = s[i][1:]
        i = i + 1
    
    for query in s:     #for each variable in the network
        table = cpt[query]  #get the table of this variable
        head = table['headers'] #get the parents of the node
        for line in table['lines']:
            if int(line[query]) == int(vals[query]):
                if len(head) == 0:  #if no parents
                    product = product * line['val']
            
                else:   #if there is parents, only get the rows in which the parents has the given boolean value
                    flag = 1
                    for h in head:
                        if int(line[h]) != int(vals[h]):
                            flag = 0
                            break
                
                    if flag == 1:
                        product = product * line['val']
    
    return product

"""
s is a list of nodes: ['b','e']
return a list of all possible combination of strings [['+b','+e'],['+b','-e'],['-b','+e'],['-b','-e']] 
Note the correct order of the parents
Note also that this is an optional method you might find it useful and use it.
You will not lose grades if you do not implement it 
"""
def genComb(s):
    if len(s) == 1: #base case, One element only
        return [['+'+s[0]],['-'+s[0]]]  #return a list [+element, - element]
    
    current = s[0]  
    s.remove(current)
    rest = genComb(s)   #recursive call, get the combination for all elements - first element
    
    first = []
    second = []
    
    i = 0
    while i < len(rest):    #take the combination of the rest of the list and duplicate it
        first.append(['+'+current] + rest[i])   #add +current to the start of the first duplication 
        second.append(['-'+current] + rest[i])   #add -current to the start of the second duplication
        i = i + 1
    
    res = first + second    #combine the two duplicates
    
    return res	 

"""
Enum function calculates the probability of any list of variables in s using variable enumeration
s is the list of variables that you wish to find the joint (Only joint no conditionals in this method)
cpt is the dictionary holding the Conditional Tables
node is a list of all nodes in the BN
"""
def Enum(s,cpt,node):
    w = float(0)
        
    for query in s:     #get the hidden variables
        node.remove(query[1:])
    
    if len(node) == 0:  #if no hidden variable it means all variables has specific values. calculate probability directly
        return fullJoint(s, cpt)
    
    node = genComb(node)    #get all possible combination for hidden variables
    for comb in node:   #E(e) E(a) P(B, e, a, j,m) (E is SIGMA symbol [summation])
        w = w + fullJoint(s + comb, cpt)
    
    return w
    
"""
A method that takes the filename where the BN is saved as parameter 	
This method should fill up a nodes instance variable that contains all the nodes
It should also fill up a dictionary (instance variable) that holds the CPTs. 
"""
def readFile(s):
    cpt = {}
    node = []
    
    f = open(s,'r')
    for lines in f:
        lines = lines.strip()
        if isalpha(lines) and "," not in lines:    #current node has no parents
            name = lines    #get the symbol for current node
            node.append(name)   #append symbol to node list
            
            table = []
            for l in f: #fill the table for this node
                l = l.strip()
                table.append({name: "0", 'val': round(float(l), 3)})
                table.append({name: "1", 'val': round(1 - round(float(l), 3), 3) })
                break;
            
            cpt[name] = {'headers': [], 'lines': table} #store table in cpt dictionary
            
        elif isalpha(lines):   #current node has one or more parents
            lines = lines.split(",")
            
            name = lines[-1]    #get the symbol for current node
            lines.remove(name)  #get the parent list
            node.append(name)   #append symbol to node list
            
            table = []
            index = 0
            for l in f: #fill the table for this node
                l = l.strip()
                binary = toBin(index, len(lines))  #getting the binary representation of index as a string

                tmp1 = {name: "0"}
                tmp2 = {name: "1"}
                
                j = 0
                while j < len(binary):
                    tmp1[lines[j]]= binary[j]
                    tmp2[lines[j]]= binary[j]    
                    j = j + 1                
                
                tmp1['val'] = round(float(l), 3)
                tmp2['val'] = round(1 - round(float(l), 3), 3)
                
                table.append(tmp1)
                table.append(tmp2)
                
                index = index + 1
                if 2**len(lines) == index:   #reading 2^n lines
                    break
            
            cpt[name] = {'headers': lines, 'lines': table}  #store table in cpt dictionary
            
    return (node, cpt)

"""
your code should read the command line arguments and calculate the corresponding probability.
the output should be formatted as follows: P(+b/+j,+mary)=0.284
"""
arg=sys.argv[1:]    #contains the command line arguments
if __name__ == '__main__':
    """main function:"""
    
    node, cpt = readFile("BN.txt")  #read data from BN.txt and store the resulting CPTs and node list
    
    QUERY = []
    EVIDENCE = []
    
    try:    #if the query contained given key word split query into QUERY and EVIDENCE
        if isinstance(arg[0:arg.index('given')], list):
            QUERY = arg[0:arg.index('given')]
        else:
            QUERY.append(arg[0:arg.index('given')])
            
        if isinstance(arg[arg.index('given')+1], list):
            EVIDENCE = arg[arg.index('given')+1]
        else:
            EVIDENCE.append(arg[arg.index('given')+1])
                
    except ValueError:  #no EVIDENCE provided
        if isinstance(arg, list):
            QUERY = arg
        else:
            QUERY.append(arg)
    
    st = "P("
    i = 0
    while i < len(QUERY):
        st = st + QUERY[i]
        
        if not i == len(QUERY)-1:
            st = st + ","
    
        i = i + 1
        
    i = 0
    while i < len(EVIDENCE):
        if i == 0:
            st = st + "|"
        st = st + EVIDENCE[i]
        
        if not i == len(EVIDENCE)-1:
            st = st + ","
            
        i = i + 1
        
    st = st + ")="

    res = Enum(QUERY[0:]+EVIDENCE[0:], cpt, node[0:]) / Enum(EVIDENCE, cpt, node[0:])   #P(QUERY + EVIDENCE) / P(EVIDENCE) [Joint Probability]
     
    print st, res
    print "DISCLAMER: floating points is not 100% accurate, fractions can't all be represented in binary base\n I am using round to get a close result"
    print "Please check the remarks about floating points in the python docs. on the web."  
    
    """TEST CASES:"""  
    """    
        TEST CASE 1:
            Bayes net:
                
                a     b
                 \   /     
                  \/
                  c

    ---------TEST CASE 1 start:
      
    node = ['a', 'b', 'c']
    s = ['-a']
    
    a = {'headers': [], 'lines': [{'a': 0, 'val': 0.66}, {'a': 1, 'val': 0.34}] }
    b = {'headers': [], 'lines': [{'b': 0, 'val': 0.5}, {'b': 1, 'val': 0.5}] }
    
    line1 = {'val': 0.1, 'a': 0, 'b': 0, 'c': 0}
    line2 = {'val': 0.1, 'a': 0, 'b': 1, 'c': 0}
    line3 = {'val': 0.1, 'a': 1, 'b': 0, 'c': 0}
    line4 = {'val': 0.1, 'a': 1, 'b': 1, 'c': 0}
    line5 = {'val': 0.1, 'a': 0, 'b': 0, 'c': 1}
    line6 = {'val': 0.1, 'a': 0, 'b': 1, 'c': 1}
    line7 = {'val': 0.1, 'a': 1, 'b': 0, 'c': 1}
    line8 = {'val': 0.3, 'a': 1, 'b': 1, 'c': 1}
    
    tt = [line1, line2, line3, line4, line5, line6, line7, line8]
    
    c = {'headers': ['a', 'b'], 'lines': tt }
    
    cpt = {'a': a, 'b': b, 'c': c}
    g = ['+c']
    
    print Enum(s+g, cpt, node[0:]) / Enum(g, cpt, node[0:])
    
    ---------TEST CASE 1 end.
    """ 
    """    
        TEST CASE 2: (SOURCE Wikipedia with an additional table ir that is independent to everything)
                    (LINK: http://en.wikipedia.org/wiki/Bayesian_network#Example)
                    
            Bayes net:
                
                sprinkler      rain            ir(an irrelevant table)
                     \         /     
                      \       /
                      Grass wet

    ---------TEST CASE 2 start:
    
    node = ['rain', 'sprinkler', 'grass wet', 'ir']
    s = ['+ir']
    g = ['-rain']
    
    rain = {'headers': [], 'lines': [{'rain': 0, 'val': 0.2}, {'rain': 1, 'val': 0.8}] }
    sprinkler = {'headers': ['rain'], 'lines': [
        {'sprinkler': 0, 'rain': 0, 'val': 0.01},
        {'sprinkler': 0, 'rain': 1, 'val': 0.4},
        {'sprinkler': 1, 'rain': 0, 'val': 0.99},
        {'sprinkler': 1, 'rain': 1, 'val': 0.6}
    ] }
    
    ir = {'headers': [], 'lines': [{'ir': 0, 'val': 0.951}, {'ir': 1, 'val': 0.049}]}
    
    line1 = {'val': 0.99, 'rain': 0, 'sprinkler': 0, 'grass wet': 0}
    line2 = {'val': 0.8, 'rain': 0, 'sprinkler': 1, 'grass wet': 0}
    line3 = {'val': 0.9, 'rain': 1, 'sprinkler': 0, 'grass wet': 0}
    line4 = {'val': 0.0, 'rain': 1, 'sprinkler': 1, 'grass wet': 0}
    line5 = {'val': 0.01, 'rain': 0, 'sprinkler': 0, 'grass wet': 1}
    line6 = {'val': 0.2, 'rain': 0, 'sprinkler': 1, 'grass wet': 1}
    line7 = {'val': 0.1, 'rain': 1, 'sprinkler': 0, 'grass wet': 1}
    line8 = {'val': 1.0, 'rain': 1, 'sprinkler': 1, 'grass wet': 1}
    
    tt = [line1, line2, line3, line4, line5, line6, line7, line8]
    
    grasswet = {'headers': ['rain', 'sprinkler'], 'lines': tt }
    
    cpt = {'rain': rain, 'sprinkler': sprinkler, 'grass wet': grasswet, 'ir': ir}
    
    ---------TEST CASE 1 end.
    """