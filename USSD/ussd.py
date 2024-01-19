import os
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request

cred = credentials.Certificate('/the/path/to/your/serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com'
})

app = Flask(__name__)

# user_data = {}

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default").split('*')

    user_ref = db.reference(f'users/{phone_number}')
    user_data = user_ref.get() or {'expenses': {}, 'budget': '0'}
    if phone_number not in user_data:
        user_data[phone_number] = {'expenses': {}, 'budget': 0}

    if text == ['']:
        response = "CON What would you want to do \n"
        response += "1. Add Expense \n"
        response += "2. Check Expenses \n"
        response += "3. Set Budget Alert"
    elif text == ['1']:
        response = "CON Enter the category and amount for the expense in the format 'category*amount'"
    elif text[0] == '1' and len(text) == 3:
        category, amount = text[1], text[2]
        user_data[phone_number]['expenses'][category] = user_data[phone_number]['expenses'].get(category, 0) + int(amount)
        response = "END Expense added successfully"
    elif text == ['2']:
        response = "END Here are your expenses: \n" + '\n'.join([f"{cat}: {amt}" for cat, amt in user_data[phone_number]['expenses'].items()])
    elif text == ['3']:
        response = "CON Enter the budget limit"
    elif text[0] == '3' and len(text) == 2:
        user_data[phone_number]['budget'] = int(text[1])
        response = "END Budget limit set successfully"
    
    # Check if budget limit is exceeded and send a notification
    if sum(user_data[phone_number]['expenses'].values()) > user_data[phone_number]['budget']:
        response += "\nYou have exceeded your budget limit!"

    user_ref.set(user_data)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))