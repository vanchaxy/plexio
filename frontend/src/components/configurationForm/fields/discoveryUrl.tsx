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
import { isServerAliveRemote } from '@/services/BackendService.tsx';

interface Props {
  form: UseFormReturn<ConfigurationFormType>;
  server: any;
}

export const DiscoveryUrlField: FC<Props> = ({ form, server }) => {
  const { toast } = useToast();

  const [testInProgress, setTestInProgress] = useState(false);
  const discoveryUrl = form.watch('discoveryUrl');

  const testUrl = () => {
    setTestInProgress(true);
    isServerAliveRemote(discoveryUrl, server.accessToken).then((alive) => {
      setTestInProgress(false);
      const ipPort = parseUrlToIpPort(discoveryUrl);
      if (alive) {
        toast({
          title: 'Discovery URL Test Successful!',
          description: `Plexio backend successfully accessed your server at ${ipPort}.`,
          variant: 'success',
          duration: 30 * 1000,
        });
      } else {
        toast({
          title: 'Discovery URL Test Failed!',
          description: `Plexio backend could not access your server at ${ipPort}. 
                        Please try again or select another URL. Ensure your server is accessible publicly, 
                        or consider using Plex Relay if the server is behind a firewall.`,
          variant: 'destructive',
          duration: 30 * 1000,
        });
      }
    });
  };

  return (
    <FormField
      control={form.control}
      name="discoveryUrl"
      render={({ field }) => (
        <FormItem className="rounded-lg border p-2">
          <FormLabel className="text-base">Discovery URL</FormLabel>
          <div className="flex">
            <Select
              onValueChange={field.onChange}
              defaultValue=""
              value={field.value}
            >
              <FormControl>
                <SelectTrigger>
                  <SelectValue placeholder="Select a discovery url" />
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
                      {!conn.local && !conn.relay && (
                        <Badge className="mr-1.5" variant="secondary">
                          public
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
              disabled={testInProgress || !discoveryUrl}
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
            Select the public or local URL of your Plex server.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
};
