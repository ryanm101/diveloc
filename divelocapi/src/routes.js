var wrecks = require('./controllers/wrecks'),
    api = require('./controllers/api');

module.exports = function (server) {
    server.get('/', api.index); //Working
    server.get('/wrecks', wrecks.getall); //Working
    server.get('/wrecks/locs', wrecks.getalllocs); //Working
    server.get('/wrecks/:wreckId', wrecks.getwreckbyid); //Working
    server.get('/wrecks/byname/:wreckName', wrecks.getwreckbyname);
    server.get('/wrecks/byloc/:wreckLoc', wrecks.getwreckbyloc);
    
    // Require API Keys & Authentication
    server.post('/wrecks', wrecks.addwreck);  //Working
    server.put('/wrecks/:wreckId', wrecks.updatewreck);  //Working
    
    // API AdminKey Only?????
    server.del('/wrecks/:wreckId', wrecks.delwreck);  //Working
};