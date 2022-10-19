'''
Linear regression

FLYNN RICHARDSON

Main file for linear regression and model selection.
'''

import numpy as np
from sklearn.model_selection import train_test_split
import util


class DataSet(object):
    '''
    Class for representing a data set.
    '''

    def __init__(self, dir_path):
        '''
        Class for representing a dataset, performs train/test
        splitting.

        Inputs:
            dir_path: (string) path to the directory that contains the
              file
        '''

        parameters_dict = util.load_json_file(dir_path, "parameters.json")
        self.pred_vars = parameters_dict["predictor_vars"]
        self.name = parameters_dict["name"]
        self.dependent_var = parameters_dict["dependent_var"]
        self.training_fraction = parameters_dict["training_fraction"]
        self.seed = parameters_dict["seed"]
        self.labels, data = util.load_numpy_array(dir_path, "data.csv")
        self.training_data, self.testing_data = train_test_split(data,
            train_size=self.training_fraction, test_size=None,
            random_state=self.seed)


class Model(object):
    '''
    Class for representing a model.
    '''

    def __init__(self, dataset, pred_vars):
        '''
        Construct a data structure to hold the model.
        Inputs:
            dataset: an dataset instance
            pred_vars: a list of the indices for the columns (of the
              original data array) used in the model.
        '''
        self.pred_vars = pred_vars
        self.dep_var = dataset.dependent_var
        self.beta = util.linear_regression(util.prepend_ones_column(dataset.training_data[:, self.pred_vars]), \
                                           dataset.training_data[:, self.dep_var])
        self.R2 = self.calculate_R2(dataset.training_data)


    def calculate_R2(self, data):
        '''
        Calculates the coefficient of determination

        Inputs:
            data: a subset of a dataset
        
        Returns: (int) R^2 value
        '''
        y_hat = util.apply_beta(self.beta, util.prepend_ones_column(data[:, self.pred_vars]))
        y = data[:, self.dep_var]

        return 1 - np.sum((y - y_hat)**2) / np.sum((y - y.mean())**2)


    def __repr__(self):
        '''
        Format model as a string.
        '''

def compute_single_var_models(dataset):
    '''
    Computes all the single-variable models for a dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        List of Model objects, each representing a single-variable model
    '''
    return [Model(dataset, [pred_var]) for pred_var in dataset.pred_vars]


def compute_all_vars_model(dataset):
    '''
    Computes a model that uses all the predictor variables in the dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object that uses all the predictor variables
    '''
    return Model(dataset, dataset.pred_vars)


def compute_best_pair(dataset):
    '''
    Find the bivariate model with the best R2 value

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object for the best bivariate model
    '''
    best_bivariate_model = None
    best_R2 = 0

    for index, pred_var_one in enumerate(dataset.pred_vars):
        for pred_var_two in dataset.pred_vars[index + 1:]:
            new_model = Model(dataset, [pred_var_one, pred_var_two])
            if new_model.R2 > best_R2:
                best_R2 = new_model.R2
                best_bivariate_model = new_model
    
    return best_bivariate_model


def forward_selection(dataset):
    '''
    Given a dataset with P predictor variables, uses forward selection to
    select models for every value of K between 1 and P.

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A list (of length P) of Model objects. The first element is the
        model where K=1, the second element is the model where K=2, and so on.
    '''
    models = []
    used_variables = []

    for __, __ in enumerate(dataset.pred_vars):
        best_model = None
        best_variable = None
        best_R2 = 0
        for pred_var in dataset.pred_vars:
            if pred_var not in used_variables:
                new_model = Model(dataset, [pred_var] + used_variables)
                if new_model.R2 > best_R2:
                    best_R2 = new_model.R2
                    best_model = new_model
                    best_variable = pred_var
        used_variables.append(best_variable)
        models.append(best_model)
    
    return models


def validate_model(dataset, model):
    '''
    Given a dataset and a model trained on the training data,
    compute the R2 of applying that model to the testing data.

    Inputs:
        dataset: (DataSet object) a dataset
        model: (Model object) A model that must have been trained
           on the dataset's training data.

    Returns:
        (float) An R2 value
    '''
    return model.calculate_R2(dataset.testing_data)