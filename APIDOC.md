
# OPENSKY-ST-API Doc
This API documentation lists all the endpoints and their workings.

# GET
- `planedata`

## `planedata` (`tail`) -> plane history
THis endpoint provides the plane history with the supplied tail

On success, the `payload` field contains the array of plane entries.

On failure, the `payload` field contains the error message.

# POST

- `auth`
- `checkauth`
- `logoff`
- `createuser`

## `auth` (`user`, `pass`) -> `authkey`
This endpoint authenticates the user with the provided username (`user`) and  password (`pass`).

On success, the `payload` field contains the authkey (`authkey`) needed for requests with elevated privileges.

On failure, the `payload` field contains the error message.

## `checkauth` (`authkey`)
This endpoint checks if the supplied authkey (`authkey`) is still valid and can be used to perform requests with elevated privileges.

On success, the `response_code` field is `200` and the authkey is valid.

On failure, the `response_code` field is equivalent to AUTH_FAILURE. The authkey is invalid and can not be used anymore.

## `logoff` (`authkey`)
This endpoint ends the authentification of the supplied authkey (`authkey`), revoking the permission for requests with elevated privileges.

On success, the `response_code` field is `200` and the authkey is now disabled.

On failure, the `payload` field contains the error message.

## `createuser` (`user`, `pass`)
This endpoint creates a new user with the supplied username (`user`) and password (`pass`).

**Note**
> The user is NOT logged in automatically, authentication needs to be done using the `auth` POST-endpoint!
> Duplicate usernames are not allowed!

On success, the `response_code` field is `200` and the new user can now log in.

On failure, the `payload` field contains the error message.

## `changepass` (`authkey`, `pass`)
Changes the password for the user owning the supplied authkey

**Note**
> The user does not get logged out automatically!

On success, the `response_code` field is `200` and the new user can now log in.

On failure, the `payload` field contains the error message.
