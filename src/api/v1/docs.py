from src.schemas.utils import ErrorResponse


tags_metadata = [
    {
        "name": "Health",
        "description": "Health endpoints are used for checking the status of the service",
    },
    {
        "name": "Auth",
        "description": "This set of endpoints handles everything that has to do with authentication / authorization.",
    },
    {
        "name": "Users",
        "description": "This set of endpoints handles the users of the app.",
    },
    {
        "name": "Models",
        "description": "This set of endpoints handles the models that a user creates.",
    },
    {
        "name": "Datasets",
        "description": "This set of endpoints handles a the user's datasets.",
    },
    {
        "name": "Dataset Rows",
        "description": "This set of endpoints handles a dataset's rows.",
    },
    {
        "name": "Inferences",
        "description": "This set of endpoints handles a model's inferences.",
    },
    {
        "name": "Performance Metrics",
        "description": "This set of endpoints handles a model's performance metrics.",
    },
    {
        "name": "Drifting Metrics",
        "description": "This set of endpoints handles a model's drifting metrics.",
    },
    {
        "name": "Model Integrity Metrics",
        "description": "This set of endpoints handles a model's integrity metrics.",
    },
]


bad_request: ErrorResponse = {
    "title": "BadRequest",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

validation_error: ErrorResponse = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

authorization_error: ErrorResponse = {
    "title": "AuthorizationError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

not_found_error: ErrorResponse = {
    "title": "NotFoundError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

conflict_error: ErrorResponse = {
    "title": "ConflictError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

conflict_error: ErrorResponse = {
    "title": "ConflictError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

content_gone: ErrorResponse = {
    "title": "ContentGone",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}