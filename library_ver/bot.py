# -*- coding: utf-8 -*-
"""
In this file, we'll create a python Bot Class.
"""
import os
import json
from slackclient import SlackClient


class Bot(object):
    """ Instanciates a Bot object to handle Slack interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      "scope": "bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.client = SlackClient("")

    def auth(self, code):
        """
        A method to exchange the temporary auth code for an OAuth token
        which is then saved it in memory on our Bot object for easier access.
        """
        auth_response = self.client.api_call("oauth.access",
                                             client_id=self.oauth['client_id'],
                                             client_secret=self.oauth[
                                                            'client_secret'],
                                             code=code)
        self.user_id = auth_response["bot"]["bot_user_id"]
        self.client = SlackClient(auth_response["bot"]["bot_access_token"])

    def say_hello(self, message):
        """
        A method to ask workshop attendees to build this bot. When a user clicks
        the button for their operating system, the bot should display the set-up
        instructions for that operating system.
        """
        hello_message = "I want to live! Please build me."
        message_attachments = [
            {
                "pretext": "I'll tell you how to set up your system. :robot_face:",
                "text": "What operating system are you using?",
                "callback_id": "os",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "mac",
                        "text": ":apple: Mac",
                        "type": "button",
                        "value": "mac"
                    },
                    {
                        "name": "windows",
                        "text": ":fax: Windows",
                        "type": "button",
                        "value": "win"
                    }
                ]
            }
        ]
        channel = message["channel"]
        self.client.api_call("chat.postMessage",
                             channel=channel,
                             text=hello_message,
                             attachments=json.dumps(message_attachments))

    def show_win(self):
        """
        Here we'll build a method to respond to a user's action taken from a
        message button. It should return a message with system setup
        instructions for building this bot on a Windows operating system.
        """
        pass

    def show_mac(self):
        """
        A method to respond to a user's action taken from a message button.
        Returns a message with system setup instructions for building this bot
        on a Mac operating system.
        """
        message = {
            "as_user": False,
            "replace_original": False,
            "response_type": "ephemeral",
            "text": ":apple: *Mac OS*:\n Here's some helpful tips for "
            "setting up the requirements you'll need for this workshop:",
            "attachments": [{
                "mrkdwn_in": ["text", "pretext"],
                "text": "*Python 2.7 and Pip*:\n_Check to see if you have "
                "Python on your system:_\n```which python && python "
                "--version```\n_If you have homebrew, you can use it to "
                "install python and pip:_\n```brew install python && pip```"
                "\n_If not, you can download python here:_Download link:_\n"
                "https://www.python.org/ftp/python/2.7.12/python-2.7.12-"
                "macosx10.6.pkg\n_After downloading Python, you must upgrade "
                "your version of Pip:_\n```pip install -U pip```\n"
                "*Virtualenv*:\n_Check to see if you have virtualenv on your "
                "system and install it if you don't have it:_\n```which "
                "virtualenv\npip install virtualenv```\n*Ngrok:*\n_Check "
                "to see if you have ngrok on your system:_\n```which ngrok"
                "```\n_Download Link:_\nhttps://bin.equinox.io/c/4VmDzA7iaHb"
                "/ngrok-stable-darwin-amd64.zip\n```unzip /path/to/ngrok.zip"
                "\ncd /usr/local/bin\nln -s /path/to/ngrok ngrok```",
                "footer": "Slack API: Build this Bot Workshop",
                "footer_icon": "https://platform.slack-edge.com/img/default"
                "_application_icon.png"
                }]
            }

        return json.dumps(message)
