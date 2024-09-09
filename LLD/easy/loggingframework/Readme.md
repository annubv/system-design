# LOGGING FRAMEWORK
- Can have multiple log levels
    - DEBUG
    - INGO
    - WARN
    - ERROR

- Can have multiple outputs
    - DB
    - FILE
    - CONSOLE
- Store logs with timetamp, log level, and message
- Extensible output and levels


## Entity Identification
- LogLevel
    - DEBUG
    - INGO
    - WARN
    - ERROR
- LogMessage
- LogAppender
    - ConsoleAppender
    - FileAppender
    - DatabaseAppender
- LoggerConfig
- LoggerService