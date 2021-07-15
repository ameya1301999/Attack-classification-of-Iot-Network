from sniffer import capture_realtime,capture_offline
from scapy.all import sniff
from flow_session import FlowSession
import config
import os
def main():
    print("ANALYZE NETWORK TRAFFIC IN ONLINE MODE OR OFFLINE MODE")
    print("1: ONLINE TRAFFIC ANALYSIS")
    print("2: OFFLINE TRAFFIC ANALYSIS")
    choice=int(input())

    if(choice==1):
        sniffer = capture_realtime()
        sniffer.start()

        try:
           sniffer.join()
        except KeyboardInterrupt:
           sniffer.stop()
        finally:
           sniffer.join()
    else:

        filepaths  = [os.path.join(config.folderpath, name) for name in os.listdir(config.folderpath)]
        newflowsession=FlowSession
        for pcap_file in filepaths:
          sniff(offline=pcap_file,prn=newflowsession.on_packet_received,session=newflowsession,store=0)
          ''' sniffer=capture_offline(pcap_file)
           sniffer.start()
           try:
             sniffer.join()
           except KeyboardInterrupt:
             sniffer.stop()
           finally:
             sniffer.join()'''
          print("Finished analyzing traffic from pcap file")


if __name__ == "__main__":
    main()