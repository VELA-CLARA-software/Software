# loggerWidget

*loggerWidget* is a simple PyQt widget that records logging output from the Python **logging** module.

## Implementation

- Import libraries

        import loggerWidget as lw
        import logging

- Define your logger (see [Python Logging](https://docs.python.org/2/library/logging.html))

        logger = logging.getLogger(__name__)

- Initialise the loggingWidget (this returns a PyQt widget)
    - Initialise widget then add logger

            logwidget = lw.loggerWidget()
            logwidget.addLogger(logger)

    - Initialise widget with logger

            logwidget = lw.loggerWidget(logger)

    - Initialise widget with multiple loggers

            logwidget = lw.loggerWidget([logger, logger2])

- Use logging messages in your app

        logger.debug('damn, a bug')
        logger.info('something to remember')
        logger.warning('that\'s not right')
        logger.error('foobar')
        logger.critical('really foobar')
