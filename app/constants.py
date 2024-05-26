class secretkeys:
    def __init__(self):
        self.client_id = 'REDACTED',
        self.client_secret = 'REDACTED',
        self.redirect_uri = 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl'
        self.environment = 'production'
        self.realm_id = 'REDACTED'
        self.refresh_token = 'REDACTED'
        self.access_token = 'REDACTED'

    def set_access_token(self, access_token):
        self.access_token = access_token

    def get_access_token(self):
        return self.access_token

    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token

    def get_refresh_token(self):
        return self.refresh_token

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

secretKeys = secretkeys()