import view.main as main_window
from loguru import logger


if __name__ == '__main__':
    logger.add('logging.log', rotation='1 week', backtrace=True, diagnose=True,
               format="<level>{level}</level>| <magenta>{time:DD.MM.YYYY H:m:s}</magenta>| "
               "<level>{message}</level>")

    logger.info('Launching the program...')
    try:
        main_window.main()
    except Exception as exc:
        logger.error(f'Непредвиденная ошибка!\n{exc.__str__()}')
