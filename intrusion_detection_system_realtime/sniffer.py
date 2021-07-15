import argparse

from scapy.sendrecv import AsyncSniffer

from flow_session import FlowSession



def capture_realtime():


    NewFlowSession = FlowSession()



    return AsyncSniffer(
            iface='Wi-Fi',
            filter="ip and (tcp or udp)",
            prn=None,
            session=NewFlowSession,
            store=False,
        )
def capture_offline(pcap_file):
    NewFlowSession=FlowSession()
    return AsyncSniffer(
        offline=pcap_file,
        filter="ip and (tcp or udp)",
        prn=NewFlowSession.on_packet_received,
        session=NewFlowSession,
        store=False,
    )


'''def main():

 

    sniffer = capture_realtime(

    )
    sniffer.start()

    try:
        sniffer.join()
    except KeyboardInterrupt:
        sniffer.stop()
    finally:
        sniffer.join()


if __name__ == "__main__":
    main()'''
