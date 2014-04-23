from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory

import constants
import json

PORT = 23316

# Load django models
import sys, os
sys.path.append(os.path.abspath('..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'CustomerServiceAnalyzer.settings'

from django.db.models.loading import get_models
loaded_models = get_models()

from employee.models import Employee, EmployeeChatList
from chat.models import Chat

class ChatHandler(basic.LineReceiver):
    def __init__(self):
        self.client_type       = -1   # Type of client
        self.associated_client = None # Connected client in chat session
        self.available         = True # Used if an employee and signifies availability
        self.chat_id           = -1   # Current chat id session
        self.name              = ""   # Name of the client
        self.employee          = None # Associated employee object if type is employee

    def connectionMade(self):
        print "Client joined " + str(self)

    def connectionLost(self, reason):
        if self.client_type == constants.ENTITY_TYPE_EMPLOYEE:
            self.factory.employees.remove(self)
            print "Employee " + str(self.name) + " disconnected"
        elif self.client_type == constants.ENTITY_TYPE_CUSTOMER:
            if (self.associated_client):
                self.associated_client.available = True    
                self.associated_client.chat_id   = -1
            print "Customer " + str(self.name) + " disconnected"

    def dataReceived(self, data):
        try:
            message = json.loads(data)
            self.validate_json(message)
        except KeyError, e:
            print "Missing json input: " + str(e)
            self.send_error("Missing json input: " + str(e))
        except Exception, e:
            print "Invalid json input " + str(data)
            self.send_error("Invalid json input" + str(e))
            return

        if (message['action'] == constants.ACTION_JOIN):
            self.handle_join(message)
        elif (message['action'] == constants.ACTION_MESSAGE):
            self.handle_message(message)
        elif (message['action'] == constants.ACTION_LEAVE):
            self.handle_leave(message)
        else:
            self.send_error("Missing action entry")

        print message

    def message(self, message):
        self.transport.write(message + '\n')

    def handle_join(self, message):
        response = {}

        # If the client is an employee
        if (message['entity_type'] == constants.ENTITY_TYPE_EMPLOYEE):
            # Retrieve the associated employee
            try:
                employee = Employee.objects.get(user__id=message['id'])
            except Exception, e:
                self.send_error("Employee with id " + str(message['id']) + " doesn't exist")
                return

            self.employee = employee
            self.client_type = constants.ENTITY_TYPE_EMPLOYEE
            self.factory.employees.append(self)
            self.name = message['name']
        
        # If the client is a customer
        elif (message['entity_type'] == constants.ENTITY_TYPE_CUSTOMER):
            self.client_type = constants.ENTITY_TYPE_CUSTOMER
            self.name        = message['name']
            
            employee_found = False

            # Assign customer to a representative
            for employee in self.factory.employees:
                if (employee.available):
                    employee.associated_client = self
                    employee.available         = False
                    self.associated_client     = employee
                    employee_found             = True
                    break

            if (employee_found):
                print "Customer " + str(self.name) + " has joined"

                # Create new chat log
                new_chat_log = EmployeeChatList(employee=self.associated_client.employee, customer_name = self.name)
                new_chat_log.save()

                self.chat_id = new_chat_log.chat_id
                self.associated_client.chat_id = new_chat_log.chat_id

                # Generate response message
                response['type'] = constants.SUCCESS
                response['message'] = "Connected with representative " + self.associated_client.name

                # Send connected message to representative
                representative_response = {}
                representative_response['type'] = constants.SUCCESS
                representative_response['name'] = self.name
                representative_response['chat_id'] = self.chat_id
                representative_response['message'] = self.chat_id
                self.associated_client.message(json.dumps(representative_response))
            else:
                print "No available employee"
                response['type'] = constants.ERROR
                response['message'] = "No customer service representative available"

            self.message(json.dumps(response))

    def handle_message(self, message):
        response = {}

        if (self.associated_client):
            response['type'] = constants.SUCCESS
            response['name'] = self.name
            response['message'] = message['message']
            self.associated_client.message(json.dumps(response))
        else:
            response['type'] = constants.ERROR
            response['message'] = "Client not conencted"
            self.message(json.dumps(response))

        # Save the message to the database
        is_employee = False
        if (self.client_type == constants.ENTITY_TYPE_EMPLOYEE):
            is_employee = True

        c = Chat(chat_id=self.chat_id, message=message['message'], is_employee=is_employee)
        c.save()
        
    def send_error(self, text):
        response = {}
        response['type'] = constants.ERROR
        response['message'] = text
        self.message(json.dumps(response))

    def json_join_validator(self, json_input):
        try:
            json_input['id']
            json_input['name']
            json_input['entity_type']
        except KeyError, e:
            raise e

    def json_message_validator(self, json_input):
        try:
            json_input['message']
        except KeyError, e:
            raise e

    def validate_json(self, json_input):
        try:
            if (json_input['action'] == constants.ACTION_JOIN):
                self.json_join_validator
            elif (json_input['action'] == constants.ACTION_MESSAGE):
                self.json_message_validator
        except KeyError, e:
            raise e

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import protocol
from twisted.application import service, internet

from twisted.internet.protocol import Factory

class ChatFactory(Factory):
	protocol = ChatHandler
	employees = []

resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
root = Resource()

root.putChild("ws", resource)

application = service.Application("chatserver")
internet.TCPServer(PORT, Site(root)).setServiceParent(application)
