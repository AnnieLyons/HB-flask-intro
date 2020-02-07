"""Greeting Flask app."""

from flask import Flask, request

# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)

AWESOMENESS = [
    'awesome', 'terrific', 'fantastic', 'neato', 'fantabulous', 'wowza',
    'oh-so-not-meh', 'brilliant', 'ducky', 'coolio', 'incredible',
    'wonderful', 'smashing', 'lovely']

MEANNESS = [
    'stinky', 'warty', 'lame', 'covered in boils', 'a CLOWN',
    'blander than oatmeal', 'the absolute worst', 'an utter fool',
    'the least stealthy ninja ever']


@app.route('/')
def start_here():
    """Home page."""

    return """
    <!doctype html>
    <html>
      <head>
        <title>Start Here</title>
      </head>
      <body>
        <a href="/hello">Take me to the start</a>
      </body>
    </html>
    """


@app.route('/hello')
def say_hello():
    """Say hello and prompt for compliments."""

    return """
    <!doctype html>
    <html>
      <head>
        <title>Hi There!</title>
      </head>
      <body>
        <h1>Hi There!</h1>
        <form action='/process-hello'>
          Would you rather be complimented or insulted? <br>
          <input type="radio" name="niceormean" value="nice">A compliment, please! <br>
          <input type="radio" name="niceormean" value="mean">I'll take an insult. CLOWN. <br>
          <input type="submit">
        </form>
      </body>
    </html>
    """


@app.route('/process-hello')
def process_hello():
    """Decide whether to send the user to choose insults or compliments."""

    nice_or_mean = request.args.get("niceormean")

    if nice_or_mean == "mean":
        levels_form = """
        <!doctype html>
        <html>
          <head>
            <title>Insult Level</title>
          </head>
          <body>
            <h2>Choose Your Insult Level:</h2>
            <form action="/select/insult">
              <select name="level">
                <option value="1">Only a little bit.</option>
                <option value="2">I'd like my insult to be medium-meanness.</option>
                <option value="3">Do your worst!</option>
              </select>
              <br>
              <input type="submit">
            </form>
          </body>
        </html>
        """

    elif nice_or_mean == "nice":
        levels_form = """
        <!doctype html>
        <html>
          <head>
            <title>Compliment Level</title>
          </head>
          <body>
            <h2>Choose Your Compliment Level:</h2>
            <form action="/select/compliment">
              <select name="level">
                <option value="1">Just say something nice.</option>
                <option value="2">I'd like a middle-of-the-road compliment.</option>
                <option value="3">Say something really flattering!</option>
              </select>
              <br>
              <input type="submit">
            </form>
          </body>
        </html>
        """

    return levels_form


@app.route('/select/insult')
def display_insult_form():
    """Let the user choose their insult level."""

    level = int(request.args.get("level"))

    # Generate HTML options, so we don't have to create each one by hand. (You
    # could also write a helper function and call it.)

    option_template = '<option value="{insult}">{insult}</option>'
    if level == 1:
        option_elements = [
            option_template.format(insult=insult) for insult in MEANNESS[:3]
        ]

    elif level == 2:
        option_elements = [
            option_template.format(insult=insult) for insult in MEANNESS[3:6]
        ]

    else:
        option_elements = [
            option_template.insult(insult=insult) for insult in MEANNESS[6:]
        ]

    return """
    <!doctype html>
    <html>
      <head>
        <title>Choose Insult</title>
      </head>
      <body>
        <h1>Oh. It's You.</h1>

        <h3>Fill out this dinky form and choose something rude.</h3>
        
        <form action="/diss">
          What's your name? <input type="text" name="person">
          Choose an insult:
          <select name="insult">
            {}
          </select>
          <input type="submit" value="Take Me to My Insult!">
        </form>

      </body>
    </html>
    """.format(option_elements)


@app.route('/select/compliment')
def display_compliment_form():
    """Let the user choose a compliment level."""

    level = int(request.args.get("level"))

    # Generate HTML options, so we don't have to create each one by hand. (You
    # could also write a helper function and call it.)

    option_template = '<option value="{comp}">{comp}</option>'
    if level == 1:
        option_elements = [
            option_template.format(comp=comp) for comp in AWESOMENESS[:3]
        ]

    elif level == 2:
        option_elements = [
            option_template.format(comp=comp) for comp in AWESOMENESS[3:6]
        ]

    else:
        option_elements = [
            option_template.format(comp=comp) for comp in AWESOMENESS[6:]
        ]

    return """
    <!doctype html>
    <html>
      <head>
        <title>Choose Compliment</title>
      </head>
      <body>
        <h1>Hooray, It's You!</h1>

        <h3>Fill out this lil form and choose your compliment. :)</h3>
        
        <form action="/greet">
          What's your name? <input type="text" name="person">
          Choose a compliment:
          <select name="compliment">
            {}
          </select>
          <input type="submit" value="Take Me to My Compliment!">
        </form>

      </body>
    </html>
    """.format(option_elements)


@app.route('/greet')
def greet_person():
    """Get user by name, get compliment, and say something nice."""

    player = request.args.get("person")
    compliment = request.args.get("compliment")

    return f"""
    <!doctype html>
    <html>
      <head>
        <title>A Compliment</title>
      </head>
      <body>
        Hi, {player}! I think you're {compliment}!
      </body>
    </html>
    """


@app.route('/diss')
def diss_person():
    """Get user by name, get insult, and mock according to insult level."""

    player = request.args.get("person")
    insult = request.args.get("insult")

    return f"""
    <!doctype html>
    <html>
      <head>
        <title>Oh. It's You.</title>
      </head>
      <body>
        <p>
          Hi, {player}! I think you're {insult}!
        </p>
      </body>
    </html>
    """


if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads"
    # our web app if we change the code.
    app.run(debug=True, host="0.0.0.0")
