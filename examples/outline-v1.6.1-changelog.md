# Changelog - Outline v1.6.1 validation

**Requested Date Range:** 2026-03-15 to 2026-03-18
**Commit Date Range:** 2026-03-15 to 2026-03-18
**Repository:** [outline/outline](https://github.com/outline/outline)

**Total Commits:** 21

## Features

- Adds API key authentication for MCP server (#11798) ([f8098ab](https://github.com/outline/outline/commit/f8098ab46482be60ba8468a72a0c5bafb73bb1b0)) - Tom Moor (2026-03-18)
- Expose moving documents within a collection (#11799) ([3740e09](https://github.com/outline/outline/commit/3740e09e5cafcc65e58cb13f52bb334d24d2315f)) - Tom Moor (2026-03-18)

## Bug Fixes

- guard against concurrent restore in documentPermanentDeleter (#11775) ([64dc5e8](https://github.com/outline/outline/commit/64dc5e8ea7e1ad03d1d27eff9dec46e8c3819d96)) - Igor Loskutov (2026-03-18)
- restore image upload (#11803) ([07099bb](https://github.com/outline/outline/commit/07099bb4f6d777826b98fc0d443bedeede78ba78)) - Apoorv Mishra (2026-03-18)
- Clicking on templates in settings table does nothing ([4673ff0](https://github.com/outline/outline/commit/4673ff084043f71cd5d6683cb4f148f3a1b15700)) - Tom Moor (2026-03-18)
- Preserve port in OAuth metadata URLs when self-hosted behind a reverse proxy (#11791) ([85072da](https://github.com/outline/outline/commit/85072dab9283df0c3ef5f67230958fe590650ebf)) - Copilot (2026-03-17)
- Support mailbox format for SMTP_FROM_EMAIL and SMTP_REPLY_EMAIL (#11784) ([1e8d9b5](https://github.com/outline/outline/commit/1e8d9b5f803904c587b6ab88cfc7c925b16050ff)) - Copilot (2026-03-17)
- Page hang with corrupted PNG upload (#11783) ([6138777](https://github.com/outline/outline/commit/613877714b345edb1806e95ba053edb53a65cc49)) - Tom Moor (2026-03-17)
- Race condition when editing title while doc is saving (#11764) ([a9401c9](https://github.com/outline/outline/commit/a9401c9bb69df527f924419ca92274aac2074a52)) - Tom Moor (2026-03-15)

## Maintenance

- chore: Cleanup working tables left in db if midrun abort (#11786) ([62cfd4e](https://github.com/outline/outline/commit/62cfd4e9bc07e85892cb960c980985bf958f2e47)) - Tom Moor (2026-03-17)

## Other

- v1.6.1 ([05eac5b](https://github.com/outline/outline/commit/05eac5bc3ba7d2d2ecb26c1783cd8b86d3fd408d)) - Tom Moor (2026-03-18)
- Add "Create a nested doc" to @mention (#11800) ([f03ac1f](https://github.com/outline/outline/commit/f03ac1f8deeca03a597dd80c91c532da589b45c0)) - Tom Moor (2026-03-18)
- Support GitLab `work_items` URL structure in unfurl integration (#11795) ([500c3f9](https://github.com/outline/outline/commit/500c3f91b0703ebe156d7edfd0f6d7e230a0f476)) - Copilot (2026-03-18)
- Apply full width to print layout (#11768) ([cc1c4b2](https://github.com/outline/outline/commit/cc1c4b22d44ffbb3384eb2ba3f3f6db6e69c13cd)) - wmTJc9IK0Q (2026-03-16)
- chore: Compressed inefficient images automatically (#11763) ([1345471](https://github.com/outline/outline/commit/1345471338633d5cc4a3975293b31f0080d2f56c)) - github-actions[bot] (2026-03-15)
- Add maskable and monochrome icon variants (#11762) ([0ddddac](https://github.com/outline/outline/commit/0ddddac9c93766dc931b1d4fd78b87f9cbf7eb72)) - Tom Moor (2026-03-15)
- v1.6.0 ([2495420](https://github.com/outline/outline/commit/24954204eac2447b648d4e56813f69205ee4b873)) - Tom Moor (2026-03-15)
- Group sync framework (#11684) ([1a893b0](https://github.com/outline/outline/commit/1a893b0e459414630415003ee7b9d1cf9cc5ae6d)) - Tom Moor (2026-03-15)
- New Crowdin updates (#11688) ([255efe9](https://github.com/outline/outline/commit/255efe98441301ce32f8fd830399c1b6da415bfd)) - Translate-O-Tron (2026-03-15)
- Move toggle container up in block menu ([20e5514](https://github.com/outline/outline/commit/20e55141deea536fc9e7e9c734331659237343d0)) - Tom Moor (2026-03-15)
- Add flags to Team model to match User (#11758) ([9940f48](https://github.com/outline/outline/commit/9940f48efa2bec89af4e6b29244af618e378a1fa)) - Tom Moor (2026-03-15)
