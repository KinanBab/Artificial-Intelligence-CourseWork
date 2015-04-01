import util
import math
import classificationMethod

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.
    
    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically
        
    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """    
            
        self.features = trainingData[0].keys() # this could be useful for your code later...
        
        if (self.automaticTuning):
                kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
                
        else:
                kgrid = [self.k]
                
        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
            
    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter 
        that gives the best accuracy on the held-out validationData.
        
        trainingData and validationData are lists of feature Counters. The corresponding
        label lists contain the correct label for each datum.
        
        To get the list of all possible features or labels, use self.features and 
        self.legalLabels.
        """        
        fCounts = util.Counter() 
        for y in self.legalLabels:
            fCounts[y] = util.Counter() #fCounts is a Counter of Counter, each sub Counter corresponds to a value of y (Label)
        
        self.priors = util.Counter() #Counter that will contain the values of P(y) for all possible Labels
                
        i = 0
        while i < len(trainingLabels):  #loop over training data
            self.priors[trainingLabels[i]] += 1 #c(y)++
            tmp = fCounts[trainingLabels[i]]
            for f in self.features:
                if trainingData[i][f] == 1:
                    tmp[f] += 1     #c(f(i)=1, y)++)
                
                else:
                    tmp[f] = tmp[f]
            i += 1
           
        kFeatures = util.Counter()  #holds a different table for each value of k
        for k in kgrid: #for all possible k in kgrid
            tmp = util.Counter()    
            for y in self.legalLabels:
                tmp[y] = fCounts[y].copy()  #copy by value
                
            for y in self.legalLabels:
                tmp[y].incrementAll(tmp[y].keys(), k)   #c(f(i) = 1, y) = c(f(i) = 1, y) + k  
                tmp[y].divideAll(self.priors[y] + 2*k)  #P(f(i) = 1, y) = c(f(i) = 1. y) + k / c(f(i) = j, y) + 2*k : j belongs {0, 1}
                
            kFeatures[k] = tmp
            
        self.priors.normalize() #P(y) = c(y) / n
        
        
        #Tuning k based on validation data set
        if len(kgrid) > 0:
            print "Tuning Phase..."
            print "Choosing the best k from", kgrid
            print "This may take a while..."
            maxAcc = -1
            maxK = -1
            for k in kgrid:
                self.fTable = kFeatures[k]
                guesses = self.classify(validationData)
                correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True) #number of correct guess with the table of k
                
                if maxAcc < correct:
                    maxAcc = correct
                    maxK = k
                    
            self.fTable = kFeatures[maxK]   #choosing k where the correct guess were maximized 
        
        else:
            self.fTable = kFeatures[kgrid[0]]   #only one possible value of k, no tuning

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses
            
    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.        
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
        """
        logJoint = util.Counter()
            
        for y in self.legalLabels:
            logJoint[y] = math.log(self.priors[y])
            for f in self.features:
                if datum[f] == 1:
                    logJoint[y] += math.log(self.fTable[y][f])
                else:
                    logJoint[y] += math.log(1.0 - self.fTable[y][f])
                    
        return logJoint
    
    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                        P(feature=1 | label1)/P(feature=1 | label2) 
        """                
        feature1 = self.fTable[label1]  #P(F = 1| label1) : for all F in features
        feature2 = self.fTable[label2]  #P(F = 1| label2) : for all F in features
        
        values = util.Counter();

        for f in self.features:
            values[f] = feature1[f] / feature2[f] #values[f] = P(F(f) = 1| label1) / P(F(f) = 1| label2)

        featuresOdds = values.sortedKeys()  #order entries according to maximum values (largest odds ratio)
        featuresOdds = featuresOdds[0:100] #get the first 100 entries

        return featuresOdds