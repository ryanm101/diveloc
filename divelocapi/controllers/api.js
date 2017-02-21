module.exports = {
    index: function(req, res, next) {
        res.send("API Documentation Goes here");
        return next();
    }
};
