import httpx
import click
import re


@click.command()
@click.argument('url')
def check_url(url: str) -> str:
    website = httpx.get(url)

    click.echo(f"Checking URL {url} now.")

    match = re.search(r"fonts.googleapis.com", string=website.text)
    if match:
        click.echo(f"The Website {url} contains Google-Fonts. Change that now!")
    else:
        click.echo(f"The Website {url} ist Google-Fonts free.")


if __name__ == '__main__':
    check_url()
