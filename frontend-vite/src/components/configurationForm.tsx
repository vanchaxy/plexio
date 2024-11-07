import React, { FC } from "react";
import { Button } from "@/components/ui/button.tsx";
import usePlexServers from "@/hooks/usePlexServers.tsx";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectItem,
  SelectContent,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select.tsx";
import usePMSSections from "@/hooks/usePMSSections.tsx";
import { Checkbox } from "@/components/ui/checkbox.tsx";
import { Switch } from "@/components/ui/switch.tsx";
import { Avatar, AvatarImage } from "@/components/ui/avatar";
import { ThemeToggle } from "@/components/themeToggle.tsx";
import { Icons } from "@/components/icons";
import {Badge} from "@/components/ui/badge.tsx";

const transcodeDownQualities = ["1080p", "720p", "480p"];

const formSchema = z.object({
  serverName: z.string(),
  discoveryUrl: z.string(),
  streamingUrl: z.string(),
  sections: z.array(
    z.object({
      key: z.string(),
      title: z.string(),
    }),
  ),
  includeTranscodeOriginal: z.boolean(),
  includeTranscodeDown: z.boolean(),
  transcodeDownQualities: z.array(z.string()).optional(),
  includePlexTv: z.boolean(),
});

interface Props {
  plexToken: string;
  setPlexToken: (token: string | null) => void;
  plexUser: PlexUser;
}

const ConfigurationForm: FC<Props> = ({
  plexToken,
  setPlexToken,
  plexUser,
}) => {
  const servers = usePlexServers(plexToken);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      includeTranscodeOriginal: true,
      includeTranscodeDown: false,
      includePlexTv: false,
    },
  });

  const serverName = form.watch("serverName");
  const server = servers.find((s) => s.name == serverName);
  const serverConnections = server?.connections || [];

  const discoveryUrl = form.watch("discoveryUrl");
  const sections = usePMSSections(discoveryUrl, server?.accessToken || null);

  const includeTranscodeDown = form.watch("includeTranscodeDown");

  const handleLogout = () => {
    setPlexToken(null);
  };

  function onSubmit(values) {
    console.log(values);
  }

  return (
    <div className="mx-auto max-w-2xl">
      <div className="flex h-12 items-center  sm:justify-between">
        <Button variant="ghost" size="icon">
          <a href="https://github.com/vanchaxy/plexio">
            <Icons.gitHub className="h-5 w-5" />
          </a>
        </Button>
        <Button variant="ghost" size="icon">
          <a href="https://discord.gg/8RWUkebmDs">
            <Icons.discord className="h-5 w-5" />
          </a>
        </Button>
        <Button variant="ghost" size="icon">
          <a href="mailto:support@plexio.stream">
            <Icons.mail className="h-5 w-5" />
          </a>
        </Button>
        <div className="flex flex-1 items-center justify-end">
          <Avatar className="h-7 w-7">
            <AvatarImage src={plexUser.thumb} />
          </Avatar>
          <span className="m-2"> {plexUser.username} </span>

          <ThemeToggle />
          <Button onClick={handleLogout} variant="ghost" size="icon">
            <Icons.exit className="h-5 w-5" />{" "}
          </Button>
        </div>
      </div>

      {servers.length > 0 ? (
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2">
            <FormField
              control={form.control}
              name="serverName"
              render={({ field }) => (
                <FormItem className="rounded-lg border p-2">
                  <FormLabel className="text-base">Plex Server</FormLabel>
                  <Select
                    onValueChange={(s) => {
                      form.resetField("discoveryUrl", {defaultValue: ""});
                      form.resetField("streamingUrl", {defaultValue: ""});
                      form.resetField("sections", {defaultValue: []});
                      field.onChange(s)
                    }}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a server name" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {servers.map((s, index) => (
                        <SelectItem key={index} value={s.name}>
                          {s.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormDescription>Choose your Plex server.</FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            {serverName && (
              <>
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
                          {serverConnections.filter((conn) => !conn.local).length > 0 && (
                            <SelectContent>
                              {serverConnections.filter((conn) => !conn.local).map((conn, index) => (
                                <SelectItem key={index} value={conn.uri}>
                                  {conn.relay && <Badge className="mr-1.5" variant="secondary">relay</Badge>}
                                  {`${conn.address}:${conn.port}`}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          )}
                        </Select>
                        <Button className="ml-2.5" type="button">
                          Test
                        </Button>
                      </div>
                      <FormDescription>
                        Select the public URL of your Plex server.
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

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
                          {serverConnections.length > 0 && (
                            <SelectContent>
                              {serverConnections.map((conn, index) => (
                                <SelectItem key={index} value={conn.uri}>
                                  {conn.local && <Badge className="mr-1.5" variant="secondary">local</Badge>}
                                  {conn.relay && <Badge className="mr-1.5" variant="secondary">relay</Badge>}
                                  {`${conn.address}:${conn.port}`}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          )}
                        </Select>
                        <Button className="ml-2.5" type="button">
                          Test
                        </Button>
                      </div>
                      <FormDescription>
                        Select the URL of your Plex server for streaming content
                        to Stremio clients.
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </>
            )}

            {discoveryUrl && (
              <FormField
                control={form.control}
                name="sections"
                render={() => (
                  <FormItem className="rounded-lg border p-2">
                    <div className="mb-4">
                      <FormLabel className="text-base">Sections</FormLabel>
                      <FormDescription>
                        Select the Plex library sections to access in Stremio.
                      </FormDescription>
                    </div>
                    {sections.length > 0
                      ? sections.map((item) => (
                          <FormField
                            key={item.key}
                            control={form.control}
                            name="sections"
                            render={({ field }) => {
                              return (
                                <FormItem
                                  key={item.key}
                                  className="flex flex-row items-start space-x-3 space-y-0"
                                >
                                  <FormControl>
                                    <Checkbox
                                      checked={field.value?.some(
                                        (v) => v.key === item.key,
                                      )}
                                      onCheckedChange={(checked) => {
                                        return checked
                                          ? field.onChange([
                                              ...(field.value || []),
                                              {
                                                key: item.key,
                                                title: item.title,
                                              },
                                            ])
                                          : field.onChange(
                                              field.value?.filter(
                                                (value) =>
                                                  value.key !== item.key,
                                              ),
                                            );
                                      }}
                                    />
                                  </FormControl>
                                  <FormLabel className="font-normal">
                                    {item.title}
                                  </FormLabel>
                                </FormItem>
                              );
                            }}
                          />
                        ))
                      : "loading"}
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}

            <FormField
              control={form.control}
              name="includeTranscodeOriginal"
              render={({ field }) => (
                <FormItem className="items-center justify-between flex flex-row rounded-lg border p-2">
                  <div className="space-y-0.5">
                    <FormLabel className="text-base">
                      Include Transcoded Stream
                    </FormLabel>
                    <FormDescription>
                      Include a transcoded stream with original quality in HLS
                      format.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="includeTranscodeDown"
              render={({ field }) => (
                <FormItem className="items-center justify-between flex flex-row rounded-lg border p-2">
                  <div className="space-y-0.5">
                    <FormLabel className="text-base">
                      Include Transcoded Streams with Lower Resolutions
                    </FormLabel>
                    <FormDescription>
                      Include transcoded streams with lower qualities.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            {includeTranscodeDown && (
              <FormField
                control={form.control}
                name="transcodeDownQualities"
                render={() => (
                  <FormItem className="rounded-lg border p-2">
                    <div className="mb-4">
                      <FormLabel className="text-base">
                        Lower Resolutions
                      </FormLabel>
                      <FormDescription>
                        Select transcoding resolutions to include.
                      </FormDescription>
                    </div>
                    {transcodeDownQualities.map((item) => (
                      <FormField
                        key={item}
                        control={form.control}
                        name="transcodeDownQualities"
                        render={({ field }) => {
                          return (
                            <FormItem
                              key={item}
                              className="flex flex-row items-start space-x-3 space-y-0"
                            >
                              <FormControl>
                                <Checkbox
                                  checked={field.value?.includes(item)}
                                  onCheckedChange={(checked) => {
                                    return checked
                                      ? field.onChange([
                                          ...(field.value || []),
                                          item,
                                        ])
                                      : field.onChange(
                                          field.value?.filter(
                                            (value) => value !== item,
                                          ),
                                        );
                                  }}
                                />
                              </FormControl>
                              <FormLabel className="font-normal">
                                {item}
                              </FormLabel>
                            </FormItem>
                          );
                        }}
                      />
                    ))}
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}

            <FormField
              control={form.control}
              name="includePlexUrl"
              render={({ field }) => (
                <FormItem className="items-center justify-between flex flex-row rounded-lg border p-2">
                  <div className="space-y-0.5">
                    <FormLabel className="text-base">
                      Include Plex.tv URL
                    </FormLabel>
                    <FormDescription>
                      Include a stream redirecting to the Plex app or website.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
            <div className="flex items-center space-x-1 justify-center pt-3 pb-12">
              <Button className="h-11 w-10 p-2" type="button">
                <Icons.clipboard/>
              </Button>
              <Button type="submit" className="h-11 rounded-md px-8 text-xl">Install</Button>
            </div>
          </form>
        </Form>
      ) : (
        "loading"
      )}
    </div>
  );
};

export default ConfigurationForm;
