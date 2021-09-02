import pandas as pd
import requests

# Reads the csv files
file_a = pd.read_csv('fileA.csv', index_col=False)
file_b = pd.read_csv('fileB.csv', index_col=False)

# combines and transforms them to a dictionary
merged = pd.merge(file_a, file_b,
                  on='user_id',
                  how='inner').to_dict(orient="records")

# API variables:
aid = "o1sRRZSLlw"
api_token = "xeYjNEhmutkgkqCZyhBn6DErVntAKDx30FqFOS6D"

# The following loops calls the API to check if there's a user_id registered with the mail given
# if so, replaces that user_id with the one located in the APP data

merged_to_check = merged[:]

for i in merged_to_check:
    try:  # I am using this try since i assuming some users will not be found in the system and i need to catch a IndexError
        email = i["email"]
        url = f"https://sandbox.piano.io/api/v3/publisher/user/list?aid={aid}&offset=0&api_token={api_token}&q={email}"
        response = requests.request("POST", url).json()
        uid = response.get("users")[0]["uid"]
        if uid != i["user_id"]:
            i["user_id"] = uid
    except IndexError:
        pass  # There's no need to do anything else.

merged_csv_file = pd.DataFrame(merged_to_check)
merged_csv_file.to_csv("fileC.csv", index=False)
