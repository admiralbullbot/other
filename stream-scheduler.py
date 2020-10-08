import boto3
import requests
import time

# Code: 0 (pending), 16 (running), 32 (shutting-down), 48 (terminated), 64 (stopping), and 80 (stopped)

session = boto3.session.Session(
    aws_access_key_id="censored",
    aws_secret_access_key="censored",
)

streamerID = 30816637  # Bulldog's ID
clientID = "censored"  # Bot's client ID


def modifyInstances(streamLive):
    for regionName in ["us-east-2", "eu-north-1"]:
        client = session.client("ec2", regionName)

        for respInstance in client.describe_instances()["Reservations"][0]["Instances"]:
            if {"Key": "Schedule", "Value": "stream"} in respInstance["Tags"]:
                if respInstance["State"]["Code"] == 16 and streamLive is False:
                    print(
                        f"Bulldog offline. Stopping instance {respInstance['InstanceType']}"
                    )
                    client.stop_instances(InstanceIds=[respInstance["InstanceId"]])
                elif respInstance["State"]["Code"] == 80 and streamLive is True:
                    client.start_instances(InstanceIds=[respInstance["InstanceId"]])
                    print(
                        f"Bulldog live. Starting instance {respInstance['InstanceType']}"
                    )


def main():
    while True:
        liveResponse = requests.get(
            f"https://api.twitch.tv/kraken/streams/{streamerID}",
            headers={
                "Client-Id": clientID,
                "Accept": "application/vnd.twitchtv.v5+json",
            },
        ).json()
        modifyInstances("stream" in liveResponse and liveResponse["stream"] is not None)
        time.sleep(300)


if __name__ == "__main__":
    main()
