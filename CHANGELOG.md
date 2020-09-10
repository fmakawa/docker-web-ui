# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2020-09-10

## [Unreleased]

- container CPU usage and performance metrics and graphs
- backwards compatability with older versions of docker

### Added

- Removed ability to delete the docker-web UI container that is running this app
- Adjusted UI in index to separate the Docker Web UI container from the running containers and add it to the bottom of the index page instead
- Changed README.md to include images of the UI
- Added a travis CI config file. Not yet configured for CI/CD
- Added persistant memory to run command
- Fixed inspect button bug on some pages
- Fixed stop,pause and remove bug in running_all.html used in the Running page

## [0.1.0] - 2020-06-07

## [Unreleased]

- container CPU usage and performance metrics and graphs
- backwards compatability with older versions of docker

### Added

- Added basic inspect, stop, pause, unpause functionality

## Convention

- Following changelog convention as described here: https://keepachangelog.com/en/0.3.0/