# Statistics from netem runs

These scripts get statistics from netem-runs.

## Install requirements and setup virtualenv

```
virtualenv -p python3 .venv
pip install -U -r requirements.txt
source .venv/bin/activate
```

## How they work

The script `generate-stats` takes the same arguments as `netem` and aggregates the HTTP archives saved from netem runs with the same parameters inte one json file that's easier to do statistical analysis on.

```json
{
    "identifiers": {
        "web_protocol": "PROTOCOL",
        "loss_ul": "PERCENT_LOSS_ON_UPLINK",
        "delay_ul": "DELAY_ON_UPLINK",
        "deviation_ul": "DELAY_DEVIATION_UPLINK",
        "bandwidth_ul": "BANDWIDTH_UPLINK",
        "loss_dl": "LOSS_RATE_DOWNLINK",
        "delay_dl": "DELAY_ON_DOWNLINK",
        "deviation_dl": "DELAY_DEVIATION_ON_DOWNLINK",
        "bandwidth_dl": "BANDWIDTH_DOWNLINK"
    },
    "websites": {
        "example.com": [
            {
                "time": 9001,
                "status": true,
                "total_bytes_fetched": 9001,
                "resource_count": 3
            },
            {
                "time": 3000,
                "status": false,
                "error": "Some error."
            }
        ]
    }
}

```

The other scripts do some form of statistical analyssis on the data from `generate-stats`.
