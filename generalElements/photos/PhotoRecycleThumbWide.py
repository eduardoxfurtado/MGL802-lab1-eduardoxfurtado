from generalElements.photos.PhotoRecycleThumb import PhotoRecycleThumb

from kivy.lang.builder import Builder
from generalElements.labels.PhotoThumbLabel import PhotoThumbLabel

Builder.load_string("""

<PhotoRecycleThumbWide>:
    PhotoThumbLabel:
        text: root.title
""")
class PhotoRecycleThumbWide(PhotoRecycleThumb):
    pass