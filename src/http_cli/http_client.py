"""HTTP client implementation for making HTTP requests."""

import requests

from http_cli.exceptions import HTTPClientError, HTTPConnectionError, ResponseError


class HTTPClient:
    """HTTP client for making HTTP requests."""

    def __init__(self, timeout=30):
        self.timeout = timeout
        self.allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    def make_request(self, method, url, **kwargs):
        """Make an HTTP request."""
        if method.upper() not in self.allowed_methods:
            raise ValueError(
                f"Unsupported HTTP method. Allowed methods: {', '.join(self.allowed_methods)}"
            )

        try:
            response = requests.request(
                method=method, url=url, timeout=self.timeout, **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as e:
            raise HTTPConnectionError(f"Failed to connect to {url}: {str(e)}") from e
        except requests.exceptions.HTTPError as e:
            raise ResponseError(f"HTTP error occurred: {str(e)}") from e
        except requests.exceptions.RequestException as e:
            raise HTTPClientError(f"Request failed: {str(e)}") from e

    def get(self, url, **kwargs):
        """Make a GET request."""
        return self.make_request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        """Make a POST request."""
        return self.make_request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        """Make a PUT request."""
        return self.make_request("PUT", url, **kwargs)

    def patch(self, url, **kwargs):
        """Make a PATCH request."""
        return self.make_request("PATCH", url, **kwargs)

    def delete(self, url, **kwargs):
        """Make a DELETE request."""
        return self.make_request("DELETE", url, **kwargs)
