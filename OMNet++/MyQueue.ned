package inet.networklayer.diffserv;

import inet.queueing.queue.PacketQueue;
import inet.queueing.queue.CompoundPacketQueueBase;
import inet.queueing.queue.DropTailQueue;
import inet.queueing.scheduler.PriorityScheduler;
import inet.queueing.scheduler.WrrScheduler;
import inet.queueing.contract.IPacketClassifier;
import inet.queueing.classifier.PriorityClassifier;
import inet.queueing.classifier.WrrClassifier;
import inet.queueing.common.PacketDelayer;
import inet.queueing.contract.IPacketClassifier;

import inet.queueing.base.PacketClassifierBase;
import inet.queueing.contract.IPacketClassifier;

module GenericClassifier extends PacketClassifierBase like IPacketClassifier{
    parameters:
        @class(GenericClassifier);
        @display("i=block/classifier");
}

module MyQueue extends CompoundPacketQueueBase
{

    submodules:
        classifier: <default("GenericClassifier")> like IPacketClassifier {
            parameters:
                @display("p=100,200");
        }
        a: PacketDelayer {
            delay = 0ms;
        }

        queue1: DropTailQueue {
            @display("p=250,100");
        }
      
        queue2: DropTailQueue {
            @display("p=250,200");
        }
        queue3: DropTailQueue {
            @display("p=250,200");
        }
        wrr: WrrScheduler {
            weights = "1 1 1"; // Assign equal weights to all queues
            @display("p=400,150");
        }
       
    connections:
        in --> classifier.in;
        classifier.out++ --> queue1.in;
		classifier.out++ -->  queue2.in;
		classifier.out++ --> a.in;
        a.out --> queue3.in;
        queue1.out -->  wrr.in++;
        queue2.out --> wrr.in++;
        queue3.out --> wrr.in++;
        wrr.out --> out;
}