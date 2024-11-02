/**
 * Get data from an API endpoint
 *
 * @async
 * @param {string} path API path
 * @returns {Promise<object>} A promise that resolves with a json data object
 */
export async function query(path) {
    const response = await fetch(path, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    if (response.ok) {
        return await response.json()
    } else {
        const error = await response.json()
        throw new Error(JSON.stringify(error))
    }
}

/**
 * Send data to an API endpoint using the POST method
 *
 * @async
 * @param {string} path API path
 * @param {object} body JSON object containing the data
 * @returns {Promise<object>} A promise that resolves with a JSON object
 */
export async function mutate(path, body, method = 'POST') {
    const response = await fetch(path, {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    })
    if (response.ok) {
        return await response.json()
    } else {
        const error = await response.json()
        throw new Error(JSON.stringify(error))
    }
}
