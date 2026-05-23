import { defineConfig } from 'astro/config';

import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  site: 'https://nicolleweeks.ca',
  output: "hybrid",
  adapter: cloudflare()
});