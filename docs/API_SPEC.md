# MovieFlix CMS API Spec

This document supplements the provided README without modifying it.

## Auth
- POST /auth/signup: Create a new `User`
- POST /auth/login: Params `email`, `password`. Returns JWT.

## Health
- GET /health: Service status

## Users
- GET /users/{userid}: Get user (protected)
- DELETE /users/{userid}: Delete user (protected)

## Movies
- POST /movies/: Create movie (protected)
- GET /movies/{movieid}: Get movie
- DELETE /movies/{movieid}: Delete movie (protected)
- PATCH /movies/{movieid}: Partially update movie (admin-only). Supports toggling `published` and updating any provided fields.

## Likes
- POST /likes/: Like a movie (protected)
- GET /likes/user/{userid}: List likes for user (protected)
