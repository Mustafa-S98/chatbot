from flask import Flask, render_template, request, session
from BankFAQbot import *

app = Flask(__name__)
app.secret_key = "session_key"

@app.route('/')
def home():
    return render_template('home.html')
    

@app.route('/chat', methods = ['GET'])
def index():
    for i in request.args.keys():
        if i == 'name':
            session['name'] = request.args['name']
            session['msg'] = ['Bot : Hello ' + session['name'], '      TYPE \"DEBUG\" to Display Debugging statements.', '      TYPE \"STOP\" to Stop Debugging statements.']
            session['msg'].append('      TYPE \"TOP5\" to Display 5 most relevent results')
            session['msg'].append('      TYPE \"CONF\" to Display the most confident result')
        
        else:
            session['msg'] = [session['name'] + ' : ' + request.args['msg']]
            # print("-----x-----")
            # print(session['msg'][0].split()[1])
            # print("-----x-----")
            result = chat(session['msg'][0].split()[1])
            session['msg'].append('Bot  :' + '; '.join(result))

    print(session['msg'])
    return render_template("template.html", msg = session['msg'])
    
    
if __name__ == "__main__":
    app.run()