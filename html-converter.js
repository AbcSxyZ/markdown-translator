// Script used from python to convert html to markdown using the turndown
// library (https://github.com/mixmark-io/turndown)
//
// Use JavaScript library as there is no suitable python library to convert
// html to markdown with appropriate standards. Expecting to use the most
// robust converter of every languages.
//
// markdownify (python lib) issue : empty line at code block end. No other
// appropriate python lib founded.

const TurndownService = require('turndown');
const turndownService = new TurndownService({
  headingStyle:"atx",
  codeBlockStyle:"fenced",
});

// Rule to keep html div balise inside markdown
turndownService.addRule('keepDiv', {
  filter: ['div'],
  replacement: function(content, node) {
    return node.outerHTML;
  }
});

// Read HTML from stdin
let html = "";
process.stdin.on('readable', () => {
  let chunk;
  while ((chunk = process.stdin.read())) {
    html += chunk;
  }
});

// Convert html to markdown, write output to stdout
process.stdin.on('end', () => {
  const markdown = turndownService.turndown(html);
  process.stdout.write(markdown);
});
