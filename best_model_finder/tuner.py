from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

class Model_Finder:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.rf = RandomForestRegressor()
        self.xgb = XGBRegressor(objective='reg:squarederror')

    def get_best_params_for_random_forest(self, train_x, train_y):
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_random_forest method of the Model_Finder class')
        try:
            self.param_grid = {
                "n_estimators": [10, 50, 100, 130],
                "criterion": ['squared_error', 'absolute_error'],
                "max_depth": range(2, 4, 1),
                "max_features": ['sqrt', 'log2']
            }

            self.grid = GridSearchCV(estimator=self.rf, param_grid=self.param_grid, cv=5, verbose=3)
            self.grid.fit(train_x, train_y)

            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            self.rf = RandomForestRegressor(n_estimators=self.n_estimators, criterion=self.criterion, max_depth=self.max_depth, max_features=self.max_features)
            self.rf.fit(train_x, train_y)

            self.logger_object.log(self.file_object, 'Random Forest best params: ' + str(self.grid.best_params_) + '. Exited the get_best_params_for_random_forest method of the Model_Finder class')

            return self.rf
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_best_params_for_random_forest method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Random Forest Parameter tuning failed. Exited the get_best_params_for_random_forest method of the Model_Finder')
            raise Exception()

    def get_best_params_for_xgboost(self, train_x, train_y):
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_xgboost method of the Model_Finder class')
        try:
            self.param_grid_xgboost = {
                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]
            }

            self.grid = GridSearchCV(XGBRegressor(objective='reg:squarederror'), self.param_grid_xgboost, verbose=3, cv=5)
            self.grid.fit(train_x, train_y)

            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            self.xgb = XGBRegressor(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            self.xgb.fit(train_x, train_y)

            self.logger_object.log(self.file_object, 'XGBoost best params: ' + str(self.grid.best_params_) + '. Exited the get_best_params_for_xgboost method of the Model_Finder class')

            return self.xgb
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_best_params_for_xgboost method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'XGBoost parameter tuning failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise Exception()

    def get_best_model(self, train_x, train_y, test_x, test_y):
        self.logger_object.log(self.file_object, 'Entered the get_best_model method of the Model_Finder class')

        try:
            self.xgboost = self.get_best_params_for_xgboost(train_x, train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x)
            self.xgboost_score = mean_squared_error(test_y, self.prediction_xgboost)
            self.logger_object.log(self.file_object, 'MSE for XGBoost: ' + str(self.xgboost_score))

            self.random_forest = self.get_best_params_for_random_forest(train_x, train_y)
            self.prediction_random_forest = self.random_forest.predict(test_x)
            self.random_forest_score = mean_squared_error(test_y, self.prediction_random_forest)
            self.logger_object.log(self.file_object, 'MSE for RF: ' + str(self.random_forest_score))

            if self.random_forest_score < self.xgboost_score:
                self.logger_object.log(self.file_object, 'Got the best Model as RandomForest: ' + str(self.random_forest_score))
                return 'RandomForest', self.random_forest
            else:
                self.logger_object.log(self.file_object, 'Got the best Model as XGBoost: ' + str(self.xgboost_score))
                return 'XGBoost', self.xgboost

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_best_model method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()
