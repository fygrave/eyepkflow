var geo = require('geoip-lite');

var config = require('./config');

var StatsD = require('node-statsd').StatsD;
var sdc = new StatsD({host: config.statsd.host, port: config.statsd.port});

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


