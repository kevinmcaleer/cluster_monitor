# Cluster Monitor

A Pimoroni Plasma 2350 for monitoring the temperature of the Mini-Rack, and displaying the temperature and status via the LED strip.

The Modes are changeable via MQTT messages:

alert - The LED strip will flash red when the temperature is above the threshold
warning - The LED strip will glow yellow when the temperature is above the threshold
normal - The LED strip will glow green when the temperature is below the threshold

You will also need to create a wifi_config.py file:

```python
SSID = "your wifi hotspot here"
PASSWORD = "your password here"
```

---
