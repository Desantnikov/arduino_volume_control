import serial

from v2.constants import DEFAULT_SERIAL_PORT_NAME
from v2.device_responses_handler import DeviceResponsesHandler

device_response_handler = DeviceResponsesHandler()


def start_event_loop():
    while True:
        device_response = device.readline().decode()
        # print(f'Decoded device response: {device_response}')

        # get handler function corresponding to the data
        handler_function = device_response_handler.get_handler_function(device_response)
        handler_function(device_response)


if __name__ == "__main__":
    serial_port_name = input(f"Enter serial port to use. Use default ({DEFAULT_SERIAL_PORT_NAME}) if blank:\r\n")
    serial_port_name = serial_port_name or DEFAULT_SERIAL_PORT_NAME

    device = serial.Serial(serial_port_name)
    print(f'Device connected: {device}')

    try:
        start_event_loop()
    except Exception as e:
        print(f'\r\n\r\nUnexpected exception: {e}')

    finally:
        device.close()
