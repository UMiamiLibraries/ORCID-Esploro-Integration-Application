# CI/CD

## Development

`docker build -f Dockerfile.local --no-cache -t cgb37/local-e-orcid:1.0.0 .`

`docker push cgb37/local-e-orcid:1.0.0`

## Staging

`docker build -f Dockerfile.staging --no-cache -t devumlacr.azurecr.io/staging-e-orcid:1.0.0 .`

`docker push devumlacr.azurecr.io/staging-e-orcid:1.0.0`

## Production

`docker build -f Dockerfile.prod --no-cache -t umlacr.azurecr.io/prod-e-uml-orcid:1.0.0 .`

`docker push umlacr.azurecr.io/prod-e-uml-orcid:1.0.0`