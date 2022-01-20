# CERP-RateCollector

RateCollector - is one of the Currency Exchange Rate Platform (CERP) services which collects data from websites or API endpoints.

## AWS setup
1. Install/Setup [SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
2. Setup [AWS credentials](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html)

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

e.g:
make deploy c=tj e=prod v=2.4.0 ll=ERROR
```