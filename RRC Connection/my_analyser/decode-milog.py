#!/usr/local/bin/python2
# Filename: decode-milog.py

'''
A script to decode and dump the qmdl/mi2log and print out the verbose xml message
Usage:
$ python decode.py > log.txt
the decoded message will be stored at log.txt

Author : Zengwen Yuan
Rev    : v2.4  2018-04-19  Modify for the latest mobileinsight release
         v2.3  2017-10-31  add LTE msg type, customize type
         v2.2  2017-02-25  add msg_type == 'haft' support
         v2.1  2016-04-21  add msg_type == 'all' support
         v1.0  2015-12-05  Init script
'''

import os, sys
from mobile_insight.monitor import OfflineReplayer
from mobile_insight.analyzer import Analyzer

lte_rrc = [
            'LTE_RRC_CDRX_Events_Info',
            'LTE_RRC_OTA_Packet',
            'LTE_RRC_Serv_Cell_Info',
            'LTE_RRC_MIB_Packet',
            'LTE_RRC_MIB_Message_Log_Packet',
            ]
lte_nas = [
            'LTE_NAS_ESM_State',
            'LTE_NAS_ESM_OTA_Incoming_Packet',
            'LTE_NAS_ESM_OTA_Outgoing_Packet',
            'LTE_NAS_EMM_State',
            'LTE_NAS_EMM_OTA_Incoming_Packet',
            'LTE_NAS_EMM_OTA_Outgoing_Packet',
            ]
lte_pdcp   = [
            'LTE_PDCP_DL_Cipher_Data_PDU',
            'LTE_PDCP_DL_Config',
            'LTE_PDCP_DL_Ctrl_PDU',
            'LTE_PDCP_DL_SRB_Integrity_Data_PDU',
            'LTE_PDCP_DL_Stats',
            'LTE_PDCP_UL_Cipher_Data_PDU',
            'LTE_PDCP_UL_Config',
            'LTE_PDCP_UL_Ctrl_PDU',
            'LTE_PDCP_UL_Data_PDU',
            'LTE_PDCP_UL_SRB_Integrity_Data_PDU',
            'LTE_PDCP_UL_Stats',
            ]
lte_rlc = [
            'LTE_RLC_DL_AM_All_PDU',
            'LTE_RLC_DL_Config_Log_Packet',
            'LTE_RLC_DL_Stats',
            'LTE_RLC_UL_AM_All_PDU',
            'LTE_RLC_UL_Config_Log_Packet',
            'LTE_RLC_UL_Stats',
            ]
lte_mac = [
            'LTE_MAC_Configuration',
            'LTE_MAC_DL_Transport_Block',
            'LTE_MAC_Rach_Attempt',
            'LTE_MAC_Rach_Trigger',
            'LTE_MAC_UL_Buffer_Status_Internal',
            'LTE_MAC_UL_Transport_Block',
            'LTE_MAC_UL_Tx_Statistics',
            ]
lte_phy = [
            'LTE_PHY_BPLMN_Cell_Confirm',
            'LTE_PHY_BPLMN_Cell_Request',
            'LTE_PHY_Connected_Mode_Intra_Freq_Meas',
            'LTE_PHY_Connected_Mode_Neighbor_Measurement',
            'LTE_PHY_Idle_Neighbor_Cell_Meas',
            'LTE_PHY_Inter_RAT_CDMA_Measurement',
            'LTE_PHY_Inter_RAT_Measurement',
            'LTE_PHY_PDCCH_Decoding_Result',
            'LTE_PHY_PDCCH_PHICH_Indication_Report',
            'LTE_PHY_PDSCH_Decoding_Result',
            'LTE_PHY_PDSCH_Packet',
            'LTE_PHY_PDSCH_Stat_Indication',
            'LTE_PHY_PUCCH_CSF',
            'LTE_PHY_PUCCH_Power_Control',
            'LTE_PHY_PUCCH_Tx_Report',
            'LTE_PHY_PUSCH_CSF',
            'LTE_PHY_PUSCH_Power_Control',
            'LTE_PHY_PUSCH_Tx_Report',
            'LTE_PHY_RLM_Report',
            'LTE_PHY_Serv_Cell_Measurement',
            'LTE_PHY_Serving_Cell_COM_Loop',
            'LTE_PHY_System_Scan_Results',
]
wcdma    = [
            'WCDMA_RRC_OTA_Packet',
            'WCDMA_RRC_Serv_Cell_Info',
            ]
umts     = [
            'UMTS_NAS_OTA_Packet',
            'UMTS_NAS_GMM_State',
            'UMTS_NAS_MM_State',
            'UMTS_NAS_MM_REG_State',
            ]
custom   = lte_rrc + lte_nas + lte_pdcp



class DumpAnalyzer(Analyzer):
    """
    Dump cellular logs in xml format from binary logs
    """

    def __init__(self, decodeformat):
        Analyzer.__init__(self)
        self.add_source_callback(self.__log_decoder)
        self.decode_format = decodeformat

    def __log_decoder(self, event):
        if self.decode_format == "raw":
            log_item = event.data.decode()
        elif self.decode_format == "xml":
            log_item = event.data.decode_xml()
        elif self.decode_format == "json":
            log_item = event.data.decode_json()
        else:  # default json
            log_item = event.data.decode_json()
        print str(log_item).lower()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: python decode-milog.py <filename> <msg_type> <decode_format>"
        sys.exit()

    file_in = sys.argv[1]
    print sys.argv[1]
    if sys.argv[2] is not None:
        msg_type = sys.argv[2]
    else:
        msg_type = 'rrc'
    if sys.argv[3] is not None:
        decode_format = sys.argv[3]
    else:
        decode_format = 'json'

    # Initialize a 3G/4G monitor
    src = OfflineReplayer()
    src.set_input_path(file_in)

    if msg_type == '4g':
        src.enable_log(lte_nas + lte_rrc + lte_pdcp + lte_rlc + lte_mac + lte_phy)
    elif msg_type == '3g':
        src.enable_log(umts + wcdma)
    elif msg_type == 'nas':
        src.enable_log(lte_nas + umts)
    elif msg_type == 'rrc':
        src.enable_log(lte_rrc + wcdma)
    elif msg_type == 'rrcnas':
        src.enable_log(lte_rrc + lte_nas + wcdma + umts)
    elif msg_type == 'pdcp':
        src.enable_log(lte_pdcp)
    elif msg_type == 'rlc':
        src.enable_log(lte_rlc)
    elif msg_type == 'mac':
        src.enable_log(lte_mac)
    elif msg_type == 'phy':
        src.enable_log(lte_phy)
    elif msg_type == 'custom':
        src.enable_log(custom)
    elif msg_type == 'all':
        src.enable_log_all()
    else:
        print "Unrecognized message type: %s" % msg_type
        sys.exit(1)

    # Start the monitoring
    logger = DumpAnalyzer(decode_format)
    logger.set_source(src)
    src.run()
