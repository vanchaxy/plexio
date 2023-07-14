import './App.css';
import React, {useEffect, useState} from 'react';
import {encode as base64_encode} from 'base-64';
import {v4 as uuidv4} from 'uuid';


function App() {
    const [plexServersList, setPlexServersList] = useState([]);
    const [plexServer, setPlexServer] = useState(null);
    const [discoveryUrl, setDiscoveryUrl] = useState(null);
    const [streamingUrl, setStreamingUrl] = useState(null);
    const [user, setUser] = useState(null);

    const [discoveryUrlOptions, setDiscoveryUrlOptions] = useState([]);
    const [streamingUrlOptions, setStreamingUrlOptions] = useState([]);

    const [discoveryTestResult, setDiscoveryTestResult] = useState('Not started');
    const [streamingTestResult, setStreamingTestResult] = useState('Not started');

    const handlePlexServerSelect = event => {
        const {value} = event.target;
        for (let server of plexServersList) {
            if (server.name === value) {
                handlePlexServerSet(server);
            }
        }
    };

    const handlePlexServerSet = server => {
        setPlexServer(server);
        setDiscoveryUrlOptions(server.connections.filter(c => !c.local));
        setStreamingUrlOptions(server.connections);
    };

    const handleUserSet = user => {
        setUser(user);

        fetch(`/api/v1/get-plex-servers`, {credentials: 'include'})
            .then(response => response.json())
            .then(data => setPlexServersList(data))
            .catch(error => console.error('Error fetching servers:', error));
    };

    useEffect(() => {
        fetch(`/api/v1/get-plex-user`, {credentials: "include"})
            .then(response => {
                switch (response.status) {
                    case 200:
                        return response.json()
                    case 403:
                        window.location = `/api/v1/login?origin_url=${window.location}`
                        break
                    default:
                        console.error('Unexpected status:', response.status)
                }
            })
            .then(data => handleUserSet(data))
            .catch(error => console.error('Error fetching user:', error));
    }, []);

    const handleSubmit = event => {
        event.preventDefault();
        const configuration = {
            accessToken: plexServer.accessToken,
            discoveryUrl: discoveryUrl,
            streamingUrl: streamingUrl,
            serverName: plexServer.name,
            installationId: uuidv4(),
        }
        const encoded_configuration = base64_encode(JSON.stringify(configuration));
        let addon_url = `/` + encoded_configuration + '/manifest.json';
        navigator.clipboard.writeText(addon_url);
        window.location = addon_url.replace(/https?:\/\//, "stremio://");
    };

    const handleDiscoveryTest = (event) => {
        event.preventDefault();
        setDiscoveryTestResult('Testing...')
        fetch(`/api/v1/test-connection?` + new URLSearchParams({
            url: discoveryUrl,
            token: plexServer.accessToken,
        }))
            .then(response => {
                switch (response.status) {
                    case 200:
                        return response;
                    default:
                        setDiscoveryTestResult('Failed!')
                }
            })
            .then(response => response.json())
            .then(data => {
                setDiscoveryTestResult(data.success ? 'Success!' : 'Failed!')
            })
            .catch(error => setDiscoveryTestResult('Failed!'));
    }

    const handleStreamingTest = (event) => {
        event.preventDefault();
        setStreamingTestResult('Testing...')
        fetch(streamingUrl + '?X-Plex-Token=' + plexServer.accessToken)
            .then(response => {
                switch (response.status) {
                    case 200:
                        setStreamingTestResult('Success!')
                        break
                    default:
                        setStreamingTestResult('Failed!')
                }
            })
            .catch(error => setStreamingTestResult('Failed!'));
    }

    const logout = () => {
        fetch(`/api/v1/logout`, {credentials: 'include'})
            .then(r => window.location.reload())
            .catch(error => console.error('Error fetching servers:', error));
    }

    if (!user) {
        return (
            <div className="container">
                Loading...
            </div>
        )
    }
    return (
        <div className="container">
            <div className="user-info">
                <div className="user-details">
                    <div className="user-avatar">
                        <img src={user.thumb} alt="Avatar" className="avatar"/>
                    </div>
                    <h2 className="user-name">{user.username}</h2>
                </div>
                <button className="logout-btn" onClick={logout}>Logout</button>
            </div>

            <form className="configuration-form" onSubmit={handleSubmit}>
                <h3>Configuration Settings</h3>
                <div className="select-field">
                    <div className="label-row">
                        <label htmlFor="server-select">Server:</label>
                    </div>
                    <div className="selector-row">
                        <select value={plexServer?.name} onChange={handlePlexServerSelect} id="server-select">
                            <option/>
                            {plexServersList.map(option => (
                                <option key={option.name} value={option.name}>
                                    {option.name}
                                </option>
                            ))}

                        </select>
                    </div>
                </div>

                <div className="select-field">
                    <div className="label-row">
                        <label htmlFor="discovery-url-select">Discovery URL:</label>
                    </div>
                    <div className="selector-row">
                        <select id="discovery-url-select" onChange={event => setDiscoveryUrl(event.target.value)}>
                            <option/>
                            {discoveryUrlOptions.map(option => (
                                <option
                                    key={option.uri}
                                    value={option.uri}
                                >
                                    {option.relay ? '[relay] ' : ''}
                                    {option.address}
                                </option>
                            ))}
                        </select>
                        <button type="button" className="test-btn" onClick={handleDiscoveryTest}>Test</button>
                    </div>
                    <div className="test-result-row">
                        <span className="test-result"
                        >Test Result: {discoveryTestResult}</span>
                    </div>
                </div>

                <div className="select-field">
                    <div className="label-row">
                        <label htmlFor="stream-url-select">Stream URL:</label>
                    </div>
                    <div className="selector-row">
                        <select
                            id="stream-url-select"
                            onChange={event => setStreamingUrl(event.target.value)}>
                            <option/>
                            {streamingUrlOptions.map(option => (
                                <option
                                    key={option.uri}
                                    value={option.uri}
                                >
                                    {option.relay ? '[relay] ' : ''}
                                    {option.local ? '[local] ' : ''}
                                    {option.address}
                                </option>
                            ))}
                        </select>
                        <button type="button" className="test-btn" onClick={handleStreamingTest}>Test</button>
                    </div>
                    <div className="test-result-row">
                        <span className="test-result"
                        >Test Result: {streamingTestResult}</span>
                    </div>
                </div>

                <div className="button-group">
                    <button className="install-btn" type="submit">Install</button>
                </div>
            </form>
        </div>
    );
}

export default App;
