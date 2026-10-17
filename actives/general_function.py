import requests

from config import RV_TOKEN, RV_LINK, RV_CERT


def get_asset_data(request_params: dict,
                   asset_type_id: int
                   ):
    url = f"https://{RV_LINK}/api/v2/am/custom/{asset_type_id}"

    headers = {
        "X-Token": RV_TOKEN,
        "Content-Type": "application/json"
    }

    asset_data = requests.get(
        url,
        headers=headers,
        params=request_params,
        verify=RV_CERT
    )

    return asset_data
