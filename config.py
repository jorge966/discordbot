import configparser

# Initialize
config = configparser.ConfigParser()
config.read('config/config.ini')

#Bot info

Bot_username = config['Bot Info']['username']
Bot_Token = config['Bot Info']['token']
ownerId = config['Bot Info']['ownerId']
App_ID = config['App Info']['ID']
App_Secret = config['App Info']['secret']
twitch_client = config['Credentials']['client_id']

