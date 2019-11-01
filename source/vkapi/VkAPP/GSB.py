from flask import Flask, render_template, request

from source.databases.UserDB import UserDB

app = Flask(__name__, template_folder="./templates")


@app.route("/gsb", methods=['GET'])
def get_r():
    return render_template('index_template.html')


@app.route("/gsb", methods=['POST'])
def calculate():
    user_id = request.args['user_id']
    UserDB.balance_changer(user_id=user_id, value=1)
    return 'ok'
