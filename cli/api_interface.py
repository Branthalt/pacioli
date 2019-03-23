#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from authenticate import Settings
import requests


def post_transactions(settings, idtoken, transaction):
    url = "{}/transaction".format(settings.apigatewayurl)
    headers = {"Authorization": idtoken}
    response = requests.post(url, headers=headers, json=transaction)
    return response


if __name__ == "__main__":
    settings = Settings()
    # load token
    tokenfile = os.path.join(settings.key_dir, "idtoken")
    if os.path.isfile(tokenfile):
        with open(tokenfile, 'r') as f:
            idtoken = f.read()
    else:
        raise Exception("token file is missing")

    response = post_transactions(settings, idtoken)
    print(response.body)
