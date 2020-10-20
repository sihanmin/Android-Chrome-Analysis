#!/usr/bin/python
# Filename: lte_rrc_analyzer.py
"""
A 4G MAC-layer analyzer with the following functions

  - UL grant utilization analysis

  - TBA

Author: Yuanjie Li
"""


try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
from mobile_insight.analyzer.analyzer import *
from mobile_insight.analyzer.protocol_analyzer import *
import datetime



__all__=["MyLteRrcAnalyzer"]


class MyLteRrcAnalyzer(ProtocolAnalyzer):

    """
    A protocol ananlyzer for LTE Radio Resource Control (RRC) protocol.
    """
    def __init__(self):
        ProtocolAnalyzer.__init__(self)
        self.add_source_callback(self.__msg_callback)
        #self.result = open("test1.csv","w+")
    

    def set_source(self, source):
        """
        Set the trace source. Enable the cellular signaling messages
        :param source: the trace source (collector).
        """
        Analyzer.set_source(self, source)

        # Phy-layer logs
        source.enable_log("LTE_RRC_OTA_Packet")

    def create_state_machine(self):
        """
        Declare a RRC state machine
        returns: a StateMachine
        """
        
        def idle_to_conn(msg):
            for field in msg.data.iter('field'):
                if field.get('name') == "lte-rrc.rrcConnectionSetupComplete_element":
                    return True

        def conn_to_idle(msg):
            for field in msg.data.iter('field'):
                if field.get('name') == "lte-rrc.rrcConnectionRelease_element":
                    return True

        state_machine={'RRC_IDLE':{'RRC_CONNECTED':idle_to_conn},
                       'RRC_CONNECTED':{'RRC_IDLE':conn_to_idle}}  

        return state_machine

    def init_protocol_state(self, msg):
        """
        Determine RRC state at bootstrap
        :returns: current RRC state, or None if not determinable 
        """
        for field in msg.data.iter('field'):
            if field.get('name') == "lte-rrc.rrcConnectionSetupComplete_element" \
            or field.get('name') == "lte-rrc.rrcConnectionReconfiguration_element":
                return 'RRC_CONNECTED'
            elif field.get('name') == "lte-rrc.rrcConnectionRelease_element":
                return 'RRC_IDLE'
        return None

    def save_msg(self, msg):
        with open("rrc_connection.csv","a") as wf:
            wf.write(msg)

    def __msg_callback(self, msg):
        log_item = msg.data.decode()
        log_item_dict = dict(log_item)

        if msg.type_id == "LTE_RRC_OTA_Packet":
            if 'Msg' not in log_item_dict:
                return

            #Convert msg to xml format
            # log_xml = ET.fromstring(log_item_dict['Msg'])
            log_xml = ET.XML(log_item_dict['Msg'])
            # xml_msg = Event(msg.timestamp,msg.type_id,log_xml)
            xml_msg = Event(log_item_dict['timestamp'],msg.type_id,log_xml)


            for field in xml_msg.data.iter('field'):
                if field.get('name') == "lte-rrc.rrcConnectionSetupComplete_element":
                    self.save_msg(str(log_item['timestamp']) + "," +
                        "rrcConnectionSetupComplete" + "\n")
                    self.log_info(str(log_item['timestamp']) + "," +
                        "rrcConnectionSetupComplete" + "\n")
                elif field.get('name') == "lte-rrc.rrcConnectionRequest_element":
                    self.save_msg(str(log_item['timestamp']) + "," +
                        "rrcConnectionRequest" + "\n")
                    self.log_info(str(log_item['timestamp']) + "," +
                        "rrcConnectionRequest" + "\n")
                elif field.get('name') == "lte-rrc.rrcConnectionRelease_element":
                    self.save_msg(str(log_item['timestamp']) + "," +
                        "rrcConnectionRelease" + "\n")
                    self.log_info(str(log_item['timestamp']) + "," +
                        "rrcConnectionRelease" + "\n")


            
            #for field in msg.data.iter('field'):
               # if field.get('name') == "lte-rrc.rrcConnectionRelease_element" : 
                   # self.log_info("connection release at: " + str(log_item['timestamp']))

                #self.save_msg(str(log_item['timestamp']) +
                       #   "," +
                        #  str(grant_received) + "\n")


