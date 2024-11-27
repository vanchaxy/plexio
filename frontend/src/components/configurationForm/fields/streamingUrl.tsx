import { FC, useState } from 'react';
import { UseFormReturn } from 'react-hook-form';
import { ConfigurationFormType } from '@/components/configurationForm/formSchema.tsx';
import { parseUrlToIpPort } from '@/components/configurationForm/utils.tsx';
import { Badge } from '@/components/ui/badge.tsx';
import { Button } from '@/components/ui/button.tsx';
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form.tsx';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select.tsx';
import { useToast } from '@/hooks/useToast';
import { isServerAliveLocal } from '@/services/PMSService.tsx';

interface Props {
  form: UseFormReturn<ConfigurationFormType>;
  server: any;
}

export const StreamingUrlField: FC<Props> = ({ form, server }) => {
  const { toast } = useToast();

  const [testInProgress, setTestInProgress] = useState(false);
  const streamingUrl = form.watch('streamingUrl');

  const testUrl = () => {
    setTestInProgress(true);
    isServerAliveLocal(streamingUrl, server.accessToken).then((alive) => {
      setTestInProgress(false);
      const ipPort = parseUrlToIpPort(streamingUrl);
      if (alive) {
        toast({
          title: 'Streaming URL Test Successful!',
          description: `Your device successfully accessed the Streaming URL at ${ipPort}.
                        Streaming will work if accessed from this device.`,
          variant: 'success',
          duration: 30 * 1000,
        });
      } else {
        toast({
          title: 'Streaming URL Test Failed!',
          description: `Your device could not access the Streaming URL at ${ipPort}. 
                        If you plan to stream from a different device, this may be expected behavior. 
                        Otherwise, please try again or select another URL. 
                        If your server is behind a firewall, consider using Plex Relay.`,
          variant: 'destructive',
          duration: 30 * 1000,
        });
      }
    });
  };

  return (
    <FormField
      control={form.control}
      name="streamingUrl"
      render={({ field }) => (
        <FormItem className="rounded-lg border p-2">
          <FormLabel className="text-base">Streaming URL</FormLabel>
          <div className="flex">
            <Select
              onValueChange={field.onChange}
              defaultValue=""
              value={field.value}
            >
              <FormControl>
                <SelectTrigger>
                  <SelectValue placeholder="Select a streaming url" />
                </SelectTrigger>
              </FormControl>
              {server.connections.length > 0 && (
                <SelectContent>
                  {server.connections.map((conn: any, index: number) => (
                    <SelectItem key={index} value={conn.uri}>
                      {conn.local && (
                        <Badge className="mr-1.5" variant="secondary">
                          local
                        </Badge>
                      )}
                      {conn.relay && (
                        <Badge className="mr-1.5" variant="secondary">
                          relay
                        </Badge>
                      )}
                      {`${conn.address}:${conn.port}`}
                    </SelectItem>
                  ))}
                </SelectContent>
              )}
            </Select>
            <Button
              className="ml-2.5 h-10 w-16"
              type="button"
              disabled={testInProgress || !streamingUrl}
              onClick={testUrl}
            >
              {testInProgress ? (
                <div className="w-5 h-5 rounded-full animate-spin border-t-2" />
              ) : (
                'Test'
              )}
            </Button>
          </div>
          <FormDescription>
            Select the URL of your Plex server for streaming content to Stremio
            clients.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
};
