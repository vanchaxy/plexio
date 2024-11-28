# Plexio: Plex Interaction for Stremio

⚠️ Plexio is an independent project and is not in any way affiliated with Plex or Stremio. ⚠️

Plexio is an addon that bridges the gap between Plex and Stremio, enabling seamless 
integration of your Plex media within the Stremio interface. With Plexio, you can discover 
and stream your Plex content directly in Stremio.

### Features
* feature1
* feature1
* feature1
* feature1

## Self-Hosting
If you'd prefer to self-host Plexio, you can do so easily using Docker. Follow these steps:

1. Use the following command to start a Plexio instance:
   ```bash
   docker run -d -p 7777:80 ghcr.io/vanchaxy/plexio
   ```
2. Plexio addon will be available at http://localhost:7777/.

### Optional Configuration with Environment Variables:
* CORS_ORIGIN_REGEX: A regex pattern to define allowed CORS origins 
(default: `https?:\/\/localhost:\d+|.*plexio.stream|.*strem.io|.*stremio.com`).
* PLEX_REQUESTS_TIMEOUT: Timeout for Plex server requests in seconds (default: `20`).
* CACHE_TYPE: Defines the cache type to use `memory`/`redis` (default: `memory`).
* REDIS_URL: URL for a Redis instance if you use `redis` cache (default: `redis://redis:6399/0`).
* PLEX_MATCHING_TOKEN: Auth token for Plex media matching (default: `None`).
* SENTRY_DSN: DSN for error tracking with Sentry (default: `None`).


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

