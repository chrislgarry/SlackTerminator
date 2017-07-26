# SlackTerminator
Delete all of the messages in a Slack channel.

# Dependencies

1. [Slack Python SDK](https://github.com/slackapi/python-slackclient), Slack API token with permissions (see below).
2. [Python](https://www.python.org/)

This script was developed and tested with Slack Python SDK version ```1.0.6```, Python version ```2.7.13```.

# Slack Permissions
The Slack app tied to the API token must have the necessary permissions for channels.list (to find the ID of the channel), channels.history (get all messages from the channel), and chat.delete (delete messages from the channel).

# Install

1. Install [Slack Python SDK](https://github.com/slackapi/python-slackclient).

2. Clone this repo.

# Usage

In this repo, from commandline:

```
export SLACK_API_TOKEN=<your-slack-api-token>
user$ python slackterminator.py --help
usage: slackterminator.py [-h] --channel_name <channel name without hashtag>

Delete all messages from a given Slack channel.

optional arguments:
  -h, --help            show this help message and exit
  --channel_name <channel name without hashtag>
                        The name of the Slack channel to delete all messages
                        in.
```
