const API_TOKEN = process.env.API_TOKEN
const API_URL = process.env.API_URL || 'http://web:8000/api/'

const ROUTER_AUTH = 'Basic YWRtaW46QWx0YW1pcmEyNjEy';
const ROUTER_API = 'http://192.168.30.1/JNAP/';

module.exports = { API_TOKEN, API_URL, ROUTER_AUTH, ROUTER_API }