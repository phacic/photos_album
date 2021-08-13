# photos_album

## Running
This is containerized with docker and has to be installed to run.

- **To run**

```shell
docker-compose up -d
```

The server will be exposed at `localhost:5333`

- **To run tests**

```shell
docker-compose run --rm web pytest
```

## known issues
- `photos/{id}/get_size/?size={image_size}` does not return the correct url for the image
