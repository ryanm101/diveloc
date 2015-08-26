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
		
	}
};