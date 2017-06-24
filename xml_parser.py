from xml.etree.ElementTree import parse
import urllib

# Data  acquisition ######################
url = 'http://w1.weather.gov/xml/current_obs/KRDU.xml'
u = urllib.urlopen(url)

# Extraction and parsing #################
curr_obs = parse(u).getroot()
location = curr_obs.find('location').text
temperature = curr_obs.find('temp_f').text
humidity = curr_obs.find('relative_humidity').text
Weather = curr_obs.find('weather').text

# Output Formatting #######################
print u'Current observation in %s is %s\u00B0 with %s%% humidity and is %s' % \
      (location, temperature, humidity, Weather)
