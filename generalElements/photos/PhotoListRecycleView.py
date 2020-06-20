from kivy.properties import NumericProperty
from kivy.uix.recycleview import RecycleView


class PhotoListRecycleView(RecycleView):
    selected_index = NumericProperty(0)

    def index(self,treeViewItem):
        pos = None
        for idx, data in enumerate(self.data):
            if data == treeViewItem:
                pos = idx
                break
        return pos

    def next(self,treeViewItem):
        current_index = self.index(treeViewItem)
        if current_index is not None:
            if current_index == len(self.data) - 1:
                next_index = 0
            else:
                next_index = current_index + 1
        return self.data[next_index]

    def previous(self, treeViewItem):
        current_index = self.index(treeViewItem)
        if current_index is not None:
            if current_index == 0:
                previous_index = len(self.data) - 1
            else:
                previous_index = current_index - 1
        return self.data[previous_index]

    def scroll_to_selected(self):
        box = self.children[0]
        selected = box.selected
        for i, item in enumerate(self.data):
            if item.target == selected.target:
                self.selected_index = i
                break
        index = self.selected_index
        pos_index = (box.default_size[1] + box.spacing) * index
        scroll = self.convert_distance_to_scroll(0, pos_index - (self.height * 0.5))[1]
        if scroll > 1.0:
            scroll = 1.0
        elif scroll < 0.0:
            scroll = 0.0
        self.scroll_y = 1.0 - scroll

    def convert_distance_to_scroll(self, dx, dy):
        box = self.children[0]
        wheight = box.default_size[1] + box.spacing

        if not self._viewport:
            return 0, 0
        vp = self._viewport
        vp_height = len(self.data) * wheight
        if vp.width > self.width:
            sw = vp.width - self.width
            sx = dx / float(sw)
        else:
            sx = 0
        if vp_height > self.height:
            sh = vp_height - self.height
            sy = dy / float(sh)
        else:
            sy = 1
        return sx, sy

    def accept(self, treeViewItem):
        treeViewItem.visit(self)


