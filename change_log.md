# Change Log

## [Added] Enhanced Matching Algorithm using spaCy

- Integrated spaCy library for more sophisticated matching algorithm.
- Installed spaCy and downloaded English language model.
- Used spaCy to compute similarity between user input and existing questions in the knowledge base.
- Replaced the `find_best_match` function with a new implementation that uses spaCy for similarity comparison.
- Improved accuracy of matching based on semantic similarity.

## [Changed] Logging Configuration

- Configured additional file handler for the existing `reboot_logger` to write log messages to the same log file (`chatbot.log`) as the general logging.
- All log messages, including those from the reboot process, are now written to the same log file.

## [Fixed] Reboot Process Error Handling

- Modified the reboot process to read the entire script content at once and execute it, avoiding syntax errors from partial code execution.
- Ensured that the reboot process is properly logged and executed without encountering syntax errors due to incomplete code execution.
