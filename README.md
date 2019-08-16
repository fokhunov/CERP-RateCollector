# CERP-RateCollector

RateCollector - is one of the Currency Exchange Rate Platform (CERP) services which collects data from websites or API endpoints.


## Deployment

```
make deploy c=tj e=staging v=v1.0.0 ll=ERROR
```

#### Available countries:
- tj
- uz
- kg
- kz

#### Available environments:
- staging
- prod

#### Available log levels:
- DEBUG
- INFO
- ERROR

## Todo:
* minify deployment artifacts size (currently about 10mb)