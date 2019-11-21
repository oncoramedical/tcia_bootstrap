"""Bootstrap a DICOM collection from TCIA.

Supply the TCIA API key via a docker compose environment variable.

"""
import argparse
import json
import logging
import os
import zipfile
from io import BytesIO

import requests
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
from tqdm import tqdm

requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)

logging.getLogger().setLevel(logging.INFO)

TCIA_URL = "https://services.cancerimagingarchive.net/services/v3/TCIA/query"
DICOM_URL = "https://dicom:8042"


def api_url(endpoint):
    """Generate TCIA REST API URL."""
    return "/".join([TCIA_URL, endpoint])


def get_collections():
    """Get available TCIA collections."""
    url = api_url("getCollectionValues")
    r = requests.get(url)
    collections = [d["Collection"] for d in json.loads(r.content)]
    collections.sort()
    return collections


def main():
    parser = argparse.ArgumentParser(
        description="Pull TCIA collection into DICOM server."
    )
    parser.add_argument(
        "-c",
        "--collection",
        nargs="?",
        dest="collection",
        type=str,
        help=(f"TCIA collections from: {get_collections()}"),
    )
    parser.add_argument(
        "--limit",
        nargs="?",
        type=int,
        default=None,
        help=("Limit the number of series pulled"),
    )
    options = parser.parse_args()

    # Get collection name
    collection = options.collection or os.getenv("COLLECTION")
    if not collection or options.list:
        collections = get_collections()
        raise ValueError(
            "Collection must be specified in environment variables or via command-line arguments."
            f" Use value from: {collections}."
        )

    # Get all series ids in TCIA collection
    logging.info(f"Getting series ids for collection {collection}...")
    url = api_url("getSeries")
    series = requests.post(
        url, data={"format": "json", "Collection": collection}
    ).json()

    # Fetch series
    logging.info(f"Retrieving series for collection {options.collection}...")
    for i, s in enumerate(series):
        # Break at series limit
        if i + 1 > (options.limit or len(series)):
            logging.warning(f"Stopping at limit of {options.limit} series...")
            break

        logging.info(f"Series {i + 1} / {len(series)}")

        # Get zip of instances
        uid = s["SeriesInstanceUID"]
        url = api_url("getImage")
        r = requests.post(url, data={"SeriesInstanceUID": uid}, stream=True)
        r.raw.decode_content = True

        # Extract instances from zipfile
        logging.info(f"Storing instances from series {uid} in DICOM server...")
        z = zipfile.ZipFile(BytesIO(r.content))
        for name in tqdm(z.namelist()):
            url = api_url("instances")
            r = requests.post(
                url,
                data=z.read(name),
                headers={"Content-Type": "application/octet-stream"},
            )
            logging.debug(r.status_code)


if __name__ == "__main__":
    main()
