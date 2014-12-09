from httmock import response


def create_mock_response(body, status=200, content_type='application/xml', extra_headers=None):
    headers = {
        'Content-Type': content_type,
    }

    if extra_headers:
        headers.update(extra_headers)

    return response(status, body, headers)
