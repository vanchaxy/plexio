import { FC } from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { encode as base64_encode } from 'js-base64';
import { useForm } from 'react-hook-form';
import { v4 as uuidv4 } from 'uuid';
import {
  DiscoveryUrlField,
  IncludeTranscodeOriginalField,
  SectionsField,
  ServerNameField,
  StreamingUrlField,
  IncludeTranscodeDownFields,
  IncludePlexTvField,
} from '@/components/configurationForm/fields';
import {
  formSchema,
  ConfigurationFormType,
} from '@/components/configurationForm/formSchema.tsx';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button.tsx';
import { Form } from '@/components/ui/form';
import usePMSSections from '@/hooks/usePMSSections.tsx';

interface Props {
  servers: PlexServer[];
}

const ConfigurationForm: FC<Props> = ({ servers }) => {
  const form = useForm<ConfigurationFormType>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      includeTranscodeOriginal: true,
      includeTranscodeDown: false,
      includePlexTv: false,
    },
  });

  const serverName = form.watch('serverName');
  const server = servers.find((s) => s.name == serverName);

  const discoveryUrl = form.watch('discoveryUrl');
  const sections = usePMSSections(discoveryUrl, server?.accessToken || null);

  function onSubmit(configuration: any, event: any) {
    configuration.version = '0.0.1';
    configuration.accessToken = server?.accessToken;
    configuration.sections = configuration.sections.filter((item: any) =>
      sections.find((s) => s.key === item.key),
    );

    const encodedConfiguration = base64_encode(JSON.stringify(configuration));
    const addonUrl = `${window.location.origin}/${uuidv4()}/${encodedConfiguration}/manifest.json`;

    if (event.nativeEvent.submitter.name === 'clipboard') {
      navigator.clipboard.writeText(addonUrl);
    } else {
      window.location.href = addonUrl.replace(/https?:\/\//, 'stremio://');
    }
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-2 p-2 rounded-lg border"
      >
        <ServerNameField form={form} servers={servers} />
        {server && (
          <>
            <DiscoveryUrlField form={form} server={server} />
            <StreamingUrlField form={form} server={server} />
          </>
        )}
        {discoveryUrl && (
          <SectionsField form={form} sections={sections}></SectionsField>
        )}
        <IncludeTranscodeOriginalField form={form} />
        <IncludeTranscodeDownFields form={form} />
        <IncludePlexTvField form={form} />

        <div className="flex items-center space-x-1 justify-center p-3">
          <Button className="h-11 w-10 p-2" type="submit" name="clipboard">
            <Icons.clipboard />
          </Button>
          <Button
            className="h-11 rounded-md px-8 text-xl"
            type="submit"
            name="install"
          >
            Install
          </Button>
        </div>
      </form>
    </Form>
  );
};

export default ConfigurationForm;
