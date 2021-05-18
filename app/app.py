from flask import Flask,render_template,jsonify,request
import socket
from sim_hownet import SimHownet
app = Flask(__name__)

@app.route("/")
def index():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return render_template('index.html', hostname=host_name, ip=host_ip)
    except:
        return render_template('error.html')

@app.route('/sim', methods=['POST'])
def sim():
    query = request.form['query']
    targets = request.form['targets'][1:-1].replace('\"','')
    query=query.replace('_','').replace('-','').replace(' ','')
    for i in range(9):
        query=query.replace(str(i),'')
    targets=targets.split(',')
    similarity=[simer.distance(query,target) for target in targets]
    return jsonify({str(target):similarity[index] for index,target in enumerate(targets)}),200

if __name__ == "__main__":
    simer=SimHownet()
    app.run(host='0.0.0.0', port=8080)
