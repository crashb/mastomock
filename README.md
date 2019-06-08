# Dependencies

* Install [Python 3.6.x](https://www.python.org/downloads/release/python-366/).
* Get the Mastodon.py package: `pip3 install mastodon.py`
* Get the TensorFlow package: `pip3 install tensorflow`
* Get the TextGenRNN package: `pip3 install textgenrnn`

# Setup

You will need to create a file called `secrets.txt` in the `secrets` directory. It needs to look like this:
```
uc_client_id:     <your client id>
uc_client_secret: <your client secret>
uc_access_token:  <your access token>
```
A great guide on how to find these values can be found [here](https://gist.github.com/aparrish/661fca5ce7b4882a8c6823db12d42d26).

You also need to point the `config.txt` file at the Mastodon instance your bot is running from.

# Running

Do `python mastomock.py` from the main directory. The script will automatically listen for any mention notifications.

# Acknowledgements

* This bot is made by [me](https://mastodon.social/@crashb).
* I was able to re-use a big chunk of code from [Josef Kenny](https://mastodon.social/@jk)'s [User Count](https://github.com/josefkenny/usercount) bot.
