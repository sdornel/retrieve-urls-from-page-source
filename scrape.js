// const puppeteer = require('puppeteer');

// function scrape() {
//     (async () => {
//         const browser = await puppeteer.launch({ headless: true });
//         const page = await browser.newPage();
        
//         await page.goto('https://www.facebook.com', { waitUntil: 'networkidle2' });

//         const pageContent = await page.content();
//         console.log(pageContent.match(/https?:\/\/[^\s"'>]+/g) || []);

//         await browser.close();
//         return pageContent.match(/https?:\/\/[^\s"'>]+/g) || [];
//     })();
// }

// scrape();

async function scrape(url) {
    const res = await fetch(url);
    const html = await res.text();
    console.log(html.match(/https?:\/\/[^\s"'>]+/g) || []);
}

scrape('https://www.archive.org');
