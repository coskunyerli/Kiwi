import PySide2.QtCore as QtCore


class SearchListModelProxy(QtCore.QSortFilterProxyModel):
	def filterAcceptsRow(self, sourceRow, sourceParent):
		index = self.sourceModel().index(sourceRow)
		dataList = index.data()
		tags = dataList[-1]
		name = dataList[1].lower()
		reqExp = self.filterRegExp()
		if reqExp.pattern():
			return reqExp.pattern().lower() in name or self.searchTag(tags)
		else:
			return True


	def searchTag(self, tags):
		reqExp = self.filterRegExp()
		searchedTags = reqExp.pattern().split(';')
		for tag in searchedTags:
			return tag in tags
