import numpy as np

class Perceptron:
    def __init__(self, n_iteration=100):
        self.n_iteration = n_iteration
        self.activation_function = self.activation_fn

    def fit(self, X, y):
        self.weights = np.zeros(len(X[0]))
        y_true = np.array([1.0 if i > 0.0 else 0.0 for i in y])

        for _ in range(self.n_iteration):
            for idx, x_i in enumerate(X):
                output = np.dot(x_i, self.weights)
                y_predicted = self.activation_function(output)
                y_star = (y_true[idx] - y_predicted)
                self.weights += y_star * x_i

    def activation_fn(self, x):
        return 1.0 if x >= 0 else 0

class LogisticRegression:
        def __init__(self, x, y, learning_rate=0.1, n_iteration=100):
            self.learning_rate = learning_rate
            self.n_iteration = n_iteration
            self.x = x
            self.y = y
 
   #Sigmoid method
        def sigmoid(self, input):    
            return 1 / (1 + np.exp(-input))

        # def gradient_descent(self, X, h, y):
        #     return np.dot(X.T, (h - y)) / y.shape[0]

        def fit(self,X,y):
            self.weights = np.zeros(len(X[0]))
            y_true = np.array([1.0 if i > 0.0 else 0.0 for i in y])

            for _ in range(self.n_iteration):
                for xi, idx in zip(X, y):
                    z = self.sigmoid(np.dot(xi, self.weights))
                    a,b=xi[0],xi[1]
                    self.weights[0] += self.learning_rate * (idx-z) * a
                    self.weights[1] += self.learning_rate * (idx-z) * b
    
    #Method to predict the class label.
        def predict(self, X):
            final=np.dot(X, self.weights)
            outcome=np.round(self.sigmoid(final).flatten(),2)
            result = list(outcome)
            return result

input_sequence = input("Enter the input pattern of the fetaures and labels: ") 

def parser(input_sequence):
  mode = input_sequence[:1]
  features = []
  labels = []
  while 1:
    start = 0
    end = 0
    if not input_sequence:
      break
    for i,char in enumerate(input_sequence):
      if char == "(":
        start = i
      if char == ")":
        end = i
        break
    numbers = input_sequence[start+1:end].split(",")
    features.append([int(numbers[0].strip()), int(numbers[1].strip())])
    labels.append(float(numbers[2].strip()))
    input_sequence = input_sequence[end+1:]
  return mode, np.array(features), np.array(labels)

algo,X,y = parser(input_sequence)
y_true = np.array([1 if i > 0 else 0 for i in y])

if algo == 'P':
    perceptron = Perceptron(n_iteration=100)
    perceptron.fit(X,y )
    x=(perceptron.weights)
    print(x.tolist())
else:   
    regressor = LogisticRegression(X, y, learning_rate=0.1, n_iteration=100)
    regressor.fit(X,y_true)
    print(*regressor.predict(X))
