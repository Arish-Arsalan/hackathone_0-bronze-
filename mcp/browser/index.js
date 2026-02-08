#!/usr/bin/env node
/**
 * Browser MCP Server - For web automation
 */
const { createMcpServer } = require('@modelcontextprotocol/sdk');
const playwright = require('playwright');
require('dotenv').config({ path: '../../.env' });

const server = createMcpServer({
  name: 'browser-mcp',
  version: '1.0.0',
  capabilities: {
    tools: {
      list: [
        {
          name: 'navigate',
          description: 'Navigate to a URL',
          parameters: {
            type: 'object',
            properties: {
              url: { type: 'string' },
              wait_for: { type: 'string' }
            },
            required: ['url']
          }
        }
      ]
    }
  }
});

server.tools.set('navigate', async (params) => {
  const { url, wait_for = 'domcontentloaded' } = params;
  
  const browser = await playwright.chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  
  await page.goto(url, { waitUntil: wait_for });
  const content = await page.content();
  
  await browser.close();
  
  return { 
    success: true, 
    message: 'Page loaded successfully',
    content: content.substring(0, 500) + '...' 
  };
});

server.connectStdio().then(() => {
  console.log('🌐 Browser MCP Server started (stdio transport)');
});
