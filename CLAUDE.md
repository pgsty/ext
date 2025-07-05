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
- Secondary language: Chinese (`cn`)
- Locale-specific content in `content/docs/` with `.cn.mdx` suffixes
- Search configured with Chinese tokenizer for CN locale

## Development Notes

### Data Updates
When updating extension data, use the PostgreSQL database as the source of truth and export to CSV files using `make save`. The database connection is configured via `PGURL` environment variable (defaults to `postgres:///vonng`).

### Search Configuration
The search API (`app/api/search/route.ts`) uses Orama with special configuration for Chinese content, including custom tokenizers and relaxed thresholds for better matching.

### Build Process
The build process uses Fumadocs to generate static documentation from MDX files. The `fumadocs-mdx` postinstall script processes MDX content during package installation.