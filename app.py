from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

# @app.route('/',methods=['POST','GET'])
# def index():
#     data = request.get_json()
#     # source_c = "USD"
#     # target_c = "AED"
#     source_currency = data['queryResult']['parameters']['unit-currency']['currency']
#     amount = data['queryResult']['parameters']['unit-currency']['amount']
#     target_currency = data['queryResult']['parameters']['currency-name']

#     cf = fetch_currency_factor(source_currency, target_currency)
#     final_amount = round(amount * cf,2)

#     response = {
#         "fulfillmentText": "{} {} is {} {}".format(amount, source_currency,final_amount, target_currency)
#     }

#     return jsonify(response)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return "GET request received. App is running."

    # POST request handling
    data = request.get_json()

    try:
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        cf = fetch_currency_factor(source_currency, target_currency)
        final_amount = round(amount * cf, 2)

        response = {
            "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
        }

    except Exception as e:
        response = {
            "fulfillmentText": f"Sorry, I couldn't process your request: {str(e)}"
        }

    return jsonify(response)



def fetch_currency_factor(source_c, target_c):
    url = 'https://v6.exchangerate-api.com/v6/db956c8ac098a5aaa578089e/latest/{}'.format(source_c)

    # Making our request
    response = requests.get(url)
    data = response.json()
    rate = data['conversion_rates'][target_c]
    
    return rate

if __name__ == '__main__':
    app.run(debug=True)
