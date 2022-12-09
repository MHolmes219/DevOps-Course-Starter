# DevOps Apprenticeship: Project Exercise

[![.github/workflows/exercise7-pipeline.yaml](https://github.com/MHolmes219/DevOps-Course-Starter/actions/workflows/exercise7-pipeline.yaml/badge.svg)](https://github.com/MHolmes219/DevOps-Course-Starter/actions/workflows/exercise7-pipeline.yaml)

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

## Trello pre-steps
* Setup a new Trello account if you don't have one already.
* Visit https://trello.com/app-key to generate a new api key.
* Once done, you will need to take that key and add in to your .env file in the API_KEY value.
* Click the Token link on the page where you generated your new API key in order to generate an access token. Add this value as the API_TOKEN in your .env file.
* Visit your trello board and add `.json` to the end of the URL to view the board in json. Take the very top `id` value and add that to your .env file in the BOARD_ID value.

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running tests

Pytest is added as part of the poetry toml dependencies, allowing you to then run `poetry install` and use within the virtual environment as a dev dependency. You can then run all of your tests in your terminal, with optional verbosity to check output:
```bash
pytest tests -vv
```
You can also run individual tests by specifying the test name, like so:
```bash
pytest tests/test_view_model.py -k 'test_return_to_do_items'
```

If you're in VSCode, you can also install Test Explorer which will allow you to find relevant tests and provide you output & debug mode to adding in breakpoints for testing steps of your methods.


# Build & run Docker

1. Development
`docker build --target development --platform linux/amd64 --tag todo-app:dev .`
`docker run --env-file ./.env -p 5001:5000 -v "$(pwd)"/todo_app:/app/todo_app todo-app:dev`

Or using docker-compose:
`docker-compose build`
`docker-compose up`

2. Production
`docker build --target production --platform linux/amd64 --tag todo-app:prod .`
`docker run --env-file ./.env -p 5001:5000 -v $(pwd)/var/log:/var/log todo-app:prod`

3. Testing
`docker build --target test --platform linux/amd64 --tag todo-app:test .`
`docker run --env-file ./.env.test todo-app:test`

Confirm the app is running by either curling the url from the terminal:
`curl 127.0.0.1:5001`
or by visiting the url in your browser.


# Documentation

## PlantUML

This can be used to document various diagrams, such as sequence diagrams, class diagrams, object diagrams and component diagrams. In this case, the diagram is to document a sequence.

```
@startuml
title ToDo App with Trello

User -> Browser : request
Browser -> Docker : request
Docker -> Flask : request
Flask -> Trello : request
Flask <- Trello : response
Docker <- Flask : response
Browser <- Docker : response
User <- Browser : response
@enduml
```

PlantUML files always declare a `@startuml` and `@enduml` to define the declarations for the diagram.

It's possible to use either `-->` or `->` to define an arrow. The double dash represents a dotted line, where as the single dash represents a solid line. `->` represents a "request" sequence, where as `<-` represents a response sequence.

The list and sequence of lines defines the order of which the entries will display, unless the order keyword is defined, like so:

```
participant Last 30
participant Middle 20
participant First 10
```

It's possible to make adjustments to arrows and colours of boxes, or arrows, to make the diagram more readable.

This can be done like so:

```
Alice -[#red]-> Bob : ok
```

It's possible to group messaging to suggest containerisation or nested elements.

```
@startuml
Alice -> Bob: Authentication Request
alt successful case
    Bob -> Alice: Authentication Accepted
else some kind of failure
    Bob -> Alice: Authentication Failure
    group My own label
    Alice -> Log : Log attack start
        loop 1000 times
            Alice -> Bob: DNS Attack
        end
    Alice -> Log : Log attack end
    end
else Another type of failure
   Bob -> Alice: Please repeat
end @enduml
```

You can add notes to add further explanation of steps within your diagram:

```
@startuml
Alice->Bob : hello
note left: this is a first note
Bob->Alice : ok
note right: this is another note
Bob->Bob : I am thinking
note left
a note
can also be defined
on several lines
end note
@enduml
```

For further guides and syntax, check out the official plantuml guide: https://plantuml.com/guide


### Logging with loggly
Sign up to loggly and find the icon for Logs. Under this select "Source Setup", then select Customer Tokens to create a new token.
Add your `LOGGLY_TOKEN` variable to your .env file and add in your loggly token that you've generated.

You can also update the `LOG_LEVEL` of the application and output specific logs, such as DEBUG, INFO, ERROR, WARNING, etc.

### Terraform plan and deployment
#### Create a plan and apply that plan by running the following

```
terraform plan -var "arm_tenant_id=<tenant_id>" -var "arm_subscription_id=<subscription_id>" -var "arm_client_id=<client_id>" -var "arm_client_secret=<arm_secret>" -var "client_id=<client_id>" -var "client_secret=<client_secret>" -var "secret_key=<secret_key>" -out terraform.tfplan
terraform apply "terraform.tfplan"
```

### Terraform destroy
#### Destroy the infrastructure by running the following
```
terraform destroy -var "client_id=<ID>" -var "client_secret=<SECRET>" -var "secret_key=<SECRET_KEY"
```

### Run in minikube
1. Start minikube by running `minikube start`
2. Run the docker build for prod from the instructions above
3. Run `minikube image load todo-app:prod`
4. `kubectl apply -f deployment.yaml`
5. `kubectl apply -f service-yaml`
6. `kubectl port-forward service/module-14 7080:5000`
7. Open http://localhost:7080 in your browser.