from keras.layers import Input, Dense
from keras.models import Model
import pandas as pd

from sklearn.model_selection import train_test_split


class FunctionNN():
    def __init__(self, data):
        self.data = pd.read_csv(data)

        self.setup_data()

        self.setup_model()
    
    def setup_data(self):
        # Split the data into inputs (iteration and effectiveness) and outputs (function)
        X = self.data[['iteration', 'effectiveness']]
        y = self.data['function']

        # One hot encoding the y
        y = pd.get_dummies(y)

        # Split the data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2)

    def setup_model(self):

        # Input layer with 2 neurons (for iteration and effectiveness)
        inputs = Input(shape=(2,))

        # Hidden layer with 8 neurons
        x = Dense(8, activation='relu')(inputs)

        # Output layer with 4 neurons (for the 4 functions)
        outputs = Dense(4, activation='softmax')(x)

        # Create the model
        self.model = Model(inputs=inputs, outputs=outputs)

        # Compile the model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    def train(self):
        # Use the model.fit() method to train the neural network
        self.model.fit(self.X_train, self.y_train, epochs=20, batch_size=10)

        print(self.model.summary())

        # Input data (1 sample with 1 feature)
        iteration = 3
        input_data = [[iteration]]

        # Make a prediction
        predictions = self.model.predict(input_data)

        # The output is a probability distribution over the different functions
        print(predictions)

if __name__ == "__main__":
    NN = FunctionNN("data/HCresults.csv")
    print(NN.data)
    NN.train()



