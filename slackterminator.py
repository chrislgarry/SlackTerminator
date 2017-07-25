import argparse
import os
from slackclient import SlackClient
import sys
import time

#Commandline help
parser = argparse.ArgumentParser(description="Delete all messages from a given Slack channel.")
parser.add_argument('--channel_name', required=True, metavar="<channel name without hashtag>",
                   help="The name of the Slack channel to delete all messages in.")
args = parser.parse_args()

#Initialization
slack_token = os.environ["SLACK_API_TOKEN"]
slack_client = SlackClient(slack_token)

#Delay as suggested by Slack team. Faster might work, but risk being throttled/blocked.
ratelimit_delay_s = 1


def get_messages (channel_name, pagination_count=1000):
	channel_id = get_channel_id(channel_name)
	print "retrieving message history of channel: {}".format(channel_name)
	response = slack_client.api_call(
	  "channels.history",
	  channel=channel_id,
	  count=pagination_count,
	)
	validate(response)
	messages = response["messages"]
	return messages


def delete_message (channel_id, timestamp):
	"deleting message at timestamp: %f".format(timestamp,)
	response = slack_client.api_call(
	  "chat.delete",
	  channel=channel_id,
	  ts=timestamp
	)
	validate(response)
	return response


def delete_all_messages (channel_name):
	messages = get_messages(channel_name)
	channel_id = get_channel_id(channel_name)
	if messages == []:
		print "The provided channel contains no messages."
		exit()
	else:
		for message in messages:
			timestamp = message["ts"]
	        response = delete_message(channel_id, timestamp)
	        print response
	        time.sleep(ratelimit_delay_s)


def get_channels ():
	response = slack_client.api_call(
	  "channels.list"
	)
	channels = response["channels"]
	return channels


def get_channel_id (channel_name):
	channels = get_channels()
	for channel in channels:
		if channel["name"] == channel_name:
			return channel["id"]

# Entry point
def start ():
	print "Are you sure you want to delete all messages in channel {}? y/n:".format(args.channel_name,)
	confirm = raw_input()
	if confirm == 'y' or confirm == 'Y':
		delete_all_messages(args.channel_name)
	else:
		print "No messages were deleted."

def validate (response):
	if response["ok"] == False:
		print response
		exit()

start()