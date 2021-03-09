function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};

  if (port === 1) {
    decoded.HUMcam = (((bytes[0] << 8 | bytes[1]) / 100).toFixed(2));
    if (bytes[2] & 0x80){
      decoded.TMPcam = ((((bytes[2] << 8 | bytes[3])-65536) / 100).toFixed(2));
    } else {
      decoded.TMPcam = (((bytes[2] << 8 | bytes[3]) / 100).toFixed(2));
    }
    decoded.HUMi = (((bytes[4] << 8 | bytes[5]) / 100).toFixed(2));
    if (bytes[2] & 0x80){
      decoded.TMPi = ((((bytes[6] << 8 | bytes[7])-65536) / 100).toFixed(2));
    } else {
      decoded.TMPi= (((bytes[6] << 8 | bytes[7]) / 100).toFixed(2));
    }
    TMPdif = (decoded.TMPcam - decoded.TMPi).toFixed(2);
    HUMdif = (decoded.HUMcam - decoded.HUMi).toFixed(2);
  return {
    field1:TMPdif,
    field2:HUMdif,
    field3:decoded.TMPcam,
    field4:decoded.HUMcam,
    field5:decoded.TMPi,
    field6:decoded.HUMi
    };
  }
  if (port === 2) {
    decoded.time = ((bytes[0] << 8) | bytes[1]).toFixed(2);
  return {
    status:decoded.time
    };
  }
  if (port === 4) {
    decoded.blindstate = bytes[0];
  return {
    field8 : decoded.blindstate
    };
  }
}
