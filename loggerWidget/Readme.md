# loggerWidget

*loggerWidget* is a simple PyQt widget that records logging output from the Python **logging** module.

## Implementation

1. Import libraries
        import loggerWidget as lw
        import logging

2. Define your logger (see [Python Logging](https://docs.python.org/2/library/logging.html))
        logger = logging.getLogger(__name__)
3. Initialise the loggingWidget (this returns a PyQt widget)
  1. Initialise widget then add logger
            logwidget = lw.loggerWidget()
            logwidget.addLogger(logger)
  2. Initialise widget with logger
            logwidget = lw.loggerWidget(logger)
  3. Initialise widget with multiple loggers
            logwidget = lw.loggerWidget([logger, logger2])
4. Use logging messages in your app
        logger.debug('damn, a bug')
        logger.info('something to remember')
        logger.warning('that\'s not right')
        logger.error('foobar')
        logger.critical('really foobar')
