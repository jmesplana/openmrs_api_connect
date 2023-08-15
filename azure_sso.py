# azure_sso.py

from requests_oauthlib import OAuth2Session

def authenticate_via_azure():
    # Azure app registration details
    client_id = 'YOUR_APP_CLIENT_ID'
    client_secret = 'YOUR_APP_CLIENT_SECRET'
    authorization_base_url = 'https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/authorize'
    token_url = 'https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token'
    redirect_uri = 'YOUR_REDIRECT_URI'  # This should match the one set in Azure AD

    # Step 1: User Authorization
    azure = OAuth2Session(client_id, redirect_uri=redirect_uri, scope="user.read")
    authorization_url, state = azure.authorization_url(authorization_base_url)
    print(f"Please go to the following URL and authorize the app: {authorization_url}")

    # Step 2: User redirects back to your app with a code
    redirect_response = input("Enter the full callback URL (from the address bar): ")
    token = azure.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

    # Return the authenticated session
    return azure
