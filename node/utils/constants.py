class Constant:

    def __init__(self):
        pass

    # function to search the matching error message with the help of hexadecimal error code.
    def get_error_msg(self, code):

        try:
            error_msg = {
                '0x00': 'Normal',
                '0x0': 'Normal',
                '0x11': 'ROM Test During POST',
                '0x12': 'RAM Test During POST',
                '0x13': 'Serial POrt Test During POST',
                '0x14': 'Card Presense Test During POST',
                '0x15': 'Relay Test During POST',
                '0x21': 'ROM Test Failed During System Working',
                '0x22': 'RAM Test Failed During System Working',
                '0x24': 'Card Presence Failed During System Working',
                '0x30': 'Loss of carrier or Link',
                '0x31': 'Sequence of Error Mismatch',
                '0x32': 'Self Count Mismatch',
                '0x33': 'Movement of Train before Preparatory Reset',
                '0x34': 'Outcount Registered before Incount',
                '0x35': 'Negative Count',
                '0x36': 'Shunt Error',
                '0x37': 'Supervisory Error',
                '0x38': 'Internal Shunt Error',
                '0x39': 'Count Mismatch in MLB of same unit',
                '0x40': 'Corruption of Packets - Communication Error',
                '0x41': 'Corruption of Data - CRC Error',
                '0x42': 'COrruption of Data - End of Packet Corrupted',
                '0x43': 'Wheel Shunt Error',
                '0x44': 'Non-overlappig Pulse Found in Forward Direction',
                '0x45': 'Non-overlappig Pulse Found in Reverse Direction',
                '0x46': 'Exit Mismatch - Train IN Trolley OUT or Vice-Versa',
                '0x47': 'Following Trolley Shunt Back',
                '0x48': 'Train Enters After Motor Trolley',
                '0x50': 'Relay Error During POST in Clear State',
                '0x51': 'Relay Error During POST in Occupied State',
                '0x52': 'Relay Contact not Read Back in Clear State',
                '0x53': 'Relay Contact not Read Back in Occupied State',
                '0x60': 'Corruption of SW in Micro-controllers',
                '0x61': 'MLB Decision Mismatch',
                '0x62': 'Secondary CPU Failed',
                '0x66': 'Micro-controller\'s Watchdog Timer Reset',
                '0x70': 'Change in COnfiguration During POST',
                '0x71': 'J Packet Configuration Error',
                '0x72': 'R Packet Configuration Error',
                '0x73': 'Address Changed During System Working',
                '0x74': 'U Packet Configuration Error',
                '0x80': 'Error in Remote System',
                '0x7F': 'Remote Unit is Reset, Local is Not',
                '0x3F': 'Local Unit is Reset, Remote is Not'
            }

            if code in error_msg:
                return error_msg[code]
            else:
                return "Undefined Error Code"

        except Exception as ex:
            return ex
