var geo = require('geoip-lite');

var config = require('./config');

var StatsD = require('node-statsd').StatsD;
var sdc = new StatsD({host: config.statsd.host, port: config.statsd.port});
//{"header":{"version":5,"count":20,"sys_uptime":1048580997,"unix_secs":1371202904,"unix_nsecs":101000,"flow_sequence":97,"engine_type":0,"engine_id":0,"sampling_interval":0},"v5Flows":[{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515400,"last":1048515400,"srcport":56482,"dstport":4005,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515487,"last":1048515487,"srcport":3052,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515390,"last":1048515390,"srcport":3971,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515400,"last":1048515400,"srcport":4005,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515389,"last":1048515389,"srcport":56482,"dstport":3971,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515461,"last":1048515461,"srcport":56482,"dstport":24800,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515395,"last":1048515395,"srcport":2007,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048514367,"last":1048514367,"srcport":4126,"dstport":56481,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515410,"last":1048515410,"srcport":56482,"dstport":3995,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515395,"last":1048515395,"srcport":56482,"dstport":2007,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515379,"last":1048515379,"srcport":56482,"dstport":3372,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515456,"last":1048515456,"srcport":2047,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515410,"last":1048515410,"srcport":3995,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515477,"last":1048515477,"srcport":56482,"dstport":3325,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515384,"last":1048515384,"srcport":1051,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515446,"last":1048515446,"srcport":2003,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515451,"last":1048515451,"srcport":56482,"dstport":2602,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515405,"last":1048515405,"srcport":8084,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[140,109,17,116],"dstaddr":[210,59,245,124],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":44,"first":1048515415,"last":1048515415,"srcport":56482,"dstport":1066,"pad1":0,"tcp_flags":2,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0},{"srcaddr":[210,59,245,124],"dstaddr":[140,109,17,116],"nexthop":[0,0,0,0],"input":0,"output":0,"dPkts":1,"dOctets":40,"first":1048515492,"last":1048515492,"srcport":1062,"dstport":56482,"pad1":0,"tcp_flags":20,"prot":6,"tos":0,"src_as":0,"dst_as":0,"src_mask":0,"dst_mask":0}]}

function getprotoent(proto) {
	var prots = {};
	prots[0] = "IP";
	prots[1] = "ICMP";
	prots[6] = "TCP";
	prots[17] = "UDP";
	prots[47] = "GRE";
	if (proto in prots) {
		return prots[proto];
	} else { return "other"; }

}

function logIP(addr, item) {
	v = addr[0] + "." + addr[1] + "." + addr[2] + "." + addr[3];
	console.log(v);
	g = geo.lookup(v);
	if (g != null) {
	sdc.increment('src.country.' + g.country, item.dPkts);
	sdc.increment('src.region.' + g.region, item.dPkts);
	sdc.increment('src.city.' + g.city, item.dPkts);
	sdc.increment('srcbytes.country.' + g.country, item.dOctets);
	sdc.increment('srcbytes.region.' + g.region, item.dOctets);
	sdc.increment('srcbytes.city.' + g.city, item.dOctets);
	}


}

var Collector=require("Netflow");
var x = new Collector(function (err) {
    if(err != null) {
        console.log("ERROR ERROR \n"+err);
    }
})
.on("listening",function() { console.log("listening"); } )
.on("packet",function(packet) { console.log("packet"); 
	packet.v5Flows.forEach(function(item) {
		console.log("packs " + item.dPkts);

		sdc.increment('flow.packets.total', item.dPkts);
		sdc.increment('flow.bytes.total', item.dOctets);
		sdc.increment('flow.packets.' + getprotoent(item.prot), item.dPkts);
		sdc.increment('flow.bytes.' + getprotoent(item.prot), item.dOctets);
//		sdc.increment('flowsport.packets.' + item.srcport, item.dPkts);
//		sdc.increment('flowsport.bytes.' + item.srcport, item.dOctets);
//		sdc.increment('flowdport.packets.' + item.dstport, item.dPkts);
//		sdc.increment('flowdport.bytes.' + item.dstport, item.dOctets);
		logIP(item.srcaddr, item);
		logIP(item.dstaddr, item);

	});

 } )
.listen(3003);



process.on('uncaughtException', function(err) {
  console.log("Uncaught Error " + err);
});


