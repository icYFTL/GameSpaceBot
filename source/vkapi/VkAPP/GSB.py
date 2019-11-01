from flask import Flask, render_template, request

app = Flask(__name__, template_folder="./templates")


@app.route("/gsb", methods=['GET'])
def get_r():
    return render_template('index_template.html')


@app.route("/gsb", methods=['POST'])
def calculate():
    if request.data:
        print(request.data)
    return 'ok'
