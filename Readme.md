# Ruuvi Prometheus scraper

Collects weather data from multiple
[Ruuvi tags](https://ruuvi.com/ruuvitag-specs/) running the
[official firmware](https://lab.ruuvi.com/ruuvitag-fw/) for consumption by
[Prometheus](http://www.prometheus.io).

The python file `main.py` is hardcoded for my tags but can easily be modified
for your own needs.

You can also take a look at the files under `deploy/` that I use to run this
scraper on a Raspberry PI 3/4 (or a Rasberry Pi with an external Bluebooth
adaptor). They assume that the scraper is run with an user called `ruuvi`.
You also need to configure Prometheus to scrape data from the app from the
address `http://localhost:9521/metrics`.

## Install on [Raspian](https://www.raspbian.org)

### Premade Packages

```bash
apt-get install python3 bluez-hcidump python3-prometheus-client python-ptyprocess
```

### Exporter


```bash
git clone git@github.com:Hilzu/ruuvi-prometheus-scraper.git
cd ruuvi-prometheus-scraper
git submodule add https://github.com/ttu/ruuvitag-sensor.git
virtualenv venv -p python3
source venv/bin/activate
python main.py
```
