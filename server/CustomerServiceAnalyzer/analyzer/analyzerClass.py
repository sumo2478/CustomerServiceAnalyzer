import json
from urllib import urlencode
from urllib2 import urlopen

from chat.models import Chat
from employee.models import EmployeeChatList

class Analyzer(object):
	"""Chat Sentiment Analyzer Class"""
	def __init__(self):
		self.api_url = "https://api.sentigem.com/external/get-sentiment"
		self.api_key = "6352f666047a4a30aa8f346d7793d5296Twn2FfkboMSWjt9OYg5PyAJG7v8BK1q"
	
	def get_score(self, text):
		"""
		get_score - retrieves the sentiment analysis on a piece of text
		@text - str, the text to be analyzed
		@return - str, the polarity of the score either "neutral", "positive", or "negative"
		"""
		search_url = [self.api_url, '?']
		args = {'api-key': self.api_key, 'text':text}

		search_url.append(urlencode(args))

		data = json.loads(urlopen(''.join(search_url)).read())
		score = data['polarity']
		
		if score == 'positive':
			return 1
		elif score == 'negative':
			return -1
		else: 
			return 0

	def analyze_chat_log(self, chat_id):
		"""
		analyze_chat_log - analyzes an entire chat log given a chat_id
		@chat_id - int, the chat identifier number
		@return  - int, returns 0 on success
		"""
		messages = Chat.objects.filter(chat_id=chat_id)
		total_score = 0

		for message in messages:
			score = self.get_score(message.message)
			message.score = score
			message.save()

			if message.is_employee:
				total_score = total_score + score

		employee_chat = EmployeeChatList.objects.get(chat_id=chat_id)
		employee_chat.score = total_score
		employee_chat.save()

		return messages

	def analyze_and_store_message(self, chat_id, entry):
		"""
		analyze_and_store_message - analyzes and stores a single log message
		@chat_id - int, the chat identifier number
		@entry   - {"message": , "is_employee":} - JSON log entry
		@return  - int, sentiment score for message
		"""
		score = self.get_score(entry['message'])
		message = Chat(chat_id=chat_id, message=entry['message'], is_employee=entry['is_employee'], score=score)
		message.save()
		return score

	def create_histogram(self, messages):
		"""
		Create Histogram

		Function that takes a list of messages and converts the scores 
		into a histogram formatted list 
		"""
		running_total = 0
		scores = []
		for message in messages:
			if not message.is_employee:
				running_total += message.score
				scores.append(running_total)

		return scores

				
