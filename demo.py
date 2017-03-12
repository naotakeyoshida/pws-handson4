#!/usr/bin/python

import os
import uuid
import urlparse
import json
import redis
from flask import Flask

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

app = Flask(__name__)
port = int(os.getenv("PORT"))
myuuid = str(uuid.uuid1())
myinstance = str(os.getenv("CF_INSTANCE_INDEX", 0))

@app.route('/')
def main():
    counter = r.incr("yoshi:incr")
    return """
    <html>
    <head>
      <title> Pivotal Cloud Foundry Demo </title>
    </head>
    <body>
      <center><FONT size="6" color="black">====== Dell EMC ======</FONT>
      <center><b><FONT size="7" color="black">PWS hands-on for Redis!</FONT></b>
      <br>
      <br>
      <br>
      <center><h1> App Instance : <font color="blue"> {}
      <br>
      <br>
      <center><FONT size="4" color="blue">UUID : {}</FONT>
      <center><h1> Access Counter : <font color="blue"> {}
      <br>
      <br>
      </center>
    </body>
    </html>
    """.format(myinstance, myuuid, counter, )
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
