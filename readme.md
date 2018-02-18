# Scan Cat: a website scanning and diagnostic tool

Scan Cat retrieves public information about websites faster than humans can. It's available at https://www.scancat.io.

Scan Cat lets support teams and developers grab facts and guesstimates to help with troubleshooting, returning information such as:

- What version of WordPress is installed?
- Which Genesis child theme is active? What version?
- Which version of Genesis is installed?
- Is the site behind a maintenance mode page?
- Has the site experienced a silent fatal error? (Finds missing `</html>` tags).
- Which popular plugins seem active?
- Is Yoast SEO in use?
- Are common caching plugins active?
- Which host do A records currently point to?
- Is Cloudflare in use?
- Are mail records set up for the domain?

## Features
You can pass a URL to Scan Cat with the url param:
https://www.scancat.io/?url=example.com

## Limitations
Scan Cat is currently optimised for WordPress sites and StudioPress themes and plugins. Other platform and theme support is planned.

## To run locally
Use the [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):

1. Do `pipenv install`.
2. Do `pipenv shell`.
3. Run `heroku local`.
4. Visit http://127.0.0.1:5000.


## To deploy to Heroku
1. `heroku create`
2. `git push heroku master`
3. `heroku config:set PRODUCTION=true`
4. `heroku open`

## To update Heroku
1. Make changes.
2. `git push heroku master`.

## Credits
Cat illustrations by Denis Sazhin ([Ikonka.com](http://iconka.com/en/)).
Commercial licenses available from http://iconka.com/en/licensing/.

The site is programmed in <a href="https://www.python.org/">Python</a> with <a href="http://flask.pocoo.org/">Flask</a>, <a href="https://github.com/kennethreitz/flask-sockets">Flask-Sockets</a>, and <a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>. It’s hosted with <a href="https://www.heroku.com/">Heroku</a>.
