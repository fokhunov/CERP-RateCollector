import base64
import json
import logging
import os
import zlib

import boto3

from src.fetcher import Fetcher
from src.parser import ParserKG
from src.parser import ParserKZ
from src.parser import ParserTJ
from src.parser import ParserUZ

# Supported countries
TJ = "tj"
UZ = "uz"
KG = "kg"
KZ = "kz"

# Env variables
SNS_TOPIC = os.environ.get('CERP_SNS_TOPIC')
COUNTRY = os.environ.get('CERP_COUNTRY')
LOG_LEVEL = os.environ.get('CERP_LOG_LEVEL')

# Logger client
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Parser client
parser = None

# SNS client
sns = boto3.client('sns')


# get_parser return new instance if not already exist (lambda runtime context).
def get_parser():
    if parser is not None:
        return parser

    if COUNTRY == TJ:
        return ParserTJ(logger, Fetcher())
    if COUNTRY == UZ:
        return ParserUZ(logger, Fetcher())
    if COUNTRY == KG:
        return ParserKG(logger, Fetcher())
    if COUNTRY == KZ:
        return ParserKZ(logger, Fetcher())

    return None


# compress_json compresses then encodes json.
def compress_json(j):
    return base64.b64encode(
        zlib.compress(
            json.dumps(j).encode('utf-8')
        )
    ).decode('ascii')


# lambda_handler entry point for AWS Lambda.
def lambda_handler(event, context):
    p = get_parser()
    if p is None:
        logger.error("no parser found for " + COUNTRY)
        return None

    # parse & compress result
    compressed_result = compress_json(p.parse_all())

    # publish a simple message to SNS topic
    sns.publish(
        TopicArn=SNS_TOPIC,
        Message=compressed_result,
    )

    return None


if __name__ == "__main__":
    #
    # for testing purpose
    #
    f = Fetcher()
    p = ParserTJ(logger, f)
    print(compress_json(p.parse_all()))
