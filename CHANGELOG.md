# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2020-09-28

## [Unreleased]

- container CPU usage and performance metrics and graphs
- backwards compatability with older versions of docker

### Added
- [BIG CHANGE] Changed URLS for container related to include 'containers' in the url i.e '/containers/running'. This is to ensure that as we add networks, images etc they follow the same naming convention
- Fixed known issue regarding hardcoded database path. Changed the database directory mapping to ensure that its not hardcoded and can be easily preserved through mounting volumes for data continuity.
- Added deletion checks for containers without mounted volumes.
- Added stop checks for containers with autoremove enabled and those with autoremove and without mounted volumes.
- Adjusted RUN command for Docker in README
- Changed the top navbar to be reactive to the docker section in use (Volumes, Containers, Config etc). Its also now highlights the current page
- Added a sidebar menu to better navigate the different sections.
- Added bootstrap and other related js and css files instead of using a CDN. Some systems might have closed systems.
- Added a Help page
- Reordered the directory setup and added the modules for config, images, volumes,swarm, network, system and overview. Templates were also restructured.

## Issues
- The container for the prettified inspect data is now too large for the screen with sidebar. The current fix is to have a new menu bar for the  Inspect page. Would like to revert to the sidebar to maintain design consistency.

## [Next Release]
- Add warnings for removing containers that have autoremove enabled or do not have mounted volumes

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