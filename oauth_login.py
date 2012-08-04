# Adapted from github.com/Khan/khan-api

import cgi
import SimpleHTTPServer
import SocketServer

import oauth


def get_request_token(client):
    token_array = [None]

    def create_callback_server():
        class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
            def do_GET(self):
                params = cgi.parse_qs(
                    self.path.split('?', 1)[1], keep_blank_values=False)
                request_token = oauth.OAuthToken(
                    params['oauth_token'][0], params['oauth_token_secret'][0])
                request_token.set_verifier(params['oauth_verifier'][0])
                token_array[0] = request_token

                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(
                    'OAuth request token fetched; you can close this window.')

            def log_request(self, code='-', size='-'):
                pass

        server = SocketServer.TCPServer(('127.0.0.1', 0), CallbackHandler)
        return server

    server = create_callback_server()
    client.start_fetch_request_token(
        'http://127.0.0.1:%d/' % server.server_address[1])
    server.handle_request()
    server.server_close()

    return token_array[0]


def get_access_token(client):
    return client.fetch_access_token(get_request_token(client))
