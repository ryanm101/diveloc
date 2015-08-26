
module.exports = {
    getall: function(req, res, next) {
        console.log("Get all Wrecks");
        req.db.list({ }, function(err, body) {
            if (err) {
                console.log(err);
                return res.send(err.statusCode, err.reason);
            }
            res.send(body)
        });
        return next();
    },
    getalllocs: function (req, res, next) {
        console.log("Get all Wreck Locations");
        req.db.view('GPS', 'DecimalGPS', function(err, body) {
            if (err) {
                console.log(err);
                return res.send(err.statusCode, err.reason);
            }
            res.send(body)
        });
        return next();
    },
    getwreckbyid: function(req, res, next) {
        console.log("Get Wreck by ID");
        req.db.get(req.params.wreckId, { }, function(err, body) {
            if (err) {
                console.log(err);
                return res.send(err.statusCode, err.reason);
            }
            res.send(body)
        });
        return next();
    },
    getwreckbyname: function(req, res, next) {
        res.send("Get Wreck by Name");
        return next();
    },
    getwreckbyloc: function(req, res, next) {
        res.send("Get Wreck by Loc");
        return next();
    },
    addwreck: function(req, res, next) {
        console.log("Add Wreck");
        req.db.insert(req.body, req.body.Name, function (error, body, headers) {
            if(error) { 
                console.log(error['status-code']  + ": " + error.message);
                console.log(body);
                if (error.message == "Document update conflict.") {
                    return res.send(409, error.message); 
                }
                return res.send(500 , error['status-code'] + ": " + error.message); 
            }
            res.send(201, body);
        });
        return next();
    },
    updatewreck: function(req, res, next) {
        console.log("Update Wreck");
        req.db.update(req.body, req.params.wreckId, function (error, response) {
            if(error) { 
                console.log("No Update");
                return res.send(520 , "No Update"); 
            }
            res.send(201, response);
        });
        return next();
    },
    delwreck: function(req, res, next) {
        console.log("Delete Wreck");
        req.db.get(req.params.wreckId, { }, function(err, body) {
            if (err) {
                console.log(err);
                return res.send(err.statusCode, err.reason);
            }
            req.db.destroy(req.params.wreckId, body._rev, function(err, body) {
                if (err) {
                    console.log(err);
                    return res.send(err.statusCode, err.reason);
                }
                res.send(200);
            });
        });
        return next();
    } 
};