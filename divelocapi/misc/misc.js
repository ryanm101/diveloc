//Decimal value = Degrees + (Minutes/60) + (Seconds/3600)
//degrees minutes seconds: 40° 26′ 46″ N 79° 58′ 56″ W
//degrees decimal minutes: 40° 26.767′ N 79° 58.933′ W
//decimal degrees: 40.446° N 79.982° W
//There are 60 minutes in a degree and 60 seconds in a minute. Then to convert from a degrees minutes seconds format to a decimal degrees format, one may use the formula

// {decimal degrees} = {degrees} + {minutes}/60 + {seconds}/3600.
//To convert back from decimal degree format to degrees minutes seconds format,

//  {degrees} = {decimal degrees}
//  {minutes} = 60*({decimal degrees} - {degrees})
//  {seconds} = 3600*({decimal degrees} - {degrees} - {minutes}/60)

// https://en.wikipedia.org/wiki/Geographic_coordinate_conversion
module.exports = {
    ParseDMS: function(input) {
        var parts = input.split(/[^\d\w]+/);
        var lat = ConvertDMSToDD(parts[0], parts[1], parts[2], parts[3]);
        var lng = ConvertDMSToDD(parts[4], parts[5], parts[6], parts[7]);
    },
    ConvertDMSToDD: function(degrees, minutes, seconds, direction) {
        var dd = degrees + minutes/60 + seconds/(60*60);

        if (direction == "S" || direction == "W") {
            dd = dd * -1;
        } // Don't do anything for N or E
        return dd;
    },
    ConvertDDToDMS: function(lat,lng) {

    },
    HMtoDec: function (strHM) {
		var re1 = /^(\d+)\.(\d+)\.(\d+)\s*(\w+)/i;
		var re2 = /^(\d+\.?\d*)\s(\d{2,}\.?\d*)?\s?(\d{2,}\s*\d*)?\s*(\w+)/i;
		var arrRes = re1.exec(strHM);
		if (arrRes) {
			console.log("re1: "+strHM);
		} else {
			console.log("re2?: "+strHM);
			arrRes = re2.exec(strHM);
			if (arrRes) {
				console.log("re2*: "+strHM);
			}
		}

	},
};
