from wsgiref import simple_server
from flask import Flask, request, render_template, Response
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import json
from trainingModel import trainModel
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def home():
    if request.method == "POST":
        data = request.form
        sales_country = data.get("sales_country")
        n_products = data.get("n_products")
        promotion_name = data.get("promotion_name")
        
        store_ids = {f"store_id_{i}": data.get(f"store_id_{i}", "0") for i in range(20)}
        
        promotion_methods = {
            "Daily_Paper": data.get("Daily_Paper", "0"),
            "Radio": data.get("Radio", "0"),
            "In_Store_Coupon": data.get("In_Store_Coupon", "0"),
            "Product_Attachment": data.get("Product_Attachment", "0"),
            "Sunday_Paper": data.get("Sunday_Paper", "0"),
            "TV": data.get("TV", "0"),
            "Street_Handout": data.get("Street_Handout", "0"),
            "Bulk_Mail": data.get("Bulk_Mail", "0"),
            "Cash_Register_Handout": data.get("Cash_Register_Handout", "0")
        }
        
        print("Sales Country:", sales_country)
        print("Number of Products:", n_products)
        print("Promotion Name:", promotion_name)
        print("Store IDs:", store_ids)
        print("Promotion Methods:", promotion_methods)
        
        return render_template('index.html')
    
    return render_template('index.html')
# trainModelObj = trainModel()
# trainModelObj.trainingModel()
# path='D:\ACADEMIC\ML Projects\CAC Prediction\Prediction_Data_Files'
# pred = prediction(path)
# json_predictions = pred.predictionFromModel()

# @app.route("/train", methods=['POST'])
# @cross_origin()
# def trainRouteClient():
#     try:
#         if request.json and 'folderPath' in request.json:
#             path = request.json['folderPath']
#         else:
#             return Response("Invalid input format", status=400)
        
#         trainModelObj = trainModel()
#         trainModelObj.trainingModel()
#         return Response("Training successful")
#     except ValueError as ve:
#         return Response("Error Occurred! %s" % ve, status=500)
#     except KeyError as ke:
#         return Response("Error Occurred! %s" % ke, status=500)
#     except Exception as e:
#         return Response("Error Occurred! %s" % e, status=500)

# @app.route("/predict", methods=["POST"])
# @cross_origin()
# def predictRouteClient():
#     try:
#         if request.json is not None:
#             path = request.json['filepath']
#         elif request.form is not None:
#             path = request.form['filepath']
#         else:
#             return Response("Invalid input format", status=400)
        
#         pred_val = pred_validation(path)
#         pred_val.prediction_validation()
#         pred = prediction(path)
#         path, json_predictions = pred.predictionFromModel()
#         return Response("Prediction File created at: " + str(path) + ' and few of the predictions are: ' + str(json.loads(json_predictions)))
#     except ValueError as ve:
#         return Response("Error Occurred! %s" % ve, status=500)
#     except KeyError as ke:
#         return Response("Error Occurred! %s" % ke, status=500)
#     except Exception as e:
#         return Response("Error Occurred! %s" % e, status=500)

port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()