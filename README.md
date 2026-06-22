# **Cloudflare Dynamic DNS (DDNS) Python script** #

The script check your current public IP and compare it to the IP associated to the DNS records for a domain managed by [Cloudflare](https://www.cloudflare.com/). If different, the DNS record(s) will be updated with the new public IP.

### Requirements ###
* You need a [Cloudflare API](https://developers.cloudflare.com/api/) token with DNS Write permission.

* You can find the Zone ID for your domain in the right sidebar of your domain’s Overview page in the Cloudflare dashboard.
   * Here’s how to get the Zone ID:
       * From your current Account home, click the domain you want.
       * You’ll land on the Overview page for that zone.
       * Look at the API section on the right sidebar — your Zone ID is listed there with a copy button. Your Account ID is also shown in the same section for convenience.

* Since the script is written in Python (v3.14) with the package and project manager [uv](https://docs.astral.sh/uv/), it is recommended to install and use uv.

### Installation ###
  * Make sure uv is installed (follow the instructions on the website).
  * In the cloned repository folder, run the command:
  ```
  uv sync
  ```
  * Variables and options can be provided as systen environment variable, as arguments or in a .env file.

    _Note: Values from command-line arguments take precedence over environment variables._

      - API_TOKEN  [-t --token] Cloudflare API token. [required]
      - ZONE_ID [-z --zone required] Zone ID for your domain.  [required]
      - LOGGING [-l --logging INT] Logging options are: [optional]
        * 0 not logging
        * 1 always logging
        * 2 logging only when an IP update is performed OR errors
      - ZONE_ID [-f --file] log file path. [optional]. If the log file path is not provided, a logs.txt file will be created in the same folder as the Python script.

    _Note: To use a .env file, fill out the .env_template with the required information and save it to .env. You may want to keep the original file for git update compatibility._

### Usage ###
  ```
  uv run main.py [-t API_TOKEN -z ZONE_ID -l 0 -f log/file/path]
  ```

   _Note: don't put brackets when using arguments!_

### Use case example to run the script automatically on Linux ###
<<<<<<< HEAD
1. Create a cron job to run the script (every hour in this example).
=======
1. Create a cron job to run the python script (every hour in this example).
>>>>>>> 8f7a31dbf4663f998848c51b25ae433cdc3a115a
    ```
    crontab -e
    ```
2. Add the line:
    ```
    0 * * * * uv run --project /path/to/cloudflareddns/ /path/to/cloudflareddns/src/main.py
    ```
<<<<<<< HEAD
=======
    
>>>>>>> 8f7a31dbf4663f998848c51b25ae433cdc3a115a
