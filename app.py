import httpx
import click
import re
from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"}


@click.command()
@click.argument('url')
def check_url(url: str) -> str:
    website = httpx.get(url, follow_redirects=True)

    click.echo(f"Checking URL {url} now.")

    google_pattern = r"fonts.googleapis.com"

    match = re.search(google_pattern, string=website.text)
    if match:
        click.echo(f"The Website {url} contains Google-Fonts. Change that now!")
        soup = BeautifulSoup(website.content, "html.parser")
        google_fonts_url = soup.find("link", attrs={'href': re.compile(r'fonts.googleapis.com')})
        if google_fonts_url["href"].startswith("//"):
            google_css = httpx.get(f"https:{ google_fonts_url['href']}", headers=headers)
            woff_files = re.findall(r"url\((.*?)\)", google_css.text)
            click.echo("You can download the woff/woff2 files from here:")
            for font in woff_files:
                click.echo(font)
            click.echo("Here is your modified css-file:\n\n")
            modified_css = re.sub(r"https:.*/", "", google_css.text)
            click.echo(modified_css)




    else:
        click.echo(f"The Website {url} ist Google-Fonts free.")


if __name__ == '__main__':
    check_url()
