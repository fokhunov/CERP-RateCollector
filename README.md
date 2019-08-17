# CERP-RateCollector

RateCollector - is one of the Currency Exchange Rate Platform (CERP) services which collects data from websites or API endpoints.

## Deployment

```
Available countries:
- tj
- uz
- kg
- kz
```

```
Available environments:
- prod
```

```
Available log levels:
- DEBUG
- INFO
- ERROR
```

Run following command to deploy AWS Lambda app:
```
make deploy c=<country> e=<env> v=<version> ll=<log_level>
```