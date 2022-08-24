import httpx
import click
import re
from bs4 import BeautifulSoup
import os

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"}


def save_file(filename: str, filecontent: str, directory: str) -> bool:
    if not os.path.isdir(directory):
        os.mkdir(directory)
    with open(os.path.join(directory, filename), mode="wb") as file:
        file.write(filecontent)
    return True


@click.command()
@click.argument('url')
def check_url(url: str) -> str:
    website = httpx.get(url, follow_redirects=True)

    website_name = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
    click.echo(f"Checking URL {url} now.")

    google_pattern = r"fonts.googleapis.com/css"

    match = re.search(google_pattern, string=website.text)
    if match:
        click.echo(f"The Website {url} contains Google-Fonts. Change that now!")
        soup = BeautifulSoup(website.content, "html.parser")
        google_fonts_url = soup.find("link", attrs={'href': re.compile(r'fonts.googleapis.com/css')})
        find_font_link = re.search(r"(https?|//)", google_fonts_url["href"]).group()
        if find_font_link:
            css_link = google_fonts_url["href"]
            if find_font_link == "//":
                css_link = "https:" + google_fonts_url["href"]
            google_css = httpx.get(css_link, headers=headers)
            woff_files = re.findall(r"url\((.*?)\)", google_css.text)
            for font in woff_files:
                font_name = re.search(r"[\w_-]+.(woff2?|ttf)", font).group(0)
                save_file(font_name, httpx.get(font).content, website_name)
            modified_css = re.sub(r"https:.*/", "", google_css.text)
            save_file("fonts.css", modified_css.encode("utf-8"), website_name)
            click.echo(f"Saved all the necessary files to {website_name}.")
    else:
        click.echo(f"The Website {url} ist Google-Fonts free.")


if __name__ == '__main__':
    check_url()
