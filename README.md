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
  * Fill the .env_template file with the information and save it to .env
    * _Note: you may want to keep the original file for git update compatibility_
    * The LOGGING options are:
      * 0: not logging
      * 1 always logging
      * 2 logging only when an IP update is performed OR errors


### Use case example to run the script automatically on Linux ###
1.	Create a bash script to run the Python script and name it cloudflareddns.sh
    ```
    #!/bin/bash
    # run the cloudflareddns python script.
    uv run --project /path/to/cloudflareddns/ /path/to/cloudflareddns/src/main.py
    ```
2.	Make the bash script executable.
    ```
    chmod +x cloudflareddns.sh
    ```
3.	Create a new cron job run the script (every hour in this example).
    ```
    crontab -e
    ```

    add a line like:
    ```
    0 * * * * / path/to/scripts/cloudflareddns.sh
    ```

