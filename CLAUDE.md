# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Next.js 15 documentation site for PostgreSQL Extensions, built with Fumadocs. The site serves as a comprehensive catalog of PostgreSQL extensions with multilingual support (English/Chinese) and advanced search capabilities.

## Development Commands

### Core Commands
- `make dev` or `npm run dev` - Start development server (port 3000) with Turbo
- `make build` or `npm run build` - Build the site for production
- `make view` - Open browser to localhost:3000
- `make clean` - Remove build output directory (`out/`)

### Package Management
- `make install` or `pnpm install` - Install dependencies
- `make update` or `pnpm update` - Update dependencies to latest versions

### Data Management
- `make save` or `make dump` - Export PostgreSQL extension data to CSV files in `data/` directory
- `make load` - Import extension data from CSV files back to PostgreSQL

## Architecture Overview

### Tech Stack
- **Framework**: Next.js 15 with React 19
- **Documentation**: Fumadocs with MDX support
- **Styling**: Tailwind CSS v4
- **Search**: Orama with Chinese tokenizer support
- **Database**: PostgreSQL (extension metadata storage)
- **Language**: TypeScript

### Key Directories
- `app/` - Next.js App Router structure with internationalization
- `content/docs/` - MDX documentation files for extensions
- `content/stub/` - Stub files for incomplete extension docs
- `lib/` - Core utilities (i18n, source configuration)
- `data/` - CSV data files for extension metadata
- `components/` - Reusable React components
- `bin/` - CLI tools and scripts

### Data Flow
1. Extension metadata stored in PostgreSQL (`ext` schema)
2. Data exported to CSV files in `data/` directory via Makefile
3. MDX files in `content/docs/ext/` document individual extensions
4. Fumadocs processes MDX and generates static documentation
5. Orama provides search functionality with Chinese language support

### Configuration Files
- `next.config.ts` - Next.js configuration with MDX support
- `source.config.ts` - Fumadocs source configuration
- `app/layout.config.tsx` - Site layout and navigation
- `lib/source.ts` - Source loaders for documentation
- `lib/i18n.ts` - Internationalization configuration

### Database Schema
The PostgreSQL database contains several tables in the `ext` schema:
- `ext.cate` - Extension categories
- `ext.repo` - Repository information
- `ext.extension` - Extension details
- `ext.pigsty` - Pigsty-specific extension data

## Content Structure

### Extension Documentation
Each extension has a corresponding MDX file in `content/docs/ext/` following the pattern `{extension-name}.mdx`. The site supports both complete documentation and stub files for incomplete extensions.

### Internationalization
- Default language: English (`en`)
- Secondary language: Chinese (`zh`)
- Locale-specific content in `content/docs/` with `.zh.mdx` suffixes
- Search configured with Chinese tokenizer for zh locale

## Development Notes

### Data Updates
When updating extension data, use the PostgreSQL database as the source of truth and export to CSV files using `make save`. The database connection is configured via `PGURL` environment variable (defaults to `postgres:///vonng`).

### Search Configuration
The search API (`app/api/search/route.ts`) uses Orama with special configuration for Chinese content, including custom tokenizers and relaxed thresholds for better matching.

### Build Process
The build process uses Fumadocs to generate static documentation from MDX files. The `fumadocs-mdx` postinstall script processes MDX content during package installation.


## Python Environment

Use `~/.venv/bin/activate` to use python virtual environment

## Translation Rules

如果你收到了翻译任务，你应该读取指定的内容文件或者目录，将其翻译为指定的语言。

作为一个示例，如果我要把 pgsql/acl.mdx 翻译成英文，那么你应该找到 content/docs/pgsql/acl.mdx 文件，将其翻译为 content/docs/pgsql/acl.zh.mdx 文件。
这里特别需要注意的是，在翻译非英文版本的文档过程中：

1. 你应该保留所有的 Markdown 链接，如果这是一个相对链接，那么你应该意识到，在其他语言的翻译中应该加上对应前缀。比如在中文翻译中你需要加上 `/zh/` 前缀来引用文档
2. 你应该保留所有 H2/H3/H4 等标题的英文锚点，然后在引用的链接中统一使用英文锚点。
3. 你应该使用地道，信达雅，精准，干练，专业的用词来进行翻译，使用计算机领域与数据库领域的专业术语。

## 提前授权

如果你要访问网络读取文档，读取本地 HTTP 访问，直接执行即可。

如果你要执行本地读取文件类操作，无需询问授权，直接干就完了。
如果你要进行本地编辑，如果是跟业务相关的文件，直接干就完了。

对于批量删除操作，你要向我确认一下。其他的中低风险我授权你执行。