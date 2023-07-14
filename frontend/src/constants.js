const production = {
    url: 'https://beta.plexio.stream'
};
const development = {
    url: 'http://localhost:8000'
};
export const config = process.env.NODE_ENV === 'development' ? development : production;