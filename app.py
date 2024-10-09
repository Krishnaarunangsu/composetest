import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379)

def get_hit_count():
    """Get The hit count from redis

    Raises:
        exc: _description_

    Returns:
        _type_: _description_
    """
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    """_summary_

    Returns:
        _type_: _description_
    """
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\n'
    #return f'Hello World! I have been seen 2 times.\n'

if __name__ == "__main__":
    app.run(debug=True)