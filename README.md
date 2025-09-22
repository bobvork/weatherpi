
## Reference:

Waveshare docs for setup and demo code:
https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi


Other projects for inspiration and reference:
- epaper status display project: https://johnj.com/posts/e-paper-rpi-display/
- epaper dashboard project: https://code.mendhak.com/raspberrypi-epaper-dashboard/

Icon font:
https://erikflowers.github.io/weather-icons/

## Running

To run the script on reboot and every hour, put something like this in
the crontab

```sh

# Run every hour with reboot protection
0 * * * * /usr/local/bin/script-wrapper.sh

# Run on reboot with delay
@reboot sleep 300 && /usr/local/bin/script-wrapper.sh
```


