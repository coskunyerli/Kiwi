import PySide2.QtCore as QtCore


class DataModelProxy(QtCore.QSortFilterProxyModel):
	def filterAcceptsRow(self, sourceRow, sourceParent):
		index = self.sourceModel().index(sourceRow)
		dataList = index.data()
		reqExp = self.filterRegExp()
		name = dataList[1].lower()
		# check that pattern text in the name
		if reqExp.pattern():
			return reqExp.pattern().lower() in name
		else:
			return True
