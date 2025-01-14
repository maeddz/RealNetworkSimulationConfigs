#include "inet/common/clock/ClockUserModuleMixin.h"
#include "inet/queueing/base/PacketClassifierBase.h"
#include "inet/linklayer/ethernet/common/EthernetMacHeader_m.h"
#include "inet/networklayer/common/L3AddressTag_m.h"
#include "inet/networklayer/ipv4/Ipv4Header_m.h"
#include <iostream>
#include "inet/common/PacketEventTag.h"
#include "inet/common/TimeTag.h"
#include "inet/common/IProtocolRegistrationListener.h"
#include "inet/queueing/base/PacketPusherBase.h"
#include "inet/common/ModuleAccess.h"

namespace inet {
    class GenericClassifier : public queueing::PacketClassifierBase {
        private:
        int numApps = 0;
        public:
            virtual int classifyPacket(Packet *packet) override;
    };
    Register_Class(GenericClassifier);
    int GenericClassifier::classifyPacket(Packet *packet){
        EV_INFO << "Pushing packet" << EV_FIELD(packet) << EV_ENDL;

        auto ethHeader = packet->popAtFront<EthernetMacHeader>();
        auto ipvHeader = packet->popAtFront();
        int queueNumber = 0;
        if (std::strstr(ipvHeader->getClassName(), "Ipv4Header")){
            packet->insertAtFront(ipvHeader);
            auto iph = packet->popAtFront<Ipv4Header>();
            if (iph->getSrcAddress().str() == "192.168.1.1"){
            if (iph->getDestAddress().str() == "192.168.3.1"){
                queueNumber = 0;
            }
            else if (iph->getDestAddress().str() == "192.168.2.2"){
                queueNumber = 1;

            }  else {
                queueNumber = 2;

            }} else if (iph->getSrcAddress().str() == "192.168.4.1"){
                if (iph->getDestAddress().str() == "192.168.3.1"){
                    queueNumber = 0;
                 }
                 else if (iph->getDestAddress().str() == "192.168.2.2"){
                      queueNumber = 1;
            }  else {
                queueNumber = 2;

            }
            }
           
        }
        packet->insertAtFront(ipvHeader);
        packet->insertAtFront(ethHeader);
//#ifdef INET_WITH_CLOCK
//
//        auto clockEvent = new ClockEvent("DelayTimer");
//        clocktime_t delay = 0;
//        clockEvent->setContextPointer(packet);
//        scheduleClockEventAfter(delay, clockEvent);
//#else
//    {
//#endif
//        simtime_t delay = 0;
//        EV_INFO << "Delaying packet" << EV_FIELD(delay) << EV_FIELD(packet) << EV_ENDL;
//        scheduleAfter(delay, packet);
//    }
        return queueNumber;
    }
}
