import json
from utils.sanitize import Sanitize
from process_packet import ProcessPKT
from utils.make_request import Server_Call
from utils.logger import Logger

logger = Logger().get_logger()


class SendToServer:

    def __init__(self):

        # initialize objects
        self.mr = Server_Call()
        self.san = Sanitize()
        self.process = ProcessPKT()

        # load packet status json file
        with open("./config/packet_status.json") as json_file:
            json_data = json.load(json_file)

        self.node_config = json_data

    '''
    check the status of packet is that changed from the previous packet or not
    '''
    def is_recieved_packet_change(self, packet):
        try:
            # sanitize packet
            sanitized_pkt = self.san.sanitize_packet(packet)

            pkt_type, card, num = self.get_pkt_card_and_no(sanitized_pkt)
            print("PACKET:", pkt_type)
            print("CARD:", card)
            print("TS/DP:", num)

            # check for packet type other than T and D
            if pkt_type in ["T", "D"]:
                prev_pkt = self.node_config["Card"][card][pkt_type][num]
            elif pkt_type == "H":
                prev_pkt = self.node_config["HASSDAC"]
            elif pkt_type == "S":
                prev_pkt = self.node_config["SSDAC"]
            else:
                prev_pkt = sanitized_pkt

            # check current and prev packet
            if sanitized_pkt == prev_pkt:
                return False, pkt_type
            else:
                self.node_config["Card"][card][pkt_type][num] = sanitized_pkt
                json_object = self.node_config

                pkt_file = open("./config/packet_status.json", "w")
                json.dump(json_object, pkt_file, indent=4)
                pkt_file.close()

            return True, pkt_type
        except Exception as ex:
            raise ex

    '''
    process the packet to check packet status, prepare paylaod and send to server
    '''
    def process_packet(self, packet):
        try:
            status, pkt_type = self.is_recieved_packet_change(packet)

            if status:
                schema_payload = self.prepare_payload(packet, pkt_type)

                # send data to server
                # payload = self.payload
                # response = self.send_payload_to_server(payload)

            return schema_payload

        except Exception as ex:
            return ex

    '''
    get the packet name, card number and track section of detection point information from recieved packet
    '''
    @staticmethod
    def get_pkt_card_and_no(data):
        try:
            packet_type = data[1]
            card = data[2]
            number = data[3]
            return packet_type, card, number

        except Exception as ex:
            return ex

    '''
    send the prepared payload packet to server
    '''
    def send_payload_to_server(self, payload):
        try:
            response = self.mr.post_to_server(payload)
            return response

        except Exception as ex:
            return ex

    '''
    prepare the payload to sent to server
    '''
    def prepare_payload(self, packet, pkt_type):
        try:
            if pkt_type == "T":
                payload = self.process.process_T_packet(packet)
            elif pkt_type == "D":
                payload = self.process.process_D_packet(packet)
            elif pkt_type == "H":
                payload = self.process.process_H_packet(packet)
            else:
                payload = {}

            # update the payload with actual payload
            # payload schema to prepare the server payload
            with open("./config/payload_schema.json") as json_file:
                schema_payload = json.load(json_file)

            schema_payload.update(payload)
            return schema_payload

        except Exception as ex:
            return ex
