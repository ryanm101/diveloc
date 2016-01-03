//Decimal value = Degrees + (Minutes/60) + (Seconds/3600)
//degrees minutes seconds: 40° 26′ 46″ N 79° 58′ 56″ W
//degrees decimal minutes: 40° 26.767′ N 79° 58.933′ W
//decimal degrees: 40.446° N 79.982° W

module.exports = {
	HMtoDec: function (strHM) {
		var re1 = /^(\d+)\.(\d+)\.(\d+)\s*(\w+)/i;
		var re2 = /^(\d+\.?\d*)\s(\d{2,}\.?\d*)?\s?(\d{2,}\s*\d*)?\s*(\w+)/i;
		var arrRes = re1.exec(strHM)
		if (arrRes) {
			console.log("re1: "+strHM);
		} else {
			console.log("re2?: "+strHM);
			arrRes = re2.exec(strHM)
			if (arrRes) {
				console.log("re2*: "+strHM);
			}
		}
		
	},
	DECtoHM: function (strDEC) {
		
	},
	DistBetweenGPSPoints: function (latA,lonA,latB,lonB) {
		var R = 6371000; // metres
		var la1 = latA.toRadians();
		var la2 = latB.toRadians();
		var latdiff = (latB-latA).toRadians();
		var londiff = (lonB-lonA).toRadians();

		var a = Math.sin(latdiffΔφ/2) * Math.sin(latdiff/2) +
		        Math.cos(la1) * Math.cos(la2) *
		        Math.sin(londiff/2) * Math.sin(londiff/2);
		var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

		var d = R * c;
		return d;
	}
};