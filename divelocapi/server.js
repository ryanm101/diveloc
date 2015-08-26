var restify = require('restify')
    , config = require('./configure')
    , nano    = require('nano')('http://' + config.dbserver + ':' + config.dbport)
    , db      = nano.use(config.dbname);
    
//var misc = require('./public/app/misc');

//Decimal value = Degrees + (Minutes/60) + (Seconds/3600)
//degrees minutes seconds: 40° 26′ 46″ N 79° 58′ 56″ W
//degrees decimal minutes: 40° 26.767′ N 79° 58.933′ W
//decimal degrees: 40.446° N 79.982° W
//misc.ToDecLongLat("40.446° N", "XXX");

nano.db.create(config.dbname);

var server = restify.createServer({
  name: 'divelocapi'
});

// extend Nano with Update ability
db.update = function(obj, key, callback) {
    var db = this;
    db.get(key, function (error, existing) { 
        if(!error) obj._rev = existing._rev;
        db.insert(obj, key, callback);
    });
};

db.insert(
		{ "views": 
			{ "DecimalGPS": { 
				"map": function(doc) {
						if(doc.DecLatitude && doc.DecLongitude)
							emit(doc.Name, [doc.DecLatitude, doc.DecLongitude, doc.GPSApprox]);
					} 
				},
			  "NoGPS": { 
				"map": function(doc) {
						if(!doc.DecLatitude && !doc.DecLongitude)
							emit(doc.Name, null);
					} 
				}
			}	
		}, '_design/GPS', function (error, response) {
			console.log("Created GPS View");
		}
);

server.use(restify.queryParser());
server.use(restify.bodyParser());
server.use(restify.CORS());
server.use(function (req, res, next) {
    req.nano = nano;
    req.db = db;
    next();
});

require('./routes')(server);

server.listen(config.port, function () {
  console.log('%s listening at %s', server.name, server.url);
});