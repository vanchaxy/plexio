# Plexio: Plex Interaction for Stremio

⚠️ Plexio is an independent project and is not in any way affiliated with Plex or Stremio. ⚠️

Plexio is an addon that bridges the gap between Plex and Stremio, enabling seamless 
integration of your Plex media within the Stremio interface. With Plexio, you can discover 
and stream your Plex content directly in Stremio.

### Features
* offers both direct and transcoded streams;
* stream locally or from remote devices;
* allows searching through your Plex library;
* works with Cinemeta and other IMDB-based addons;
* handles media without IMDB matching;
* uses OAuth for safe login without sharing passwords;
* fully open-source with self-hosting support.


## Self-Hosting
If you'd prefer to self-host Plexio, you can do so easily using Docker. Follow these steps:

1. Use the following command to start a Plexio instance:
   ```bash
   docker run -d -p 7777:80 ghcr.io/vanchaxy/plexio
   ```
2. Plexio addon will be available at http://localhost:7777/.

### Optional Configuration with Environment Variables
* *CORS_ORIGIN_REGEX*: A regex pattern to define allowed CORS origins 
(default: `https?:\/\/localhost:\d+|.*plexio.stream|.*strem.io|.*stremio.com`).
* *PLEX_REQUESTS_TIMEOUT*: Timeout for Plex server requests in seconds (default: `20`).
* *CACHE_TYPE*: Defines the cache type to use `memory`/`redis` (default: `memory`).
* *REDIS_URL*: URL for a Redis instance if you use `redis` cache (default: `redis://redis:6399/0`).
* *PLEX_MATCHING_TOKEN*: Auth token for Plex media matching (default: `None`).
* *SENTRY_DSN*: DSN for error tracking with Sentry (default: `None`).
* *LOCAL_DISCOVERY*: Show local network Plex server addresses (default: `false`).

### Using addon with shared Plex server
If you are using Plexio with a Plex server that you do not own (you will see a "shared" badge 
next to the server name), you must provide the `PLEX_MATCHING_TOKEN` environment variable. 
This token is an access token from a Plex server you own, which will be used to
query the Plex API and resolve the Plex GUID using IMDB IDs.

To find your Plex authentication token, open any media on a Plex server you own.
Look for the XML data for the media and find the `X-Plex-Token` in the URL. 
Copy the token from the URL.

You can learn more about finding your authentication token in the official Plex article 
["Finding an authentication token"](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).

## Local Development
1. Fork the Repository.
2. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/plexio.git
   ```
3. Create a `.env` file and configure the required environment variables.
4. Run doker-compose:
   ```bash
   docker-compose up --build
   ```

## Contacts

For bug reports, feature requests, or general questions, join our
[Discord support forum](https://discord.gg/8RWUkebmDs).

Alternatively, you can open an issue directly in this repository.

