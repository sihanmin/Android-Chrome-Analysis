#!/usr/bin/python
# Filename: lte_mac_analyzer.py
"""
A 4G MAC-layer analyzer with the following functions

  - UL grant utilization analysis

  - TBA

Author: Yuanjie Li
"""


from mobile_insight.analyzer.analyzer import *
import datetime

__all__ = ["MyLteMacAnalyzer"]


class MyLteMacAnalyzer(Analyzer):

    def __init__(self):
        Analyzer.__init__(self)

        self.add_source_callback(self.__msg_callback)
        #self.result = open("test.csv","w+")

    def set_source(self, source):
        """
        Set the trace source. Enable the cellular signaling messages
        :param source: the trace source (collector).
        """
        Analyzer.set_source(self, source)

        # Phy-layer logs
        source.enable_log("LTE_MAC_DL_Transport_Block")
        # source.enable_log("LTE_PHY_PUSCH_Tx_Report")

    def save_msg(self, msg):
        with open("dl_bytes.csv","a") as wf:
            wf.write(msg)

    def __msg_callback(self, msg):

        if msg.type_id == "LTE_MAC_DL_Transport_Block":
            log_item = msg.data.decode()

            grant_received = 0


            for i in range(0, log_item['Num SubPkt']):
                for j in range(0, log_item['Subpackets'][i]['Num Samples']):
                    grant_received += log_item['Subpackets'][i]['Samples'][j]['DL TBS (bytes)']

            self.save_msg(str(log_item['timestamp']) +
                          "," +
                          str(grant_received) + "\n")

            self.log_info(str(log_item['timestamp']) +
                          " MAC DL grant: received=" +
                          str(grant_received) +
                          " bytes")
  
