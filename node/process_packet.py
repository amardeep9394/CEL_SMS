from utils.constants import Constant
from utils.logger import Logger

logger = Logger().get_logger()


class ProcessPKT:
    def __init__(self):
        self.constant = Constant()

    # Create list of the errors from the bytes of the T packet
    def ts_error_lst(self, status_binary):

        # list contains all the list of errors in DP and TS
        error_lst = []

        status = ''
        if status_binary[0] == '1':

            if status_binary[1] == '1':
                error_lst.append('Error(Due to DP)')
            if status_binary[2] == '1':
                error_lst.append('DACFU SUP')
            if status_binary[3] == '1':
                error_lst.append('Relay Status')
            if status_binary[4] == '1':
                error_lst.append('Link Error')
            if status_binary[5] == '1':
                error_lst.append('Comm Error')

            ts_status = status_binary[6:8]
            if ts_status == '00':
                status = 'RESET'
            if ts_status == '01':
                status = 'PREPARATORY RESET'
            if ts_status == '10':
                status = 'OCCUPIED'
            if ts_status == '11':
                status = 'UNOCCUPIED'

        else:
            error_lst.append('Inactive')
            status = '--'

        # check error
        if ("Error(Due to DP)" or "Link Error" or "Comm Error") in error_lst:
            system_status = "Unknown"
        else:
            system_status = ""

        error = ','.join(error_lst)
        return error, status, system_status

    def process_T_packet(self, packet):

        try:
            card_no = packet[2]
            tc_no = packet[3]
            ts_id = card_no + tc_no
            status = packet[4:7]
            status_binary = '{0:012b}'.format(int(status, 16))
            error, ts_status, system_status = self.ts_error_lst(status_binary)

            # prepare dict data
            data = {"Card_No": card_no,
                    "TS_ID": ts_id,
                    "TS_Status": ts_status,
                    "Remarks": error,
                    "System_Status": system_status,
                    "Packet_Type": "T"
                    }
            return data

        except Exception as ex:
            return ex

    def process_D_packet(self, packet):

        try:
            card_no = packet[2]
            channel_no = packet[3]
            dp_id = card_no + channel_no
            error_code = packet[5:7]
            hex_error_code = self.constant.get_error_msg(hex(int(error_code)))

            # prepare dict data
            data = {"Card_No": card_no, "DP_ID": dp_id, "Error_Code": hex_error_code, "Packet_Type": "D"}
            return data

        except Exception as ex:
            return ex

    def process_H_packet(self, packet):

        try:
            system1_status = ""
            system2_status = ""
            unknown = ""

            if len(packet) == 4:
                system1_status = packet[3]
                system2_status = '--'
                unknown = '--'
            if len(packet) == 5:
                system1_status = packet[3]
                system2_status = packet[4]
                unknown = '--'

            if len(packet) == 6:
                system1_status = packet[3]
                system2_status = packet[4]
                unknown = packet[5]

            # prepare dict data
            data = {"System1_Status": system1_status,
                    "System2_Status": system2_status,
                    "Unknown": unknown,
                    "Packet_Type": "H"}
            return data

        except Exception as ex:
            return ex
