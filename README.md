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
  * Parameters can be provided as system environment variables, as arguments or in a .env file.

    _Note: Values from command-line arguments take precedence over environment variables._

      - API_TOKEN  [-t --token] Cloudflare API token. [required]
      - ZONE_ID [-z --zone required] Zone ID for your domain.  [required]
      - LOGGING [-l --logging INT] Logging options are: [optional]
        * 0 not logging
        * 1 always logging
        * 2 logging only when an IP update is performed OR errors
      - LOG_FILE [-f --file] log file path. [optional]. If the log file path is not provided, a logs.txt file will be created in the same folder as the Python script.

    _Note: To use a .env file, fill out the .env_template with the required information and save it to .env. You may want to keep the original file for git update compatibility._

### Usage ###
```
uv run main.py [-t API_TOKEN -z ZONE_ID -l 0 -f log/file/path]
```

   _Note: don't put brackets when using arguments!_

### Use case 1 to run the script automatically on Linux with crontab ###
1. Create a cron job to run the Python script (every hour in this example).
```
crontab -e
```
2. Add the line:
```
0 * * * * /home/USERNAME/.local/bin/uv run --project /path/to/cloudflareddns/ /path/to/cloudflareddns/src/main.py
```
    
### Use case 2 to run the script automatically on Linux with a bash script ###

1.	Create a bash script to run the Python script and name it cloudflareddns.sh (_a template is provided in the utilities folder._)
```
 #!/bin/bash
 UV_PATH=/home/USERNAME/.local/bin/
 SCRIPT_PATH=/path/to/cloudflareddns/
 API_TOKEN=
 ZONE_ID=
 LOG_FILE=/path/to/log/logs.txt
 LOGGING=1

 ${UV_PATH}uv run --project ${SCRIPT_PATH} ${SCRIPT_PATH}/src/main.py -t ${API_TOKEN} -z ${ZONE_ID} -f ${LOG_FILE} -l ${LOGGING}
```

2.	Make the bash script executable.

```
chmod +x cloudflareddns.sh
```
   
3.	Create a new cron job run the script (every hour in this example).
```
crontab -e
```

4. Add the line:
```
0 * * * * /path/to/cloudflareddns.sh
```