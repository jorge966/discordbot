import configparser

# Initialize
config = configparser.ConfigParser()
config.read('config/config.ini')

#
Bot_Token = config['Bot Info']['token']
