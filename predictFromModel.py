import pandas as pd
from file_operations import file_methods
from data_preprocessing import preprocessing
from application_logging import logger 
from data_ingestion import data_loader

class prediction:
    def __init__(self,path):
        self.file_object=open("Prediction_Logs/Prediction_Log.txt",'a+')
        self.log_writer=logger.App_Logger()
        if path is not None:
            self.file_op=file_methods.File_Operation(self.file_object,self.log_writer)
    
    def predictionFromModel(self):
        try:
            self.file_op.deletePredictionFile()
            self.log_writer.log(self.file_object,'Start of Prediction')
            data_getter=data_loader.Data_Getter(self.file_object,self.log_writer)
            data=data_getter.get_data_predict()
            preprocessor=preprocessing.Preprocessor(self.file_object,self.log_writer)
            onehot_encode_cols=['promotion_name','sales_country']
            data=preprocessor.encode_data_prediction(data,onehot_encode_cols)
            is_null_present=preprocessor.is_null_present(data)
            if(is_null_present):
                data=preprocessor.impute_missing_values(data)
            model_name=self.file_op.find_correct_model_file()
            model=self.file_op.load_model(model_name)
            result=pd.DataFrame(model.predict(data))
            result.to_csv("Prediction_Output_File/Predictions.csv",header=True,mode='a+')
            self.log_writer.log(self.file_object,'End of Prediction')
        except Exception as e:
            self.log_writer.log(self.file_object,'Error occurred while running prediction. Error:: %s' %e)
            raise e 
        return result.head().to_json(orient="records")


