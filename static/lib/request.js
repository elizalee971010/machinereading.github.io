var Host = 'http://127.0.0.1:5000'

function req(url, data, method) {
    if (method === 'GET') {
        return axios.get(Host + url, {
            params: data
        })
    } else if (method === 'POST') {
        return axios.post(Host + url, data)
    }
}


//浏览接口
function SendKy(data) {
    return req('/push', data, 'GET')
}


