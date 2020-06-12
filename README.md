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

## Config
  * `.env`


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
