# Authorization Scheme
In order to have the user approve your app for access to user private
spotify data the app must be verified.

* App Authorization - Spotify authorizes your app to acces the spotify
  platform(Apis, SDKS, etc)
* User Authorization - grant your app persmission to acces the users own data.

# Getting Authorization
There are three parties
* Server: The spotify server
* Client: the application
* Resource: The end user data and controls

#Scopes
Allows your application to access specific API endpoints on behalf of the user.

## Example
This code generates a reques for the scopes user-read-private and
user-read-email.

	var.scopes = 'user-read-private user-read-email';
	res.redirect('https://accounts.spotify.com/authorize' +
	  '?response_type=code' +
	  '&client_id=' + my_client_id +
	(scopes ? '&scope=' + encodeURIComponent(scopes) : '') +
	'&redirect_uri=' encodeURIComponent(redirect_uri));

and so on.


# Authorization Flows

## Authorization Code
This flow is suitable for long running apps in wich permission is only grandted
once. The accesss token can then be refreshed. This however involves sending a
secret key so make sure that it is secure

You do: Promput user to  a webpage where they can choose to grant you access to
their data.

You get: An **access token** and a **refresh token**

you use the refresh tokens to extend the validity of the access token.
## Authorization Code with PKCE

## Client Credintials

## Implicit Grant


