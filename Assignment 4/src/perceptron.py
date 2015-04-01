# Perceptron implementation
import util
PRINT = True

class PerceptronClassifier:
    """
    Perceptron classifier.
    
    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        for label in legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use
            
    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details. 
        
        Use the provided self.weights[label] datastructure so that 
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).
        """
        
        self.features = trainingData[0].keys() # could be useful later
        
        for iteration in range(self.max_iterations):    #self.max_iterations is given as Command Line argument, default is 3
            print "Starting iteration ", iteration, "..."
            allGuessesCorrect = True    #check if 100% accuracy on training data is reached
            for i in range(len(trainingData)):  #loop over each entry in training data
                    expected = trainingLabels[i]    #the correct classification of this entry
                    guess = self.classify([trainingData[i]])    #attempt to classify this entry
                    if guess[0] != expected:    #if the classification was wrong, adjust weight vectors, otherwise no action is taken
                        self.weights[expected] += trainingData[i]   #w(y) = w(y) + f
                        self.weights[guess[0]] -= trainingData[i]   #w(y) = w(y) - f
                        allGuessesCorrect = False
            
            if allGuessesCorrect == True:   #100% of accuracy on training data, nothing more to learn. 
                print "Reached 100% accuracy on Training data"
                break
        
    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.    See the project description for details.
        
        Recall that a datum is a util.counter... 
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns a list of the 100 features with the greatest difference in weights:
                                         w_label1 - w_label2

        """
        feature1 = self.weights[label1] #w(y1) : y1 = label1
        feature2 = self.weights[label2] #w(y2) : y2 = label2
        
        values = util.Counter();
        
        for f in self.features:
            values[f] = feature1[f] - feature2[f]   #values[f] = w(y1)(f) - w(y2)(f) 

        featuresOdds = values.sortedKeys()  #order entries according to maximum values (maximum difference in weights)
        featuresOdds = featuresOdds[0:100]  #get the first 100 entries
        
        return featuresOdds