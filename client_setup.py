# -*- coding: utf-8 -*-
"""
Set up a client using stravalib
"""
import json
import os
import pandas as pd
import webbrowser
import time
from stravalib.client import Client

def inititalise_stravalib_client():
    client_details_filename = 'client_details.json'
    access_token_filename = 'access_token.json'
    
    client = Client()
    
    access_token_does_exist = os.path.isfile(access_token_filename)
    access_token_doesnt_exist = not(access_token_does_exist)
    access_token_expired = True
    
    if access_token_does_exist:
         with open(access_token_filename, 'r') as f:
            token_response = json.load(f)
            token_response = json.loads(token_response)      
            token_expiry_time = token_response['expires_at']
            current_time = time.time()
            access_token_expired = current_time > token_expiry_time
        
    if access_token_doesnt_exist or access_token_expired:
        # Check if I have client details in a json:
        if os.path.isfile(client_details_filename):
            with open(client_details_filename, 'r') as f:
                client_details = json.load(f)
                client_details = json.loads(client_details)
        else:
            client_id = str(input('Enter your client ID: '))
            client_secret = str(input('Enter your client secret: '))
            client_details = {'client_id': client_id,
                              'client_secret': client_secret}
            # Save client details to file
            client_details_string = json.dumps(client_details)
            with open(client_details_filename, 'w+') as f:
                json.dump(client_details_string, f)
        
        # Read client details from file:
        with open(client_details_filename, 'r') as f:
            client_details = json.load(f)
            client_details = json.loads(client_details)
              
        client_id = client_details['client_id']
        client_secret = client_details['client_secret']
        scope = ['read', 'read_all', 'profile:read_all', 'profile:write', 'activity:read', 'activity:read_all', 'activity:write']
        authorize_url = client.authorization_url(client_id=client_id, redirect_uri='http://localhost:5000/authorized', scope=scope)
        
        # Open the authorization url
        print('Opening: ' + authorize_url)
        webbrowser.open(authorize_url)
        
        # Get code
        entered_code = str(input('Please enter code: '))
        
        # Exchange code for token:
        token_response = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=entered_code)
        # Save it to file so we can use it until it expires.
        access_token_string = json.dumps(token_response)
        with open(access_token_filename, 'w+') as f:
            json.dump(access_token_string, f)
    
    # Now we have a token_response dict either from file or from the
    # Strava API
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
       
    # Provide the access token and refresh token to the client:
    client.access_token = access_token
    client.refresh_token = refresh_token

    return client


if __name__ == '__main__':
    client = inititalise_stravalib_client()
    
 