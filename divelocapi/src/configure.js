if (process.env.DB_PORT_5984_TCP_ADDR && process.env.DB_PORT_5984_TCP_PORT) {
    var dbport = `${process.env.DB_PORT_5984_TCP_PORT}`;
    var dbaddr = `${process.env.DB_PORT_5984_TCP_ADDR}`;
} else {
    var dbport = '5984';
    var dbaddr = 'db';
}

var config = {
    ip_addr: '0.0.0.0',
    port: '3000',
    dbname: 'diveloc',
    dbport: dbport,
    dbserver: dbaddr,
    dbuser: '',
    dbpass: ''
};

module.exports = config;
