from wsgiref import simple_server
from flask import Flask, request, render_template, Response
import os
import pandas as pd
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
        try:
            data = {
                'sales_country': request.form.get('sales_country'),
                'n_products': int(request.form.get('n_products')),
                'promotion_name': request.form.get('promotion_name'),
                'store_id_0': int(request.form.get('store_id_0', 0)),
                'store_id_1': int(request.form.get('store_id_1', 0)),
                'store_id_2': int(request.form.get('store_id_2', 0)),
                'store_id_3': int(request.form.get('store_id_3', 0)),
                'store_id_4': int(request.form.get('store_id_4', 0)),
                'store_id_5': int(request.form.get('store_id_5', 0)),
                'store_id_6': int(request.form.get('store_id_6', 0)),
                'store_id_7': int(request.form.get('store_id_7', 0)),
                'store_id_8': int(request.form.get('store_id_8', 0)),
                'store_id_9': int(request.form.get('store_id_9', 0)),
                'store_id_10': int(request.form.get('store_id_10', 0)),
                'store_id_11': int(request.form.get('store_id_11', 0)),
                'store_id_12': int(request.form.get('store_id_12', 0)),
                'store_id_13': int(request.form.get('store_id_13', 0)),
                'store_id_14': int(request.form.get('store_id_14', 0)),
                'store_id_15': int(request.form.get('store_id_15', 0)),
                'store_id_16': int(request.form.get('store_id_16', 0)),
                'store_id_17': int(request.form.get('store_id_17', 0)),
                'store_id_18': int(request.form.get('store_id_18', 0)),
                'store_id_19': int(request.form.get('store_id_19', 0)),
                'Daily_Paper': int(request.form.get('Daily_Paper', 0)),
                'Radio': int(request.form.get('Radio', 0)),
                'In_Store_Coupon': int(request.form.get('In_Store_Coupon', 0)),
                'Product_Attachment': int(request.form.get('Product_Attachment', 0)),
                'Sunday_Paper': int(request.form.get('Sunday_Paper', 0)),
                'TV': int(request.form.get('TV', 0)),
                'Street_Handout': int(request.form.get('Street_Handout', 0)),
                'Bulk_Mail': int(request.form.get('Bulk_Mail', 0)),
                'Cash_Register_Handout': int(request.form.get('Cash_Register_Handout', 0)),
            }

            df = pd.DataFrame([data])
            print(df)
            pred = prediction(df)
            predicted_result = pred.predictionFromModel()  
            if not predicted_result.empty:
                predicted_value = predicted_result.iloc[0, 0]
                print(predicted_value)
            return render_template('index.html', prediction=predicted_value)
        except Exception as e:
            print(f"Error occurred: {e}")
            return render_template('index.html', error=str(e))

    return render_template('index.html')

port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    app.run(debug=True)
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
