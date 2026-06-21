# **Cloudflare Dynamic DNS (DDNS) Python script** #

The script check your current public IP and compare it to the IP associated to the DNS records for a domain managed by [Cloudflare](https://www.cloudflare.com/). If different, the DNS record(s) will be updated with the new public IP.



You need a [Cloudflare API](https://developers.cloudflare.com/api/) token with DNS Write permission.

You can find the Zone ID for your domain in the right sidebar of your domain’s Overview page in the Cloudflare dashboard.
* Here’s how to get there:
    * From your current Account home, click the domain you want.
    * You’ll land on the Overview page for that zone.
    * Look at the API section on the right sidebar — your Zone ID is listed there with a copy button. Your Account ID is also shown in the same section for convenience.

The script is written in Python (v3.14) with the package and project manager [uv](https://docs.astral.sh/uv/)

Fill the .env_template file with the information and save it to .env

* _Note: you may want to keep the original file for git update compatibility_
* The LOGGING options are:
  * 0: not logging
  * 1 always logging
  * 2 logging when update OR errors
