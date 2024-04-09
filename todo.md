# Shortcuts
> Works with int only for now

> to avoid encoding problems I made the /op/<op> take value in ''.

> Used sqlite3 db for quick implementation

> used flask webserver instead of a prod webserver

# TODO
api Side:
> Add error codes to spec

> Add check on the values in inputs

> complete the schemas


backend Side:
> use rpn library to interact with db using sqlalchemy

> put the operands as a column in db and use ids for requests to avoid encoding/decoding problems

> return proper error codes instead of 500 errors

> add error handlers
