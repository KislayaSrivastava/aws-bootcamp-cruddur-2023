from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os
from random import randint
import sys
import logging

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *


#new Library Flask-AWSCognito
#from flask_awscognito import AWSCognitoAuthentication
from lib.cognito_token_verification import CognitoTokenVerification

#HoneyComb -------------
from opentelemetry import trace
from opentelemetry import metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

#X-RAY --------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Crudder',dynamic_naming=xray_url)


#HoneyComb --------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter("HoneyComb-Testing-Meter")

#CloudWatch Logs
import watchtower
import logging
from time import strftime

#RollBar -----
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
#LOGGER.info("some message")

app = Flask(__name__)

#new Library Testing
cognito_token_verification = CognitoTokenVerification(
  
)
#new library Testing
#XRAY ----
XRayMiddleware(app,xray_recorder)
#HoneyComb --------
#Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
#for Error logging in CloudWatch Logs
#@app.after_request
#def after_request(response):
#    timestamp = strftime('[%Y-%b-%d %H:%M]')
#    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#    return response


#RollBar Testing ----
#RollBar
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
#@app.before_first_request
#def init_rollbar():
#    """init rollbar module"""
#    rollbar.init(
#        # access token
#        rollbar_access_token,
#        # environment name
#        'production',
#        # server root directory, makes tracebacks prettier
#        root=os.path.dirname(os.path.realpath(__file__)),
#        # flask already sets up logging
#        allow_logging_basic_config=False)

#   # send exceptions from `app` to rollbar, using flask's signal system.
#    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

#For RollBar Testing one route ----
#@app.route('/rollbar/test')
#def rollbar_test():
#    rollbar.report_message('Hello World!', 'warning')
#    return "Hello World!"

roll_counter = meter.create_counter(
    "roll_counter",
    description="The number of rolls by roll value",
)

#For HoneyComb Testing------
@app.route('/honeycomb/test')
def honeycomb_test():
  #found the current span 
  #added two extra Attributes, version and roll.value
  #added an custom span
  current_span = trace.get_current_span()
  current_span.set_attribute("version","2.2.2") #added Extra Attribute
  with tracer.start_as_current_span("calculate") as rollspan:
          res = str(randint(1, 6))
          rollspan.set_attribute("roll.value", res)
          # This adds 1 to the counter for the given roll value
          roll_counter.add(1, {"roll.value": res})
          return res
#End of HoneyComb Testing------

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'andrewbrown'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture('My_API-Activities_SubSegment') #Xray Subsegment ---
#@aws_auth.authentication_required   #New Code for Testing
def data_home():
  #For Testing Logging
  #app.logger.debug('AUTH HEADER 1----')
  #app.logger.debug(
  #  request.headers.get('Authorization')
  #)
  #app.logger.debug('AUTH HEADER 2----')
  data = HomeActivities.run()
  claims = aws_auth.claims   #Adding for new library testing
  app.logger.debug('claims')
  app.logger.debug(claims)   #for logging
  return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
@xray_recorder.capture('User-API-Activities_Show_SubSegment') #Xray Subsegment ---
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'andrewbrown'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
@xray_recorder.capture('My_API-Activities_Show_SubSegment') #Xray Subsegment ---
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

if __name__ == "__main__":
  app.run(debug=True)