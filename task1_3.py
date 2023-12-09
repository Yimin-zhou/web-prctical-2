import io
import time
from mastodon import Mastodon, StreamListener
import json
from datetime import datetime

# Create an app and obtain the client credentials.
# Substitute the name of your app and name of the credentials file.
Mastodon.create_app("myapp",
api_base_url="https://mastodon.social",
to_file="client_credential.secret"
)
# Substitute the name of the credentials file.
mastodon = Mastodon(
client_id="client_credential.secret"
)
# Log in with your account.
# Substitute your e-mail and password
# and the name of the credentials file.
mastodon.log_in("lingxiaojun2018@gmail.com", "5KczDfLDd!qU,?6",
to_file="user_credential.secret"
)

class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return super().default(obj)
        
class StdOutListener(StreamListener):
    """
    A listener handles Statuses received from the stream.
    This basic listener simply prints received statuses to stdout.
    You need to modify the code to solve the tasks.
    """
    
    def on_update(self, status):
        keywords = ["israel", "palestine", "hamas", "gaza", "israel-palestine conflict"]
        text = status.get("content", "").lower()
        with open(file_name, "a", encoding="utf-8") as file:
            json.dump(status, file, cls=DateTimeEncoder, ensure_ascii=False)
            file.write(",\n")
        if any(keyword in text for keyword in keywords):
            with open(filtered_file_name, "a", encoding="utf-8") as filtered_file:
                json.dump(status, filtered_file, cls=DateTimeEncoder, ensure_ascii=False)
                filtered_file.write(",\n")
        return True

    def on_abort(self, err):
        print(err)

# Get the current date and time
current_datetime = datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# Create the file name with the formatted date and time
file_name = f"status_{formatted_datetime}.json"
filtered_file_name = f"filtered_status_{formatted_datetime}.json"

# formatting json file
with open(file_name, "a") as file:
    file.write("[")
with open(filtered_file_name, "a") as filtered_file:
    filtered_file.write("[")

l = StdOutListener()
user = mastodon.stream_public(listener=l, run_async=True)

# Run the stream for 2 hours
time.sleep(7200)
user.close()

# Remove the last comma and newline character from status.json
with open(file_name, "rb+") as file:
    file.seek(-3, io.SEEK_END)
    file.truncate()
with open(filtered_file_name, "rb+") as filtered_file:
    filtered_file.seek(-3, io.SEEK_END)
    filtered_file.truncate()

# formatting json file
with open(file_name, "a") as file:
    file.write("]")
with open(filtered_file_name, "a") as filtered_file:
    filtered_file.write("]")