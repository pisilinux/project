find_package(KDE4 REQUIRED)
include(KDE4Defaults)

add_definitions(${QT_DEFINITIONS} ${KDE4_DEFINITIONS})
include_directories(${KDE4_INCLUDES})

find_package(OpenGL REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}
                    ${CMAKE_CURRENT_BINARY_DIR})

add_subdirectory(po)

########### kcontrol module ###############

set(kcm_panda_PART_SRCS panda.cpp
                        panda_parser.cpp)


kde4_add_plugin(kcm_panda ${kcm_panda_PART_SRCS})


target_link_libraries(kcm_panda
                        ${KDE4_KDEUI_LIBS}
                        kworkspace
                        ${QT_QTGUI_LIBRARY}
                        ${X11_X11_LIB}
                        ${OPENGL_gl_LIBRARY})

install(TARGETS kcm_panda  DESTINATION ${PLUGIN_INSTALL_DIR} )

#### KAuth helper and actions ####
kde4_add_executable(kcmpandahelper helper.cpp)
target_link_libraries(kcmpandahelper ${KDE4_KDECORE_LIBS})
install(TARGETS kcmpandahelper DESTINATION ${LIBEXEC_INSTALL_DIR})

kde4_install_auth_helper_files(kcmpandahelper org.kde.kcontrol.kcmpanda root)

kde4_install_auth_actions(org.kde.kcontrol.kcmpanda kcmpanda.actions)


########### install files ###############

install( FILES panda.desktop  DESTINATION  ${SERVICES_INSTALL_DIR} )

kde4_install_icons( ${ICON_INSTALL_DIR}  )
