from typing import Optional, Tuple
from PIL import Image


class MockRoomData(object):
    def __init__(self, images, name: str):
        self.images = images
        self.name = name
        self.index = 0

    def get_image(self):
        if len(self.images) == 0:
            return None
        image = self.images[self.index]
        self.index = (self.index + 1) % len(self.images)
        return image


class MockRooms(object):
    def __init__(self):
        self.data = {
            "1": MockRoomData(['liv_1.jpg'], "Test Room"),
            "2": MockRoomData(['.jpg', 'and_2.jpg', 'and_3.jpg', 'and_4.jpg', 'and_5.jpg', 'and_6.jpg', 'and_7.jpg'], "Andreea's Room"),
            "3": MockRoomData(['liv_1.jpg', 'liv_2.jpg', 'liv_3.jpg', 'liv_4.jpg'], "Liviu's Room"),
            "4": MockRoomData(['mar_2.jpg', 'mar_3.jpg', 'mar_5.jpg', 'mar_6.jpg', 'mar_13.jpg', 'mar_24.jpg', 'mar_29.jpg', 'mar_33.jpg', 'mar_36.jpg'], "Maria's Room")
        }

    def get_mock_data_for_room(self, room_id: str) -> Optional[MockRoomData]:
        if room_id not in self.data:
            return None
        return self.data[room_id]

    def has_room(self, room_id: str) -> bool:
        return room_id in self.data


mock_rooms = MockRooms()
base_image_path = 'resources/images/'


def handle_mock_room(room_id: str) -> Optional[any]:
    if not mock_rooms.has_room(room_id):
        return None

    room_data = mock_rooms.get_mock_data_for_room(room_id)
    image_name = base_image_path + room_data.get_image()
    image = Image.open(image_name)
    return room_data.name, image
