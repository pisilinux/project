# Project name
PROJECT (comar)

# CMake 2.6 required
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

# Python is required
FIND_PACKAGE(PythonLibs)

FIND_PACKAGE(PkgConfig)
PKG_CHECK_MODULES (DBUS REQUIRED dbus-1)

# Application name
SET (APP_NAME "comar")
SET (APP_SUFFIX "3")

# Uncomment this for production releases.
SET (VERSION_SUFFIX "")
#SET (FLAGS "-g -O0 -Werror -Wcast-align -Wno-uninitialized -Wall -fstrict-aliasing")

# Uncomment this for gprof profiling
# SET (FLAGS "-g -O0 -Werror -Wcast-align -Wno-uninitialized -Wall -fstrict-aliasing -fprofile-arcs -ftest-coverage")
#SET (CMAKE_C_FLAGS "${FLAGS}")
# Uncomment this for sparse building
# SET (CMAKE_C_COMPILER cgcc)

# Append name suffix, if specified
IF (APP_SUFFIX)
   SET (APP_NAME "${APP_NAME}${APP_SUFFIX}")
ENDIF (APP_SUFFIX)

# Define version, config dir, data dir and log file.
ADD_DEFINITIONS (
                 -D'PID_FILE="/var/run/${APP_NAME}.pid"'
                 -D'DATA_DIR="/var/lib/${APP_NAME}"'
                 -D'LOG_DIR="/var/log/${APP_NAME}"')

# Set standard sources
SET (SOURCES src/main.c
             src/bus.c
             src/config.c
             src/db.c
             src/iksemel.c
             src/log.c
             src/loop.c
             src/process.c
             src/policy.c
             src/pydbus.c
             src/script.c
             src/utils.c)

# Set standard libraries
SET (LIBS ${PYTHON_LIBRARIES}
          dbus-1)

# Include standard headers
INCLUDE_DIRECTORIES (include/
                     ${PYTHON_INCLUDE_DIRS}
                     ${DBUS_INCLUDE_DIRS})

# Compile comar from specified sources
ADD_EXECUTABLE (comar ${SOURCES})

# Link comar to specified libraries
TARGET_LINK_LIBRARIES(comar ${LIBS} )

# Install comar to /usr/sbin/<app-name>
INSTALL (PROGRAMS comar
         DESTINATION /usr/sbin)

# Install Models
INSTALL (DIRECTORY
        models
        DESTINATION /var/db/${APP_NAME}
        PATTERN ".svn" EXCLUDE)

# Install Modules
INSTALL (DIRECTORY
        modules
        DESTINATION /var/db/${APP_NAME}
        PATTERN ".svn" EXCLUDE)

# Install service activation config under /usr/share/dbus-1/system-services/
INSTALL (FILES
         config/tr.org.pardus.comar.service
         config/tr.org.pardus.comar2.service
         DESTINATION /usr/share/dbus-1/system-services/)

# Install polkit policies
INSTALL (DIRECTORY
         policy/
         DESTINATION /usr/share/polkit-1/actions
         FILES_MATCHING PATTERN "*.policy"
         PATTERN ".svn" EXCLUDE)

# Install system bus policy under /etc/dbus-1/system.d/
INSTALL (FILES
         config/tr.org.pardus.comar.conf
         DESTINATION /etc/dbus-1/system.d)

# Install hav to /usr/bin/hav
INSTALL (PROGRAMS tools/hav.py
         DESTINATION /usr/bin
         RENAME hav)

# Install hav to /usr/bin/comar2to3
INSTALL (PROGRAMS tools/comar2to3.py
         DESTINATION /usr/bin
         RENAME comar2to3)
