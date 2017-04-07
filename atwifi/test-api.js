const ApiHttpClient = require('./lib/ApiHttpClient')

const { API_TOKEN, API_URL } = require('./config')

var apiClient = new ApiHttpClient({ url: API_URL + 'devices', token: API_TOKEN })

const data = {
    public_id: 'xxdxx',
    friendly_name: 'dfskhod',
    mac_address: 'afasfd'
};

apiClient.findOrCreate(data, 'public_id').then(console.log, console.error)

