#!/usr/bin/python

from mastodon import Mastodon, StreamListener
from html.parser import HTMLParser    # for parsing toots
from textgenrnn import textgenrnn     # for generative text
import os.path                        # for getting settings from config files

###############################################################################
# INITIALISATION
###############################################################################

# Return the parameter from the specified file
def get_parameter(parameter, file_path):
    # Check if secrets file exists
    if not os.path.isfile(file_path):    
        print("File %s not found, exiting."%file_path)
        sys.exit(0)

    # Find parameter in file
    with open(file_path) as f:
        for line in f:
            if line.startswith(parameter):
                return line.replace(parameter + ":", "").strip()

    # Cannot find parameter, exit
    print(file_path + "  Missing parameter %s "%parameter)
    sys.exit(0)
	
# Load secrets from secrets file
secrets_filepath = "secrets/secrets.txt"
uc_client_id     = get_parameter("uc_client_id",     secrets_filepath)
uc_client_secret = get_parameter("uc_client_secret", secrets_filepath)
uc_access_token  = get_parameter("uc_access_token",  secrets_filepath)

# Load configuration from config file
config_filepath = "config.txt"
mastodon_hostname = get_parameter("mastodon_hostname", config_filepath) # E.g., mastodon.social

# Initialise Mastodon API
mastodon = Mastodon(
    client_id = uc_client_id,
    client_secret = uc_client_secret,
    access_token = uc_access_token,
    api_base_url = 'https://' + mastodon_hostname,
)

###############################################################################
# STREAM LISTENER SETUP
###############################################################################
	
# parser class - scrapes the last bit of data (the toot) from parsed HTML
class myParser(HTMLParser):
	def handle_data(self, data):
		self.data = data
		
# get text from a single toot
def parse_toot(content):
	parser = myParser()
	parser.feed(content)
	return parser.data.strip()
	
# get corpus of all status texts
def get_corpus(statuses):
	corpus = []
	for s in statuses:
		toot_text = parse_toot(s['content'])
		corpus.append(toot_text)
	return corpus
	
# train neural network on corpus and get response
def get_response(corpus):
	textgen = textgenrnn()
	textgen.train_on_texts(corpus, num_epochs=2, gen_epochs=2)
	return textgen.generate(1, True)[0]
	
# a test function to post unlisted toots, so as not to spam the local timeline
def test_toot(status, replyid=None):
	mastodon.status_post(status, replyid, None, False, 'unlisted', None, None, None)
		
# listener class - contains method that is executed on mention notification
class myListener(StreamListener):
	def on_notification(self, notification):
		# show all notifications in the terminal
		print('Received notification of type {}'.format(notification['type']))
		if notification['type'] != 'mention':
			return
		
		mentioner = notification['account']
		statuses = mastodon.account_statuses(mentioner['id'])
		corpus = get_corpus(statuses)
		response = get_response(corpus)
		
		toot_string = '{}: \'{}\''.format('@'+mentioner['username'], response)
		mention = notification['status']
		test_toot(toot_string, mention['id'])
		print('Echoed response: {}'.format(toot_string))

# run the listener
listener = myListener()
print('Listening for mentions...')
mastodon.stream_user(listener)