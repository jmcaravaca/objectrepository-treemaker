from parsers.activities import main_activities
from parsers.uiobjects import main_uiobjects
from parsers.uireferences import main_uireferences
from parsers.activityreferences import main_activityreferences
from parsers.configs import main_configs
from parsers.configreferences import main_configreferences
from parsers.getrepos import clone_repos
import os, click
from db.startdb import create_db
from loguru import logger


@click.group()
def cli():
    pass


# @cli.command()
@click.option("--delete", default="no")
def init_db(delete: str == "no"):
    if delete == "yes":
        os.remove("uidata.db")
        # click.echo("Deleted DB")
    create_db()
    # click.echo("Initialized the database")


# @cli.command()
def clone_repos():
    clone_repos()
    click.echo("Initialized the database")


# @cli.command()
@click.option(
    "--findsubfolder",
    default="yes",
    help="whether to find subfolders in the provided path or take it as is",
)
@click.argument("librarylocation")
def get_activities(findsubfolder: str, librarylocation: str):
    logger.debug(f"{librarylocation} : {findsubfolder}")
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        logger.debug(liblist)
        for lib in liblist:
            main_activities(folderpath=lib)
    else:
        main_activities(folderpath=librarylocation)


# @cli.command()
@click.option(
    "--findsubfolder",
    default="yes",
    help="whether to find subfolders in the provided path or take it as is",
)
@click.argument("librarylocation")
def get_uiobjects(findsubfolder: str, librarylocation: str):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_uiobjects(folderpath=lib)
    else:
        main_uiobjects(folderpath=librarylocation)


# @cli.command()
@click.option(
    "--findsubfolder",
    default="yes",
    help="whether to find subfolders in the provided path or take it as is",
)
@click.argument("librarylocation")
def get_activityreferences(findsubfolder: str, librarylocation: str):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        logger.debug(liblist)
        for lib in liblist:
            main_activityreferences(folderpath=lib)
    else:
        main_activityreferences(folderpath=librarylocation)


# @cli.command()
@click.option(
    "--findsubfolder",
    default="yes",
    help="whether to find subfolders in the provided path or take it as is",
)
@click.argument("librarylocation")
def get_uireferences(findsubfolder: str, librarylocation: str):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_uireferences(folderpath=lib)
    else:
        main_uireferences(folderpath=librarylocation)


@cli.command()
@click.option(
    "--findsubfolder",
    default="yes",
    help="whether to find subfolders in the provided path or take it as is",
)
@click.argument("librarylocation")
def get_configreferences(findsubfolder: str, librarylocation: str):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_configreferences(folderpath=lib)
    else:
        main_configreferences(folderpath=librarylocation)


@cli.command()
@click.option(
    "--findsubfolder",
    default="yes",
    help="whether to find subfolders in the provided path or take it as is",
)
@click.argument("librarylocation")
def get_configs(findsubfolder: str, librarylocation: str):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_configs(folderpath=lib)
    else:
        main_configs(folderpath=librarylocation)


if __name__ == "__main__":
    cli()
