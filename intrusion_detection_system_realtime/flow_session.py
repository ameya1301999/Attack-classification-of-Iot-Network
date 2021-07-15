import gc
from collections import defaultdict
from real_time_detection import predict

from scapy.sessions import DefaultSession

from features.context.packet_direction import PacketDirection
from features.context.packet_flow_key import get_packet_flow_key
from flow import Flow
import numpy as np
from colorama import Fore
import tensorflow as tf
from numpy  import newaxis

EXPIRED_UPDATE = 40

GARBAGE_COLLECT_PACKETS = 100


class FlowSession(DefaultSession):
    """Creates a list of network flows."""

    def __init__(self, *args, **kwargs):
        self.flows = {}


        self.flows_count=np.empty((0,21))

        self.packets_count = 0
        self.fl_count=0

        self.clumped_flows_per_label = defaultdict(list)

        super(FlowSession, self).__init__(*args, **kwargs)

    def toPacketList(self):
        # Sniffer finished all the packets it needed to sniff.
        # It is not a good place for this, we need to somehow define a finish signal for AsyncSniffer
        self.garbage_collect(None)
        return super(FlowSession, self).toPacketList()

    def on_packet_received(self, packet):
        count = 0
        direction = PacketDirection.FORWARD



        try:
            # Creates a key variable to check
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))
        except Exception:
            return

        self.packets_count += 1

        # If there is no forward flow with a count of 0
        if flow is None:
            # There might be one of it in reverse
            direction = PacketDirection.REVERSE
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))

            if flow is None:
                # If no flow exists create a new flow
                direction = PacketDirection.FORWARD
                flow = Flow(packet, direction)
                packet_flow_key = get_packet_flow_key(packet, direction)
                self.flows[(packet_flow_key, count)] = flow

            elif (packet.time - flow.latest_timestamp) > EXPIRED_UPDATE:
                # If the packet exists in the flow but the packet is sent
                # after too much of a delay than it is a part of a new flow.
                expired = EXPIRED_UPDATE
                while (packet.time - flow.latest_timestamp) > expired:
                    count += 1
                    expired += EXPIRED_UPDATE
                    flow = self.flows.get((packet_flow_key, count))

                    if flow is None:
                        flow = Flow(packet, direction)
                        self.flows[(packet_flow_key, count)] = flow
                        break

        elif (packet.time - flow.latest_timestamp) > EXPIRED_UPDATE:
            expired = EXPIRED_UPDATE
            while (packet.time - flow.latest_timestamp) > expired:

                count += 1
                expired += EXPIRED_UPDATE
                flow = self.flows.get((packet_flow_key, count))

                if flow is None:
                    flow = Flow(packet, direction)
                    self.flows[(packet_flow_key, count)] = flow
                    break

        flow.add_packet(packet, direction)


        if self.packets_count % GARBAGE_COLLECT_PACKETS == 0 or (
            flow.duration > 120
        ):

          flows_predict=self.garbage_collect(packet.time)
          self.fl_count=self.fl_count+1;
          print("FLOWS GENERATED =",self.fl_count,end="\r")

          if(flows_predict!= None):
            flows_predict=list(flows_predict)
            print(f'{Fore.WHITE}')
            print(flows_predict)
            flows_predict=np.array(flows_predict)
            #if(self.flows_count.size==0):
            #    self.flows_count=flows_predict
            #else:
            #self.flows_count= np.append(self.flows_count,flows_predict, axis=0)

            r,c=self.flows_count.shape
            pred_value=predict(flows_predict)
            print("pred_value=",pred_value)

            print(f'{Fore.YELLOW}.......analyzing Flows.......')
            if(pred_value[0]<0.5):
                print(f'{Fore.GREEN}Benign')
                print("\n\n")
            else:
                print("DDOS ATTACK")
            del flows_predict


            '''if(r==4):
               flow_cnt_temp=self.flows_count[newaxis,:,:]

               pred_value=predict(flow_cnt_temp)
               print("pred_value=",pred_value)

               print(f'{Fore.YELLOW}.......analyzing Flows.......')
               if(pred_value[0]<0.5):
                  print(f'{Fore.GREEN}Benign')
                  print("\n\n")
               else:
                  print("DDOS ATTACK")
               #del self.flows_count
               #gc.collect()

               self.flows_count=np.delete(self.flows_count,0,0)'''






    def garbage_collect(self, latest_time) -> None:
        keys = list(self.flows.keys())
        for k in keys:
            flow = self.flows.get(k)

            if (
                latest_time is None
                or latest_time - flow.latest_timestamp > EXPIRED_UPDATE
                or flow.duration > 60
            ):
                data = flow.get_data()







                del self.flows[k]
                return data.values()
def generate_session_class():
    return (
            FlowSession(None,False)

    )






