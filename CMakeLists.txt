cmake_minimum_required(VERSION 2.8.9)

project(SimpleVTK)

#-----------------------------------------------------------------------------
set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/SimpleVTK")
set(EXTENSION_CATEGORY "SimpleVTK")
set(EXTENSION_CONTRIBUTORS "Kevin Wang (Princess Margaret Cancer Centre)")
set(EXTENSION_DESCRIPTION "This is SimpleVTK extension")
set(EXTENSION_ICONURL "http://viewvc.slicer.org/viewvc.cgi/Slicer4/trunk/Extensions/Testing/SimpleVTK/SimpleVTK.png?revision=21747&view=co")
set(EXTENSION_SCREENSHOTURLS "http://wiki.slicer.org/slicerWiki/images/e/e2/Slicer-r19441-SimpleVTK-screenshot.png")

#-----------------------------------------------------------------------------
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
add_subdirectory(ImageResample)
add_subdirectory(ImageCast)

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
