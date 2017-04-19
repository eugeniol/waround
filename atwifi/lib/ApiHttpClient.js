const request = require('request-promise');
const _ = require('lodash');

class ApiHttpClient {
    constructor({ url, token }) {
        this.url = url;
        this.token = token

    }

    doRequest(opts) {
        return request(Object.assign({
            uri: this.url + '/',
            headers: {
                'Authorization': 'Token ' + this.token,
                'Content-Type': 'application/json'
            },
            json: true // Automatically stringifies the body to JSON
        }, opts))
    }

    create(body) {
        return this.doRequest({ method: 'POST', body })
    }

    findOne(qs) {
        return this.doRequest({ method: 'GET', qs }).then(rs => rs.results[0])
    }

    findOrCreate(body, filter = body) {
        if (_.isString(filter))
            filter = _.pick(body, filter)
        return this.findOne(filter).then(rs => rs ? this.update(Object.assign(rs, body)) : this.create(body))
    }

    update(body) {
        return this.doRequest({
            uri: this.url + '/' + body.id + '/',
            method: 'PUT',
            body
        })
    }
}

module.exports = ApiHttpClient