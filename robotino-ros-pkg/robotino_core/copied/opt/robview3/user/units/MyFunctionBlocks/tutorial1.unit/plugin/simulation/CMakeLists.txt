cmake_minimum_required( VERSION 2.6 )
SET( NAME unit_robview_myfunctionblocks_tutorial1_simulation )

IF( WIN32 )
	STRING( REPLACE "\\" "/" ROBVIEW2APIDIR "$ENV{ROBOTINOVIEW3_API_DIR}" )
	INCLUDE( "${ROBVIEW2APIDIR}/cmake/unit_plugin_simulation.cmake" )
ELSE( WIN32 )
	INCLUDE( /opt/robview3/api/cmake/unit_plugin_simulation.cmake )
ENDIF( WIN32 )
