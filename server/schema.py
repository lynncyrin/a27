"""
schema.py contains all of the input and output schemas for our server

The schemas are all defined with marshmallow, which you can read about here
=> https://marshmallow.readthedocs.io/

🚨 Changing the keys on the schemas will change the inputs and outputs for our server.
🚨 So before you change the keys, please check that all of our clients are updated!

The schemas are tested by writing tests for the controllers. We could instead choose to
test the schemas directly, if they controller tests (and their database calls) become
too heavy.

TODO - pipe all of these into autogenerated OpenAPI v3 definitions.
"""

from typing import List

from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate
from marshmallow.validate import Range


# VALID_ROLES is my assumption that we want the backend to validate the list of
# available roles. I built a system similar to this @ Textio, and there we used
# a list just like this to validate the role input.
VALID_ROLES = [
    "standard",
    "admin",
]


def role_must_be_valid(role: str):
    if role not in VALID_ROLES:
        raise ValidationError(f"role {role} was not a valid role")


def roles_must_be_valid(roles: List[str]):
    for role in roles:
        role_must_be_valid(role)


# disable "too few public methods" warning, the schemas inherit public methods from their base class
# pylint: disable=R0903


class BaseUserPostSchema(Schema):
    """
    BaseUserPostSchema represents the schema that clients input into our server, or
    recieve as output from our server.
    So for example, it is the schema that you should respect when `POST`ing the server.

    When used as input, it looks like so:
    {
        "email": "lynncyrin@gmail.com",
        "role": "admin",
        ...
    }

    When used as output, it looks like so:
    {
        "id": 1234, # <== newly added
        "email": "lynncyrin@gmail.com",
        "role": "admin",
        ...
    }

    This is a "base" schema, and is expanded via
        - UserPostCreateSchema (runs on create)
        - UserPostUpdateSchema (runs on update)
    """

    ################################
    # fields altered in subclasses #
    ################################

    email = fields.Email(required=False)
    role = fields.Str(required=False)

    ###################
    # optional fields #
    ###################

    # I'm assuming that given the problem space (politics) and the reccommendations
    # here => https://www.w3.org/International/questions/qa-personal-names
    # that it is a good decision to avoid trying to limit the lengths of peoples
    # name inputs.
    #
    # That said, our database has limits so we want to avoid people accidentally
    # copy pasting the entire text of The Illiad into the 1st name field,
    # since that would simply bring down the database.
    #
    # So the max length you see here isn't an attempt at guessing at the max length
    # of someones name, it is a protective measure to unsure that postgres can
    # actually store the data.
    #
    # 10000 seems like more than enough characters for a name, I think!!!
    # 1000 would probably also be fine.

    familyName = fields.Str(validate=validate.Length(max=10000))
    givenName = fields.Str(validate=validate.Length(max=10000))

    smsUser = fields.Boolean(default=False, missing=False)

    ######################
    # output only fields #
    ######################

    id = fields.Integer(
        validate=[Range(min=0, error="must not be negative")], dump_only=True
    )

    class Meta:
        unknown = EXCLUDE


class UserPostCreateSchema(BaseUserPostSchema):
    """
    UserPostCreateSchema is the "user create schema" for when you create a user, eg.

        $ http POST /users

    It is distinct from the "user update schema" due to certain fields being
    required upon user creation - which is an assumption I'm making about the problem
    space!

    This schema inheritence thing is Complex ™️ so ideally I would spend a few
    beats working on making it easier to understand.
    """

    # NOTE! I'm assuming here that we don't want users with duplicate emails.
    #
    # In a work environment, I would check in with the person who is creating
    # requirements to see if that is an accurate assumption.
    email = fields.Email(required=True)
    role = fields.Str(required=True, validate=role_must_be_valid)

    class Meta:
        unknown = EXCLUDE


class UserPostUpdateSchema(BaseUserPostSchema):
    """
    UserPostUpdateSchema is the "user update schema" for when you update a user, eg.

        $ http PUT /users/1

    It is distinct from the "user create schema" due to all fields being optional.
    """

    # this is actually identical to the base schema
    # but its still useful to add these here, for the sake of clarity
    email = fields.Email(required=False)
    role = fields.Str(required=False, validate=role_must_be_valid)

    class Meta:
        unknown = EXCLUDE


class UserPathParamSchema(Schema):
    """
    UserPathParamSchema represents the path parameter schema to use when making GET requests
    for our users endpoints.

    For example, given the request...
    GET /users/5000
               ^
               the schema defines the data input here
    """

    user_id = fields.Integer(
        required=True, validate=[Range(min=0, error="must not be negative")]
    )

    class Meta:
        unknown = EXCLUDE


class UserQueryParamSchema(Schema):
    """
    UserQueryParamSchema represents the query string schema to use when making GET requests
    for our users endpoints.

    For example, given the request...
    GET /users?page=20&limit=10
              ^
              the schema defines the data from this point, and on.
    """

    # WRT both `default` and `missing` being present here, see
    #  => https://github.com/marshmallow-code/marshmallow/issues/775
    page = fields.Integer(
        default=1, missing=1, validate=[Range(min=0, error="must not be negative")]
    )
    limit = fields.Integer(
        default=50,
        missing=50,
        # 1000 is my napkin math estimate for the a number that will prevent the server
        # overloading the database with massive GET requests
        validate=[
            Range(max=1000, error="limit must be less than 1000"),
            Range(min=0, error="must not be negative"),
        ],
    )
    roles = fields.List(
        fields.String, default=[], missing=[], validate=roles_must_be_valid
    )
    sort_by = fields.String(
        default="", missing=""
    )  # validate that its actually a column name
    order = fields.String(
        default="desc", missing="desc"
    )  # validate that its "desc" "asc"

    # {
    #   nextUrl: "GET /users?page=2020-01-01-TZUS&limit=2020-02-01-TZUS"
    # }
    nextUrl = fields.String()

    class Meta:
        unknown = EXCLUDE
