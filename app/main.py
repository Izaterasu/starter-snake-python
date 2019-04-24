import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response


state = dict()


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))
    global state
    state[data['you']['id']] = "right"
    
    color = "#00FF00"

    return start_response(color)

@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    '''s = data['board']['snakes']
    s_count = len(s)
    for snake in s:
        snakes[snake['id']] = snake
'''

    directions = ['up', 'down', 'left', 'right']
    body = data['you']['body']
    x = int(body[0]['x'])
    y = int(body[0]['y'])
    uuid = data['you']['id']
    
    global state
    direction = state[uuid]
    
    for i in range(1,100):
        appliedDir = 0
        
        if direction== 'left':
            appliedDir = x-1
        elif direction == 'right':
            appliedDir = x+1
        elif direction == 'up':
            appliedDir = y-1
        elif direction == 'down':
            appliedDir = y+1
            
        if appliedDir >= 0 and appliedDir < 15 and not -appliedDir:
            print("Move "+direction+" to: "+str(appliedDir))
            break
        
        direction = random.choice(directions)
    state[uuid] = direction
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
