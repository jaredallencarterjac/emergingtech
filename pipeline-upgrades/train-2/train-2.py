import argparse
import joblib
import numpy as np
from sklearn import tree

def train_model(x_train, y_train):
    x_train_data = np.load(x_train)
    y_train_data = np.load(y_train)
#type of model
    model_2 = tree.DecisionTreeRegressor()
    model_2.fit(x_train_data, y_train_data)
#packaging model into a file we can use later
    joblib.dump(model_2, 'model_2.pkl')


if __name__ == '__main__':
#accepting the file paths to the training data, from the pipeline.py
    parser = argparse.ArgumentParser()
    parser.add_argument('--x_train')
    parser.add_argument('--y_train')
    args = parser.parse_args()
    train_model(args.x_train, args.y_train)
