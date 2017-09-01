#
# USBProxy logging filters
#

import datetime

from ..USBProxy import USBProxyFilter

class USBProxyPrettyPrintFilter(USBProxyFilter):
    pass

    def __init__(self, verbose, decoration=''):
        """
        Sets up a new USBProxy pretty printing filter.
        """
        self.verbose = verbose
        self.decoration = decoration

    def filter_control_in(self, req, data, stalled):

        if req is None:
            print("{} {}< --filtered out-- ".format(self.timestamp(), self.decoration))
            return req, data, stalled

        if self.verbose > 3:
            print("{} {}{}".format(self.timestamp(), self.decoration, repr(req)))

        if self.verbose > 3 and stalled:
            print("{} {}< --STALLED-- ".format(self.timestamp(), self.decoration))

        if self.verbose > 4 and data:
            is_string = (req.request == 6) and (req.value >> 8 == 3)
            self._pretty_print_data(data, '<', self.decoration, is_string)

        return req, data, stalled


    def filter_control_out(self, req, data):

        # TODO: just call control_in, it's the same:

        if self.verbose > 3 and req is None:
            print("{} {}> --filtered out-- ".format(self.timestamp(), self.decoration))
            return req, data

        if self.verbose > 3:
            print("{} {}{}".format(self.timestamp(), self.decoration, repr(req)))

        if self.verbose > 4 and data:
            self._pretty_print_data(data, '>', self.decoration)

        return req, data


    def handle_out_request_stall(self, req, data, stalled):
        if self.verbose > 3 and req is None:
            if stalled:
                print("{} {}> --STALLED-- ".format(self.timestamp(), self.decoration))
            else:
                print("{} {}> --STALLED, but unstalled by filter-- ".format(self.timestamp(), self.decoration))

        return req, data, stalled


    def filter_in(self, ep_num, data):

        if self.verbose > 4:
            print("IN", ep_num, data)

        return ep_num, data

    def filter_out(self, ep_num, data):

        if self.verbose > 4:
            print("OUT", ep_num, data)

        return ep_num, data


    def timestamp(self):
        return datetime.datetime.now().strftime("[%H:%M:%S]")

    def _magic_decode(self, data):
        try:
            return bytes(data).decode('utf-16le')
        except:
            return bytes(data)


    def _pretty_print_data(self, data, direction_marker, decoration='', is_string=False):
        data = self._magic_decode(data) if is_string else bytes(data)
        print("{} {}{}: {}".format(self.timestamp(), decoration, direction_marker, data))



