from TreeViewItem.TreeViewItem import TreeViewItem

class TreeViewItemFavorites(TreeViewItem):
    indent = 0

    def visit(self, visitor):
        super(TreeViewItemFavorites, self).visit()

        screenDatabase = self.owner
        datas = []
        for photo in self.item.favorites():
            datas.append(photo.data_item(screenDatabase))

        screenDatabase.data = datas
        screenDatabase.update_can_browse()
        screenDatabase.update_selected()

    def visit_drop(self,visitors):
        self.owner.add_favorites(visitors)

