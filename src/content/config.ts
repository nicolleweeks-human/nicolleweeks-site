import { defineCollection, z } from 'astro:content';

const baseSchema = z.object({
  title: z.string(),
  pubDate: z.coerce.date().optional(),
  description: z.string().optional(),
  heroImage: z.string().optional(),
  originalUrl: z.string().optional(),
});

const writing = defineCollection({ type: 'content', schema: baseSchema });
const work = defineCollection({ type: 'content', schema: baseSchema });

export const collections = { writing, work };
