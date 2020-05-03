import PySide2.QtCore as QtCore


class DataModelProxy(QtCore.QSortFilterProxyModel):
	def filterAcceptsRow(self, sourceRow, sourceParent):
		index = self.sourceModel().index(sourceRow)
		dataList = index.data()
		reqExp = self.filterRegExp()
		if reqExp.pattern():
			return reqExp.pattern().lower() in dataList[1].lower()
		else:
			return True
