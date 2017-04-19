console.log(process.env)
const restify = require('restify');
const express = require('express');
const LinkSysClient = require('./lib/LinkSysClient');
const ApiHttpClient = require('./lib/ApiHttpClient');
const server = restify.createServer();

const { API_TOKEN, API_URL, ROUTER_AUTH, ROUTER_API } = require('./config')

const client = new LinkSysClient({ auth: ROUTER_AUTH, baseUrl: ROUTER_API });

const wrap = cb => (req, res, next) => cb(req, res, next).then((body => res.send(body)), next)

const MongoClient = require('mongodb').MongoClient;
const mongodb_url = 'mongodb://localhost:27017/myproject';

const dbconn = MongoClient.connect(mongodb_url);

server.get('/router/connections', wrap(() => client.getConnections()));
server.get('/router/devices/byMac/:mac', wrap(({ params:{ mac } }) => client.getDeviceByMac(mac)))

server.get('/router/devices', wrap(() => client.getDevices()));
server.get('/devices', wrap(() => dbconn.then(db => db.collection('devices').find().toArray())));

server.listen(8080, function() {
    console.log('%s listening at %s', server.name, server.url);
});

server.get(/\/public\/?.*/, restify.serveStatic({
    directory: __dirname,
    default: 'index.html',
    etag: false
}));
var ok = true

client.on('added', ({ mac }) => {
    client.getDeviceByMac(mac).then(registerDeviceAction('IN'))
})

client.on('removed', ({ mac }) => {
    client.getDeviceByMac(mac).then(registerDeviceAction('OUT'))
})

client.start()

const devicesApi = new ApiHttpClient({ url: API_URL + 'devices', token: API_TOKEN })
const devicesLogApi = new ApiHttpClient({ url: API_URL + 'devices/log', token: API_TOKEN })
const LOG_ACTIONS = {
    IN: 0,
    OUT: 1
}
function registerDeviceAction(action) {
    return (device) => {
        return devicesApi.findOrCreate({
            public_id: device.deviceID,
            friendly_name: device.friendlyName,
            mac_address: device.knownMACAddresses[0]
        }, 'public_id').then(device => {
            devicesLogApi.create({
                device: device.id, type: LOG_ACTIONS[action]
            })
        }).then(null, console.error)
    }
}
