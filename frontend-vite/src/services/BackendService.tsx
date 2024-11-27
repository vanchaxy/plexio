import axios from 'axios';

const BACKEND_API_URL = 'http://localhost/api/v1';

export const isServerAliveRemote = async (serverUrl: string, token: string) => {
  try {
    const response = await axios.get(`${BACKEND_API_URL}/test-connection`, {
      timeout: 25000,
      params: {
        url: serverUrl,
        token: token,
      },
    });
    return response.data?.success;
  } catch (error) {
    console.error('Error while ping PMS remote:', error);
    return false;
  }
};
