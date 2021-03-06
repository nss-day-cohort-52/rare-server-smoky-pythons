import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from views import (add_comment, create_post, create_tag, create_user, delete_comment, find_tag, get_all_comments, get_all_post_tags, get_all_posts, get_all_tags, get_all_users,
                   get_single_category, get_single_comment,
                   get_single_tag, get_single_user, login_user, update_post, create_category, find_category,
                   get_all_categories, delete_post,
                   get_posts_by_category, get_posts_by_user,
                   get_single_post, get_all_subscriptions, create_subscription, delete_subscription, get_users_subscriptions)


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""

        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url()

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            if resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"
            if resource == 'posts':
                if id:
                    response = get_single_post(id)
                else:
                    response = get_all_posts()
            if resource == 'comments':
                if id:
                    response = get_single_comment(id)
                else:
                    response = get_all_comments()
            if resource == 'users':
                if id:
                    response = get_single_user(id)
                else:
                    response = get_all_users()
            if resource == 'posttags':
                response = get_all_post_tags()

            if resource == 'subscriptions':
                if id:
                    response = get_users_subscriptions(id)
                else:
                    response = get_all_subscriptions()

        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "label" and resource == "categories":
                response = find_category(value)
            if key == "label" and resource == "tags":
                response = find_tag(value)
            if key == "user_id" and resource == "posts":
                response = get_posts_by_user(value)
            if key == "category_id" and resource == "posts":
                response = get_posts_by_category(value)

        self.wfile.write(response.encode())

    def do_POST(self):
        """Makes a POST request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == 'tags':
            response = create_tag(post_body)
        if resource == 'comments':
            response = add_comment(post_body)
        if resource == 'posts':
            response = create_post(post_body)
        if resource == 'subscriptions':
            response = create_subscription(post_body)
        self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        success = False

        resource, id = self.parse_url()

        if resource == 'posts':
            success = update_post(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

    def do_DELETE(self):
        """Handles DELETE Requests"""
        self._set_headers(204)
        (resource, id) = self.parse_url()
        if resource == "posts":
            delete_post(id)
        if resource == 'subscriptions':
            delete_subscription(id)
        if resource == "comments":
            delete_comment(id)


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
