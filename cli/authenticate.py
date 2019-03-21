#!/usr/bin/env python
import boto3
import configparser
import os

class Settings:

    def __init__(self, section='DEFAULT', configfile='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.file = configfile
        if not section in self.config:
            raise Exception("section {} does not exist in config.ini".format(section))
        self.section = section
        activeconfig = self.config[section]
        self.username = activeconfig.get('username')
        self.password = activeconfig.get('password')
        self.accountid = activeconfig.get('accountid')
        self.user_pool_id = activeconfig.get('user_pool_id')
        self.clientid = activeconfig.get('clientid')
        self.apigatewayurl = activeconfig.get('apigatewayurl')
        self.basepath = activeconfig.get('basepath', '.')
        self.key_dir = os.path.join(self.basepath, activeconfig.get('key_dir', 'keys'))

    def update_password(self, password):
        """
        Update the password in the in memory settings if it is set.
        Also updates the config file if a password is defined there. Only the password in the active section gets updated.

        parameters:
            password: the new password
        """
        assert type(password) is str
        if self.password:
            self.password = password
        if self.config[self.section].get('password'):
            self.config[self.section]['password'] = password
            with open(self.file, 'w') as f:
                self.config.write(f)



class Authenticator:

    def __init__(self, settings):
        self.settings = settings
        self.client = boto3.client('cognito-idp')
        self.challenge = None

    def initiate_auth(self):
        response = self.client.admin_initiate_auth(
            UserPoolId=self.settings.user_pool_id,
            ClientId=self.settings.clientid,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME':self.settings.username,
                'PASSWORD':self.settings.password
                }
            )
        if response.get('ChallengeName'):
            self.challenge = response
            raise self.ChallengeException

        return response

    def respond_to_auth_challenge(self, **kwargs):
        if not self.challenge:
            raise Exception("There is no challenge to respond to")
        if self.challenge['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            assert 'password' in kwargs, "password parameter is required"
            response = self.client.admin_respond_to_auth_challenge(
                UserPoolId=self.settings.user_pool_id,
                ClientId=self.settings.clientid,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ChallengeResponses={'NEW_PASSWORD':kwargs['password'], 'USERNAME':self.settings.username},
                Session=self.challenge['Session']
            )
            self.settings.password = password
        else:
            raise Exception("unknown challenge")
        return response

    class ChallengeException(Exception):
        pass

if __name__ == '__main__':
    import getpass

    settings = Settings()
    authenticator = Authenticator(settings)
    try:
        response = authenticator.initiate_auth()
    except Authenticator.ChallengeException:
        print("Your password has to be renewed, please provide a new password")
        while True:
            password = getpass.getpass()
            check = getpass.getpass(prompt="Password again")
            if password == check:
                break
            else:
                print("The two passwords do not match, please try again")
        response = authenticator.respond_to_auth_challenge(password=password)
        settings.update_password(password)
    
    # Write keys to disk
    with open(os.path.join(settings.key_dir, 'accesstoken'), 'w') as f:
        f.write(response['AuthenticationResult']['AccessToken'])
    with open(os.path.join(settings.key_dir, 'refreshtoken'), 'w') as f:
        f.write(response['AuthenticationResult']['RefreshToken'])
    with open(os.path.join(settings.key_dir, 'idtoken'), 'w') as f:
        f.write(response['AuthenticationResult']['IdToken'])

