# App-python-shorten-url


## Set up the Services
 * make up


## Swagger:
  * `http://${host_name}:8080/apidocs/`

## Debuging:
  * Start the flask debug server (auto reload)
    * `make flask_dev`

  * Connect to Mysql
    * `make mysql`

  * Connect to Redis
    * `make redis`

## Configs
  * see configs/dev.env

## Redirect
  * `http:{host_name}:8080/shorten_url/v1/{url_id}`


## Design
  * Flow:
    * Route -> Controller -> UseCase -> Model

  * Controllers:

  * Models:
    * Entity
    * Entitry Repository

  * Storages:
    * Implement the Entitry Repository

  * Use Cases:
    * One Usecase may consist of multiple Entitry Repositories


## Analysis:
  * The Indexed Web contains at least 5.49 billion pages (Saturday, 13 June, 2020).
    * which is greaterh than 2^32 (4 billion)
    * 64 bits integer is enough.

  * How to display the 64 bits unique id in the web??
    * Base62 is a common method.
      * charset [a-z A-Z 0-9]
    * max lenth of the unique id
      * `math.log(2**64-1, 62)` = 10.7 (at most 11 characters)


  * Ref:
    * https://www.worldwidewebsize.com/
    * http://cn.soulmachine.me/2017-04-10-how-to-design-tinyurl/


## Setup Editor env
  ```shell
  pyenv version 3.8.5
  pipenv shell
  pip install -r requirements.txt
  ```

## How to get a unique id
  * Ref:
    * https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c
