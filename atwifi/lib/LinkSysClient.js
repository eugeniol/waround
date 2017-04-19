const denodeify = require('denodeify')
const request = denodeify(require('request'));
const _ = require('lodash');
const EventEmitter = require('events');

class LinkSysClient extends EventEmitter {
    constructor({ auth, baseUrl }) {
        super();
        this.auth = auth;
        this.baseUrl = baseUrl;

        this._currentState = []

    }

    start() {
        if (this._interval) {
            clearInterval(this._interval)
        }
        this.refreshState()
        this._interval = setInterval(() => this.refreshState(), 15000)
    }

    refreshState() {
        return this.checkState(this._currentState)
            .then(({ toAdd, toDelete, newState }) => {
                toAdd.forEach(mac => this.emit('added', { mac }))
                toDelete.forEach(mac => this.emit('removed', { mac }))
                this._currentState = newState
                return this
            }, console.error)
    }

    checkState(prevState) {
        return this.getConnections().then(conn => {
            let newState = _.map(conn, 'macAddress');
            const toDelete = _.difference(prevState, newState)
            const toAdd = _.difference(newState, prevState)

            return { toAdd, toDelete, newState }
        })
    }

    doRequest(body) {
        return request({
            method: 'POST',
            uri: this.baseUrl,
            headers: {
                'X-JNAP-Authorization': this.auth,
                'X-JNAP-Action': 'http://linksys.com/jnap/core/Transaction'
            },
            body,
            json: true
        })
    }

    get() {
        return this.doRequest([
            {
                "action": "http://linksys.com/jnap/devicelist/GetDevices",
                "request": { "sinceRevision": 0 }
            },
            {
                "action": "http://linksys.com/jnap/networkconnections/GetNetworkConnections",
                "request": {}
            }
        ])
    }

    getDevices() {
        return this
            .doRequest([{
                "action": "http://linksys.com/jnap/devicelist/GetDevices",
                "request": { "sinceRevision": 0 }
            }])
            .then(({ body:{ responses:[{ output:{ devices } }] } }) => devices)
    }

    getDeviceByMac(mac) {
        return this._devideIx && this._devideIx[mac] ? Promise.resolve(this._devideIx[mac]) : this.getDevices().then(devices => devices.find(it => it.knownMACAddresses.includes(mac)))
    }

    getConnections() {
        return this
            .doRequest([{
                "action": "http://linksys.com/jnap/networkconnections/GetNetworkConnections",
                "request": {}
            }, {
                "action": "http://linksys.com/jnap/devicelist/GetDevices",
                "request": { "sinceRevision": 0 }
            }])
            .then(({ body:{ responses:[{ output:{ connections } }, { output:{ devices } }] } }) => {
                this._devideIx = _.chain(devices)
                    .groupBy(it => it.knownMACAddresses[0])
                    .mapValues(_.first)
                    .value()

                const connectedDevs = connections.map(it => {
                    let result = Object.assign(it, {
                        device: Object.assign({}, this._devideIx[it.macAddress])
                    })
                    this._devideIx[it.macAddress].lastConnection = Object.assign({
                        timestamp: new Date()
                    }, it)

                    return result
                });

                return connectedDevs
            })
    }

}

module.exports = LinkSysClient