/**
 * Converts markdown text to HTML; note that indented code blocks are not supported.
 * @param {string} markdownText The markdown text to convert
 * @returns {string} The HTML (i.e., converted text)
 */
function convertMarkdown(markdownText, globalRefs = null) {
    /**
     * Escapes special markdown/HTML characters to protect them from unnecessary conversion
     * @param {string} text The text to escape special characters
     * @returns {string} The escaped text
     */
    function escapeSpecialChrs(text) {
        return text.replace(/[*_[\\\]#\-=!]/g, (c) => `&#${c.charCodeAt(0)};`).replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    /**
     * Formats HTML output with proper multi-level indentation
     * @param {string} html The unformatted HTML string
     * @returns {string} The formatted HTML string
     */
    function formatHTMLOutput(html) {
        const blockTags = 'blockquote|ul|ol|li|div';
        const startClosesRegex = new RegExp(`^(<\\/(${blockTags})>)+`, 'i');
        const opensRegex = new RegExp(`<(${blockTags})[ >]`, 'gi');
        const closesRegex = new RegExp(`<\\/(${blockTags})>`, 'gi');

        const lines = html.split('\n');
        let formatted = [];
        let indent = 0;
        let inPre = false;
        
        lines.forEach(line => {
            let trimmed = line.trim();
            if (trimmed.length===0) {
                formatted.push(inPre ? line : '');
                return;
            }
            
            // Deal with code in pre blocks
            let isPreStart = trimmed.match(/<pre/i);
            let isPreEnd = trimmed.match(/<\/pre>/i);
            if (isPreStart) {
                inPre = true;
                formatted.push('    '.repeat(indent)+line);
                if (isPreEnd) inPre = false;
                return;
            }
            if (inPre) {
                formatted.push(line);
                if (isPreEnd) inPre = false;
                return;
            }
            
            // Deal with indentation
            let printIndent = indent;
            let startClosesMatch = trimmed.match(startClosesRegex);
            if (startClosesMatch) {
                let numStartCloses = (startClosesMatch[0].match(/<\//g) || []).length;
                printIndent = Math.max(0, indent-numStartCloses);
            }
            formatted.push('    '.repeat(printIndent)+trimmed);
            let opens = (trimmed.match(opensRegex) || []).length;
            let closes = (trimmed.match(closesRegex) || []).length;
            indent = Math.max(0, indent+opens-closes);
        });
        
        return formatted.join('\n');
    }

    let html = markdownText;
    const placeholders = [];
    let references = globalRefs || {};

    // Add reference definitions
    if (!globalRefs) {
        const definitionRegex = /^[ \t]*\[([^\]]+)\]:\s*([^\s<]+)(?:\s+(?:"([^"]*)"|'([^']*)'|\(([^)]*)\)))?\s*$/gm;
        html = html.replace(definitionRegex, (match, id, url, titleDouble, titleSingle, titleParen) => {
            let title = titleDouble || titleSingle || titleParen;
            references[id.toLowerCase()] = {url, title};
            return '';
        });
    }

    // Fenced Code Blocks (Multi-line)
    const codeBlockRegex = /^[ \t]*`{3}[ \t]*(?<language>[a-z0-9-]*)[ \t]*\r?\n(?<code>[\s\S]*?)^[ \t]*`{3}/gm;
    html = html.replace(codeBlockRegex, (match, language, code) => {
        let escapedCode = escapeSpecialChrs(code);
        let output = language ? `<pre><code class="language-${language}">${escapedCode}</code></pre>` : `<pre><code>${escapedCode}</code></pre>`;
        placeholders.push(output);
        return `<pre>MDPLACEHOLDER${placeholders.length-1}X</pre>`;
    });

    // Inline Code
    const inlineCodeRegex = /(?<!\\)(?<ticks>`+)(?<code>.+?)\k<ticks>/g;
    html = html.replace(inlineCodeRegex, (match, ticks, code) => {
        let escapedCode = escapeSpecialChrs(code.trim());
        placeholders.push(`<code>${escapedCode}</code>`);
        return `MDINLINEPLACEHOLDER${placeholders.length-1}X`;
    });

    // Escaped Characters
    const escapeRegex = /\\([\\`*_{}[\]()#+\-.!>])/g;
    html = html.replace(escapeRegex, (match, char) => `&#${char.charCodeAt(0)};`);

    // Blockquotes (with recursion)
    const quoteBlockRegex = /^(?:[ \t]*>.*\r?\n?)+/gm;
    html = html.replace(quoteBlockRegex, (match) => {
        const quoteText = match.replace(/^[ \t]*>[ \t]?/gm, '');
        let childHtml = convertMarkdown(quoteText, references);
        placeholders.push(`<blockquote>\n${childHtml}\n</blockquote>`);
        return `<blockquoteMDPLACEHOLDER${placeholders.length-1}X>\n`;
    });

    // Groups of regex for each type of markdown
    const headingRegex = /^[ \t]*(?<level>#{1,6})[ \t]+(?<heading>.*)/gm;
    html = html.replace(headingRegex, (match, level, heading) => {
        const levelNum = level.length;
        return `<h${levelNum}>${heading.trim()}</h${levelNum}>`
    });

    const altHeading1Regex = /^(?<heading>[^\n\r]+)\r?\n={2,}\s*$/gm;
    html = html.replace(altHeading1Regex, `<h1>$<heading></h1>`);

    const altHeading2Regex = /^(?<heading>[^\n\r]+)\r?\n-{2,}\s*$/gm;
    html = html.replace(altHeading2Regex, `<h2>$<heading></h2>`);

    const lineReggex = /^[ \t]*([-*_])[ \t]*\1[ \t]*\1[-\s*_]*$/gm;
    html = html.replace(lineReggex, `<hr>`);

    // Lists (ordered and unordered)
    const listBlockRegex = /^(?:[ \t]*(?:[*+-]|\d+\.)[ \t]+.*(?:\r?\n|$))+/gm;
    html = html.replace(listBlockRegex, (match) => {
        const lines = match.split(/\r?\n/).filter(line => line.trim()!=='');
        let result = '';
        const stack = []; // { indent: number, type: 'ul'|'ol' }

        lines.forEach((line) => {
            const listMatch = line.match(/^([ \t]*)([*+-]|\d+\.)[ \t]+(.*)/);
            if (listMatch) {
                const indent = listMatch[1].length;
                const bullet = listMatch[2];
                const type = /^[*+-]$/.test(bullet) ? 'ul' : 'ol';
                let content = convertMarkdown(listMatch[3], references).replace(/^<p>([\s\S]*)<\/p>$/i, '$1'); 

                while (stack.length>0 && stack[stack.length-1].indent>indent) {
                    result += `</li>\n</${stack.pop().type}>\n`;
                }

                if (stack.length===0 || stack[stack.length-1].indent<indent) {
                    stack.push({indent, type});
                    result += (stack.length>1 ? `\n` : ``) + `<${type}>\n<li>${content}`;
                } else if (stack.length>0 && stack[stack.length-1].indent===indent && stack[stack.length-1].type!==type) {
                    result += `</li>\n</${stack.pop().type}>\n<${type}>\n<li>${content}`;
                    stack.push({indent, type});
                } else {
                    result += `</li>\n<li>${content}`;
                }
            }
        });

        while (stack.length>0) {
            result += `</li>\n</${stack.pop().type}>\n`;
        }

        placeholders.push(result);
        return `<ulMDPLACEHOLDER${placeholders.length-1}X>\n`;
    });

    const boldRegex = /(?<boldType>\*{2}|_{2})(?<boldText>.*?)\k<boldType>/g;
    html = html.replace(boldRegex, `<strong>$<boldText></strong>`);

    const italicRegex = /(?<italicType>\*|_)(?<italicText>.*?)\k<italicType>/g;
    html = html.replace(italicRegex, `<em>$<italicText></em>`);

    const imgRegex = /!\[([^\]]*)\]\(([^\s)]+)(?:\s+(?:"([^"]*)"|'([^']*)'|\(([^)]*)\)))?\)/g;
    html = html.replace(imgRegex, (match, alt, src, titleDouble, titleSingle, titleParen) => {
        let title = titleDouble || titleSingle || titleParen;
        let titleAttr = title ? ` title="${title}"` : '';
        return `<img src="${src}" alt="${alt}"${titleAttr}>`;
    });

    const linkRegex = /\[([^\]]+)\]\(([^\s)]+)(?:\s+(?:"([^"]*)"|'([^']*)'|\(([^)]*)\)))?\)/g;
    html = html.replace(linkRegex, (match, text, url, titleDouble, titleSingle, titleParen) => {
        let title = titleDouble || titleSingle || titleParen;
        let titleAttr = title ? ` title="${title}"` : '';
        return `<a href="${url}"${titleAttr}>${text}</a>`;
    });

    const refLinkRegex = /\[([^\]]+)\] ?\[([^\]]*)\]/g;
    html = html.replace(refLinkRegex, (match, text, refId) => {
        let key = (refId || text).toLowerCase(); // Fallback to text if empty like [link][]
        if (references[key]) {
            let titleAttr = references[key].title ? ` title="${references[key].title}"` : '';
            return `<a href="${references[key].url}"${titleAttr}>${text}</a>`;
        }
        return match;
    });

    const autolinkRegex = /<(?<autoLink>(?:https?|ftp):\/\/[^\s>]+)>/g;
    html = html.replace(autolinkRegex, `<a href="$<autoLink>">$<autoLink></a>`);

    const emailRegex = /<(?<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>/g;
    html = html.replace(emailRegex, `<a href="mailto:$<email>">$<email></a>`);

    const paragraphRegex = /^(?!<(?:h[1-6]|blockquote|ul|ol|li|div|p|hr|pre))(?<paragraphText>(?:[^\n\r]+(?:\r?\n(?!\r?\n|<(?:h[1-6]|blockquote|ul|ol|li|div|p|hr|pre)))?)+)/gm;
    html = html.replace(paragraphRegex, (match, paragraphText) => {
        return `<p>${paragraphText.replace(/\r?\n/g, '<br>')}</p>`;
    });

    // Restore placeholders
    placeholders.forEach((block, i) => {
        html = html.replace(`<ulMDPLACEHOLDER${i}X>`, () => block);
        html = html.replace(`<blockquoteMDPLACEHOLDER${i}X>`, () => block);
        html = html.replace(`<pre>MDPLACEHOLDER${i}X</pre>`, () => block);
        html = html.replace(`MDINLINEPLACEHOLDER${i}X`, () => block);
    });

    return formatHTMLOutput(html.trim());
}


// Handeling user input
/** @type {HTMLTextAreaElement} */
const markdownInput = document.getElementById("markdown-input");
/** @type {HTMLDivElement} */
const htmlOutput = document.getElementById("html-output");
/** @type {HTMLDivElement} */
const htmlPreview = document.getElementById("preview");
markdownInput.addEventListener("input", () => {
    const htmlConverted = convertMarkdown(markdownInput.value);
    htmlOutput.textContent = htmlConverted;
    htmlPreview.innerHTML = htmlConverted;
})

// Handeling copy button
const copyButton = document.getElementById("copy-button");
markdownInput.addEventListener("input", () => {
    copyButton.disabled = (htmlOutput.textContent.trim() === "");
})
copyButton.addEventListener("click", () => {
    navigator.clipboard.writeText(htmlOutput.textContent);
    copyButton.textContent = "Copied!";
    copyButton.disabled = true;
    setTimeout(() => {
        copyButton.textContent = "Copy HTML to Clipboard";
        copyButton.disabled = (htmlOutput.textContent.trim() === "");
    }, 1000);
})