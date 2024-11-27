export const parseUrlToIpPort = (url: string): string => {
  const urlObj = new URL(url);

  const hostname = urlObj.hostname;
  const port = urlObj.port;

  const ipMatch = hostname.match(/^(\d+-\d+-\d+-\d+)/);
  if (!ipMatch) {
    throw new Error('Invalid hostname format.');
  }

  const ip = ipMatch[1].replace(/-/g, '.');

  return `${ip}:${port}`;
};
