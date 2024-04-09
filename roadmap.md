# Roadmap

db:
> Add status to stack to keep track of history: instead of deleting change status to deleted
> Add a request table to keep track of calls
api:
> use request to apply operands to stacks
> add other operators
> add a dockerfile to use api in a docker container
> use a prod webserver like gunicorn
> improve error gestion, instead of returning 500 errors we should return specific error codes