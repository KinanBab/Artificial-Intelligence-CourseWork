import sys
import random



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

	
#fullJoint calculates the full joint probability 
#of any possible combination of ALL Nodes
#s is the list of variables to calculate joint
#e.g: s=['+a','+e','-b','+j','+mary']
#cpt is the dictionary of CPTs 
def fullJoint(s,cpt):
	
	#your code goes here
	
	
	
	return -1
	
	 

# s is a list of nodes: ['b','e']
# return a list of all possible combination of strings [['+b','+e'],['+b','-e'],['-b','+e'],['-b','-e']] 
# Note the correct order of the parents
# Note also that this is an optional method you might find it useful and use it.
# You will not lose grades if you do not implement it 
def genComb(s):
	b=len(s)-1
	res=[]
	#your code goes here
	return res	 
	
	
#Enum function calculates the probability of any list of variables in s using variable enumeration
#s is the list of variables that you wish to find the joint (Only joint no conditionals in this method)
#cpt is the dictionary holding the Conditional Tables
#node is a list of all nodes in the BN
def Enum(s,cpt,node):
	w=0
	
	#your code goes here
	
	return w
	
	
#A method that takes the filename where the BN is saved as parameter 	
# This method should fill up a nodes instance variable that contains all the nodes
# It should also fill up a dictionary (instance variable) that holds the CPTs. 
def readFile(s):
	f=open(s,'r')
	for lines in f:
		#code goes here
	return 0
	


#Here is the main method	
#arg contains all command line arguments
arg=sys.argv[1:]


#code goes here

#your code should read the command line arguments and calculate the corresponding probability.
#the output should be formatted as follows: P(+b/+j,+mary)=0.284