import { z } from 'zod';

export const formSchema = z.object({
  serverName: z.string(),
  discoveryUrl: z.string(),
  streamingUrl: z.string(),
  sections: z
    .array(
      z.object({
        key: z.string(),
        title: z.string(),
        type: z.string(),
      }),
    ),
  includeTranscodeOriginal: z.boolean(),
  includeTranscodeDown: z.boolean(),
  transcodeDownQualities: z.array(z.string()).optional(),
  includePlexTv: z.boolean(),
});

export type ConfigurationFormType = z.infer<typeof formSchema>;
