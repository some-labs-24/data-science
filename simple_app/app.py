from flask import Flask,request,jsonify

def create_app():
    app = Flask(__name__)
   

    

    @app.route('/recommand',methods=['GET'])
    def recommanded():

        return jsonify({
      "recommended_time": "1PM"
})

    return app