from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
app = Flask(__name__)

VALID_USERNAME = 'siddharth'
VALID_PASSWORD = 'password'


creds = ServiceAccountCredentials.from_json_keyfile_name('vertical-sunset-400909-16ac0f419f04.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(creds)

sheet1 = client.open_by_key('1UQ87xCSp3Ao6QNR_YWlCyJK5XKf6q-mI7vhCfJXKOO8').sheet1
values = sheet1.get_all_records()
df = pd.DataFrame(values)
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
sheet2 = client.open_by_key('11SRykmr3glZjT5XPnX4g90mm6k9yjNKqpnmPi8zMFNU').sheet1
values1 = sheet2.get_all_records()
df1 = pd.DataFrame(values1)
df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%Y-%m-%d')
#excel_file = 'exc1.xlsx'
#df = pd.read_excel(excel_file)
#df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
#excel_file1 = 'exc2.xlsx'
#df1 = pd.read_excel(excel_file1)
#df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%Y-%m-%d')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            wishes_data = df[['Wish', 'From','Date']].to_dict(orient='records')
            appreciations_data = df1[['Appreciations', 'From','Date']].to_dict(orient='records')
            print(appreciations_data)
            return render_template('index.html', wishes_data=wishes_data, appreciations_data=appreciations_data, username=username)
        else:
            return redirect(url_for('login.html'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)