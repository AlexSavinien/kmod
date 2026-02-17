## SelectionShortcuts
##
## Extra selection shortcuts for stack filters.

from CvPythonExtensions import *


def _triggerSelectionControl(eControl):
	# Don't steal focus-sensitive key input.
	if CyInterface().isFocused():
		return 0

	CyGame().doControl(eControl)
	return 1


def selectWoundedStack(argsList=None):
	"""
	Triggers CONTROL_SELECT_HEALTHY.
	Behavior is implemented in the DLL:
	- Alt+H: all wounded units on current plot
	- Ctrl+H: wounded units matching selected unit type
	"""
	return _triggerSelectionControl(ControlTypes.CONTROL_SELECT_HEALTHY)


def selectUndamagedStack(argsList=None):
	"""
	Triggers CONTROL_SELECT_UNDAMAGED.
	Behavior is implemented in the DLL:
	- Alt+V: all non-wounded units on current plot
	- Ctrl+V: non-wounded units matching selected unit type
	"""
	return _triggerSelectionControl(ControlTypes.CONTROL_SELECT_UNDAMAGED)


def selectFullMovesStack(argsList=None):
	"""
	Triggers CONTROL_SELECT_FULL_MOVES.
	Behavior is implemented in the DLL:
	- Alt+W: all units with full movement points on current plot
	- Ctrl+W: full-movement units matching selected unit type
	"""
	return _triggerSelectionControl(ControlTypes.CONTROL_SELECT_FULL_MOVES)
