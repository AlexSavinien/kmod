## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvLogisticsRoutesScreen:
	"Routes Logistique Screen"

	MOD_MESSAGE_SET_FOOD_ROUTE_FLOW = 7100

	TABLE_X = 18
	TABLE_Y = 92
	ROW_HEIGHT = 24
	TABLE_HEADER_HEIGHT = 24
	ACTION_BUTTON_SIZE = 20

	COL_NAME = 0
	COL_POP = 1
	COL_FOOD = 2
	COL_GROWTH = 3
	COL_PROD = 4
	COL_PROD_END = 5
	COL_MINUS = 6
	COL_PLUS = 7
	COL_FLOW = 8
	COL_STATUS = 9

	def __init__(self, iScreenID):
		self.iScreenID = iScreenID
		self.iSourceCityID = -1
		self.nScreenWidth = 0
		self.nScreenHeight = 0
		self.nTableWidth = 0
		self.nTableHeight = 0
		self.nNormalizedTableWidth = 970
		self.aiColumnWidths = [0] * 10
		self.aRouteButtonNames = []
		self.mPendingFlowOverrides = {}

	def getScreen(self):
		return CyGInterfaceScreen("LogisticsRoutesScreen", self.iScreenID)

	def interfaceScreen(self, iSourceCityID = -1):
		screen = self.getScreen()

		self.nScreenWidth = screen.getXResolution() - 30
		self.nScreenHeight = screen.getYResolution() - 120
		self.nTableWidth = self.nScreenWidth - 35
		self.nTableHeight = self.nScreenHeight - 170

		self.iSourceCityID = iSourceCityID
		self.mPendingFlowOverrides = {}
		self.resolveSourceCity()

		screen.setRenderInterfaceOnly(True)
		screen.setDimensions(15, 30, self.nScreenWidth, self.nScreenHeight)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addPanel("LogisticsRoutesBG", u"", u"", True, False, 0, 0, self.nScreenWidth, self.nScreenHeight, PanelStyles.PANEL_STYLE_MAIN)
		screen.setText("LogisticsRoutesExit", "Background", localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper(), CvUtil.FONT_RIGHT_JUSTIFY, self.nScreenWidth - 25, self.nScreenHeight - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
		screen.setLabel("LogisticsRoutesTitle", "Background", u"<font=4b>Routes Logistique</font>", CvUtil.FONT_LEFT_JUSTIFY, 22, 18, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("LogisticsSourcePanel", u"", u"", True, True, 18, 42, self.nTableWidth, 44, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setLabel("LogisticsRoutesSummary", "Background", u"", CvUtil.FONT_LEFT_JUSTIFY, 22, 52, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("LogisticsHint", "Background", u"<font=1>Tableau cible: toutes les autres villes. Les boutons +/- sont inactifs hors reseau commercial.</font>", CvUtil.FONT_LEFT_JUSTIFY, 22, self.nScreenHeight - 64, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.drawContents()
		CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)

	def getPlayerCity(self, player, iCityID):
		if iCityID < 0:
			return None
		city = player.getCity(iCityID)
		if city is None:
			return None
		if city.isNone():
			return None
		return city

	def resolveSourceCity(self):
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		if player.getNumCities() <= 0:
			self.iSourceCityID = -1
			return

		sourceCity = self.getPlayerCity(player, self.iSourceCityID)
		if sourceCity is not None:
			return

		if CyInterface().isCityScreenUp() and CyInterface().isOneCitySelected():
			headCity = CyInterface().getHeadSelectedCity()
			if headCity and not headCity.isNone() and headCity.getOwner() == gc.getGame().getActivePlayer():
				self.iSourceCityID = headCity.getID()
				return

		(loopCity, iter) = player.firstCity(False)
		if loopCity and not loopCity.isNone():
			self.iSourceCityID = loopCity.getID()
		else:
			self.iSourceCityID = -1

	def getGrowthText(self, city):
		iFoodDiff = city.foodDifference(True)
		if city.isFoodProduction():
			return u"Production"
		if iFoodDiff > 0:
			return u"%d tour(s)" % city.getFoodTurnsLeft()
		if iFoodDiff < 0:
			return u"%d tour(s) famine" % (city.getFood() / -iFoodDiff + 1)
		return u"-"

	def getProductionPerTurn(self, city):
		if city.isProductionProcess():
			return city.getYieldRate(YieldTypes.YIELD_PRODUCTION)
		return city.getCurrentProductionDifference(True, False)

	def getProductionEndText(self, city):
		if city.getOrderQueueLength() <= 0:
			return u"-"
		if city.isProductionProcess():
			return u"%s (continu)" % city.getProductionName()
		return u"%s (%d tour(s))" % (city.getProductionName(), city.getProductionTurnsLeft())

	def formatSignedRate(self, iValue):
		sz = u"%+d" % iValue
		if iValue > 0:
			return localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + sz + localText.getText("TXT_KEY_COLOR_REVERT", ())
		if iValue < 0:
			return localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + sz + localText.getText("TXT_KEY_COLOR_REVERT", ())
		return sz

	def formatDisabledAction(self, szText):
		return u"<color=160,160,160,255>%s</color>" % szText

	def clearRouteButtons(self):
		screen = self.getScreen()
		for szName in self.aRouteButtonNames:
			screen.deleteWidget(szName)
		self.aRouteButtonNames = []

	def getColumnStartX(self, iColumn):
		iX = self.TABLE_X
		for i in range(iColumn):
			iX += self.aiColumnWidths[i]
		return iX

	def addRouteAdjustButton(self, iCityID, iRow, bPlus, bEnabled):
		screen = self.getScreen()
		iColumn = self.COL_PLUS
		if not bPlus:
			iColumn = self.COL_MINUS
		iColX = self.getColumnStartX(iColumn)
		iColWidth = self.aiColumnWidths[iColumn]
		iX = iColX + max(0, (iColWidth - self.ACTION_BUTTON_SIZE) / 2)
		iY = self.TABLE_Y + self.TABLE_HEADER_HEIGHT + 2 + iRow * self.ROW_HEIGHT
		iSign = 0
		iDelta = -1
		eStyle = ButtonStyles.BUTTON_STYLE_CITY_MINUS
		if bPlus:
			iSign = 1
			iDelta = 1
			eStyle = ButtonStyles.BUTTON_STYLE_CITY_PLUS
		szName = "LogisticsRouteAdjust_%d_%d" % (iCityID, iSign)
		screen.setButtonGFC(szName, u"", "", iX, iY, self.ACTION_BUTTON_SIZE, self.ACTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, iCityID, iDelta, eStyle)
		screen.show(szName)
		screen.enable(szName, bEnabled)
		screen.moveToFront(szName)
		self.aRouteButtonNames.append(szName)

	def drawHeaders(self):
		screen = self.getScreen()
		self.aiColumnWidths[self.COL_NAME] = (170 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_POP] = (50 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_FOOD] = (90 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_GROWTH] = (75 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_PROD] = (80 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_PROD_END] = (190 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_MINUS] = (45 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_PLUS] = (45 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_FLOW] = (120 * self.nTableWidth) / self.nNormalizedTableWidth
		self.aiColumnWidths[self.COL_STATUS] = (95 * self.nTableWidth) / self.nNormalizedTableWidth

		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_NAME, "<font=2>Ville</font>", self.aiColumnWidths[self.COL_NAME])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_POP, "<font=2>Pop</font>", self.aiColumnWidths[self.COL_POP])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_FOOD, "<font=2>Nourriture/tour</font>", self.aiColumnWidths[self.COL_FOOD])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_GROWTH, "<font=2>Croissance</font>", self.aiColumnWidths[self.COL_GROWTH])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_PROD, "<font=2>Prod/tour</font>", self.aiColumnWidths[self.COL_PROD])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_PROD_END, "<font=2>Fin de prod</font>", self.aiColumnWidths[self.COL_PROD_END])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_MINUS, "<font=2>-</font>", self.aiColumnWidths[self.COL_MINUS])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_PLUS, "<font=2>+</font>", self.aiColumnWidths[self.COL_PLUS])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_FLOW, "<font=2>Flux (nourriture/tour)</font>", self.aiColumnWidths[self.COL_FLOW])
		screen.setTableColumnHeader("LogisticsRoutesTable", self.COL_STATUS, "<font=2>Etat</font>", self.aiColumnWidths[self.COL_STATUS])

	def updateSummary(self):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		sourceCity = self.getPlayerCity(player, self.iSourceCityID)
		if sourceCity is None:
			screen.setLabel("LogisticsRoutesSummary", "Background", u"<font=2>Aucune ville source selectionnee.</font>", CvUtil.FONT_LEFT_JUSTIFY, 22, 52, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			return

		iFoodDiff = sourceCity.foodDifference(True)
		iProd = self.getProductionPerTurn(sourceCity)
		szSummary = u"<font=2>Source: %s | Pop: %d | Nourriture/tour: %s | Croissance: %s | Prod/tour: %s | Fin de prod: %s</font>" % (
			sourceCity.getName(),
			sourceCity.getPopulation(),
			self.formatSignedRate(iFoodDiff),
			self.getGrowthText(sourceCity),
			self.formatSignedRate(iProd),
			self.getProductionEndText(sourceCity))

		screen.setLabel("LogisticsRoutesSummary", "Background", szSummary, CvUtil.FONT_LEFT_JUSTIFY, 22, 52, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def updateCityRow(self, sourceCity, city, iRow):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		iPlayer = gc.getGame().getActivePlayer()
		iCityID = city.getID()

		bConnected = sourceCity.isConnectedTo(city)
		iConfiguredFlow = player.getCityLogisticsRouteFlow(self.iSourceCityID, iCityID, YieldTypes.YIELD_FOOD, False)
		iActiveFlow = player.getCityLogisticsRouteFlow(self.iSourceCityID, iCityID, YieldTypes.YIELD_FOOD, True)
		if self.mPendingFlowOverrides.has_key(iCityID):
			iPendingFlow = self.mPendingFlowOverrides[iCityID]
			if iPendingFlow == iConfiguredFlow:
				del self.mPendingFlowOverrides[iCityID]
			else:
				iConfiguredFlow = iPendingFlow
		bRoutePossible = player.canCreateCityLogisticsRoute(self.iSourceCityID, iCityID, YieldTypes.YIELD_FOOD)
		iDisplayActiveFlow = iActiveFlow
		if self.mPendingFlowOverrides.has_key(iCityID):
			if iConfiguredFlow > 0 and bConnected and bRoutePossible:
				iDisplayActiveFlow = iConfiguredFlow
			else:
				iDisplayActiveFlow = 0
		bCanAdd = bRoutePossible
		bCanReduce = iConfiguredFlow > 0

		if iConfiguredFlow <= 0 and not bConnected:
			szStatus = u"Hors reseau"
		elif iConfiguredFlow <= 0 and not bRoutePossible:
			szStatus = u"Source sans grenier"
		elif iConfiguredFlow <= 0:
			szStatus = u"Disponible"
		elif not bConnected:
			szStatus = u"Suspendu"
		elif not bRoutePossible:
			szStatus = u"Suspendu"
		elif iDisplayActiveFlow > 0:
			szStatus = u"Actif"
		else:
			szStatus = u"Suspendu"

		iFoodDiff = city.foodDifference(True)
		iProd = self.getProductionPerTurn(city)

		screen.setTableText("LogisticsRoutesTable", self.COL_NAME, iRow, city.getName(), "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableInt("LogisticsRoutesTable", self.COL_POP, iRow, unicode(city.getPopulation()), "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_FOOD, iRow, self.formatSignedRate(iFoodDiff), "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_GROWTH, iRow, self.getGrowthText(city), "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_PROD, iRow, self.formatSignedRate(iProd), "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_PROD_END, iRow, self.getProductionEndText(city), "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_MINUS, iRow, u"", "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_PLUS, iRow, u"", "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_FLOW, iRow, self.formatSignedRate(iConfiguredFlow), "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("LogisticsRoutesTable", self.COL_STATUS, iRow, szStatus, "", WidgetTypes.WIDGET_GENERAL, iPlayer, iCityID, CvUtil.FONT_LEFT_JUSTIFY)
		self.addRouteAdjustButton(iCityID, iRow, False, bCanReduce)
		self.addRouteAdjustButton(iCityID, iRow, True, bCanAdd)

	def drawContents(self):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.resolveSourceCity()
		sourceCity = self.getPlayerCity(player, self.iSourceCityID)
		self.clearRouteButtons()

		screen.deleteWidget("LogisticsRoutesTable")
		screen.addTableControlGFC("LogisticsRoutesTable", 10, self.TABLE_X, self.TABLE_Y, self.nTableWidth, self.nTableHeight, True, False, 24, self.ROW_HEIGHT, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("LogisticsRoutesTable", True)
		screen.setStyle("LogisticsRoutesTable", "Table_StandardCiv_Style")

		self.drawHeaders()

		iRow = 0
		(loopCity, iter) = player.firstCity(False)
		while(loopCity):
			if (sourceCity is not None) and (loopCity.getID() != sourceCity.getID()):
				screen.appendTableRow("LogisticsRoutesTable")
				self.updateCityRow(sourceCity, loopCity, iRow)
				iRow += 1
			(loopCity, iter) = player.nextCity(iter, False)

		self.updateSummary()

	def changeRouteFlow(self, iTargetCityID, iDelta):
		playerID = gc.getGame().getActivePlayer()
		player = gc.getPlayer(playerID)
		if self.iSourceCityID < 0 or iTargetCityID < 0 or self.iSourceCityID == iTargetCityID:
			return

		sourceCity = self.getPlayerCity(player, self.iSourceCityID)
		targetCity = self.getPlayerCity(player, iTargetCityID)
		if sourceCity is None or targetCity is None:
			return
		if iDelta > 0 and not sourceCity.isConnectedTo(targetCity):
			return

		iCurrent = player.getCityLogisticsRouteFlow(self.iSourceCityID, iTargetCityID, YieldTypes.YIELD_FOOD, False)
		if self.mPendingFlowOverrides.has_key(iTargetCityID):
			iCurrent = self.mPendingFlowOverrides[iTargetCityID]
		if iDelta > 0 and not player.canCreateCityLogisticsRoute(self.iSourceCityID, iTargetCityID, YieldTypes.YIELD_FOOD):
			return
		if iDelta < 0 and iCurrent <= 0:
			return

		iNewFlow = max(0, iCurrent + iDelta)
		if iNewFlow == iCurrent:
			return

		CyMessageControl().sendModNetMessage(self.MOD_MESSAGE_SET_FOOD_ROUTE_FLOW, playerID, self.iSourceCityID, iTargetCityID, iNewFlow)
		self.mPendingFlowOverrides[iTargetCityID] = iNewFlow
		CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
		CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, True)
		self.drawContents()

	def handleInput(self, inputClass):
		if inputClass.getNotifyCode() != NotifyCode.NOTIFY_CLICKED:
			return 0
		szName = inputClass.getFunctionName()
		if not szName.startswith("LogisticsRouteAdjust_"):
			return 0
		self.changeRouteFlow(inputClass.getData1(), inputClass.getData2())
		return 0

	def update(self, fDelta):
		if CyInterface().isDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT):
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, False)
			self.drawContents()
		return

	def onClose(self):
		return
