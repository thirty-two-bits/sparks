export DEFAULT_WSGI="sparks.wsgi"
export WSGI_PATH="${WSGI_PATH:-$DEFAULT_WSGI}"
gunicorn $WSGI_PATH --log-file -

