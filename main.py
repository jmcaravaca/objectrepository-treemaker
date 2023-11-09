from activities import main_activities
from uiobjects import main_uiobjects
from uireferences import main_uireferences
from activityreferences import main_activityreferences
import os, click
from db.startdb import CreateDB
from loguru import logger

@click.group()
def cli():
    pass

@cli.command()
@click.option('--delete', default='no')
def init_db(delete:str):
    if delete == 'yes':
        os.remove("uidata.db")
        click.echo('Deleted DB')
    CreateDB()
    click.echo('Initialized the database')


@cli.command()
@click.option('--findsubfolder', default='yes', help='whether to find subfolders in the provided path or take it as is')
@click.argument('librarylocation')
def get_activities(findsubfolder: str, librarylocation: str):
    logger.debug(f"{librarylocation} : {findsubfolder}")
    if findsubfolder == 'yes':
        liblist = [os.path.join(librarylocation, foldername) for foldername in next(os.walk(librarylocation))[1]]
        logger.debug(liblist)
        for lib in liblist:
            main_activities(folderpath=lib)
    else:
        main_activities(folderpath=librarylocation)

@cli.command()
@click.option('--findsubfolder', default='yes', help='whether to find subfolders in the provided path or take it as is')
@click.argument('librarylocation')
def get_uiobjects(findsubfolder: str, librarylocation: str):
    if findsubfolder == 'yes':
        liblist = [os.path.abspath(name) for name in os.listdir(librarylocation)]
        for lib in liblist:
            main_uiobjects(folderpath=lib)
    else:
        main_activities(folderpath=librarylocation)            

@cli.command()
@click.option('--findsubfolder', default='yes', help='whether to find subfolders in the provided path or take it as is')
@click.argument('librarylocation')
def get_activityreferences(findsubfolder: str, librarylocation: str):
    if findsubfolder == 'yes':
        liblist = [os.path.abspath(name) for name in os.listdir(librarylocation)]
        for lib in liblist:
            main_activityreferences(folderpath=lib)
    else:
        main_activities(folderpath=librarylocation)            

@cli.command()
@click.option('--findsubfolder', default='yes', help='whether to find subfolders in the provided path or take it as is')
@click.argument('librarylocation')
def get_uireferences(findsubfolder: str, librarylocation: str):
    if findsubfolder == 'yes':
        liblist = [os.path.abspath(name) for name in os.listdir(librarylocation)]
        for lib in liblist:
            main_uireferences(folderpath=lib)
    else:
        main_activities(folderpath=librarylocation)            
                
    
if __name__ == '__main__':
    cli()