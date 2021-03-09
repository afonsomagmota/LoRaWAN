# Wireless Control System using LoRaWAN

Get started in IoT using The Things Network, Thingspeak and Micropython.

In this repository, you can find the source code for the MicroPython end-node (I used LoPy4) that receives data from a DHT21 sensor (in here you can also find the library) and sends it over a LoRaWAN network to The Things Network which will retreive the data to Thingspeak, in order to plot the data and send a response with an action to the end-node based on the temperature and humidity values. In this case, we are controlling the shutters of a Trombewall.

Make sure to get your Device Extended Unique Identifier because you will need it to register your device and create an application with The Things Network.
Once you create it, you will have an App_EUI and an App_Key, which will be used to create a connection between the end-device and the server/app. Replace those values you get from the TTN in the source code you upload to the MicroPython device, and things should be running smoothly.

In order to plot the data and get responses, you'll need to create a Thingspeak account and, in TTN, integrate the Thingspeak platform.

Create graphs in Thingspeak and associate each port that you'll find in TTN payload format decoder (JS file, that you'll also need to upload to TTN).

To get responses from the application to the end device, setup a React for certain values and a ThingHTTP (corresponding to that React) in Thingspeak, so you can POST an information in JSON format back to TTN.

This consists in a Class A LoRaWAN device: once is sent one message from the end-node, a 20ms window is opened by the microcontroller expecting a response.

However, even if you have a programmed response in the application side for a certain value, this same response will only arrive the next time the microcontroller sends information because it will be waiting in the server.
We can agree that a 20ms window isn't enough to the response being processed in the server/application side.

Therefore, if you want to build a project where accurate data and actions are extremely important, LoRaWAN class A end-devices are probably not what you are looking for.

