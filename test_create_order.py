import pytest
from enums import UnitType
from models import Order
from uuid import uuid4

DEFAULT_CLIENT_NAME = 'Пол Атрейдес'


class TestCreateOrder:
    @pytest.mark.parametrize(
        "available, quantity, is_valid",
        [
            (100, 50, True),  # Quantity в [10;1000] для UnitType.GRAMS.
            (100, 10, True),  # Левая граница quantity.
            (1000, 1000, True),  # Правая граница quantity.
            (2000, 1001, False),  # Quantity > max значения.
            (100, 9, False),  # Quantity < min значения.
            (10, 100, False),  # Quantity > доступного значения.
            (100, 0, False),  # Quantity принимает нулевое значение.
            (100, None, False),  # Quantity принимает null значение.
            (100, "abc", False),  # Quantity принимает отличное от INT значение.
            (100, -15, False)  # Quantity принимает отрицательное значение.
        ]
    )
    def test_create_order_with_unit_type_grams(self, client, available, quantity, is_valid,
                                               client_name=DEFAULT_CLIENT_NAME):
        spice_id = client.spices.add_spice("Перец черный", UnitType.GRAMS, available)
        try:
            order_id = client.orders.create_order(spice_id, quantity, client_name)
        except Exception:
            assert is_valid is False, f"Заказ с параметрами spice_id={spice_id}, quantity={quantity}, " \
                                      f"client_name={client_name} не был создан."
            spice_details = client.spices.get_spice(spice_id)
            assert spice_details.available == available, "Кол-во специи на складе уменьшилось при неудачном заказе."

        else:
            order_details = client.orders.get_order(order_id)
            spice_details = client.spices.get_spice(spice_id)
            expected_order = self._create_expected_order(
                order_id, quantity, client_name, spice_id
            )
            assert expected_order == order_details, "Данные заказа отличаются от ожидаемых."
            assert spice_details.available == available - quantity, "Кол-во специи на складе не уменьшилось."

    @pytest.mark.parametrize(
        "available, quantity, is_valid",
        [
            (100, 5, True),  # Quantity в [1;10] для UnitType.PIECES.
            (100, 1, True),  # Левая граница quantity.
            (100, 10, True),  # Правая граница quantity.
            (100, 11, False),  # Quantity > max значения.
            (100, 0, False),  # Quantity < min значения.
            (2, 3, False),  # Quantity > доступного значения.
            (100, None, False),  # Quantity принимает null значение.
            (100, "abc", False),  # Quantity принимает отличное от INT значение.
            (100, -6, False)  # Quantity принимает отрицательное значение.
        ]
    )
    def test_create_order_with_unit_type_pieces(self, client, available, quantity, is_valid,
                                                client_name=DEFAULT_CLIENT_NAME):
        spice_id = client.spices.add_spice("Корица Палочки", UnitType.PIECES, available)
        try:
            order_id = client.orders.create_order(spice_id, quantity, client_name)
        except Exception:
            assert is_valid is False, f"Заказ с параметрами spice_id={spice_id}, quantity={quantity}, " \
                                      f"client_name={client_name} не был создан."
            spice_details = client.spices.get_spice(spice_id)
            assert spice_details.available == available, "Кол-во специи на складе уменьшилось при неудачном заказе."

        else:
            order_details = client.orders.get_order(order_id)
            spice_details = client.spices.get_spice(spice_id)
            expected_order = self._create_expected_order(
                order_id, quantity, client_name, spice_id
            )
            assert expected_order == order_details, "Данные заказа отличаются от ожидаемых."
            assert spice_details.available == available - quantity, "Кол-во специи на складе не уменьшилось."

    @pytest.mark.parametrize(
        "client_name, is_valid",
        [
            ("Валерий МЕЛАДЗЕ", True),  # Сlient_name содержит кириллицу размером в [3;20].
            ("Timothee СHALAMET", True),  # Сlient_name содержит латиницу размером в [3;20].
            ("abz", True),  # Левая граница Сlient_name на латинице.
            ("пар", True),  # Левая граница Сlient_name на кириллице.
            ("бвгдёжзкмнопстуфхцчш", True),  # Правая граница Сlient_name на кириллице.
            ("ЯЮЭЬЫЪЩШЧЦХФУТСРПОНК", True),  # Правая граница Сlient_name на кириллице в верхем регистре.
            ("щъыьэюяЙИЖЁГБ", True),  # Оставшиеся символы на кириллице.
            ("bcdfgjklnpqrstuvwxyz", True),  # Правая граница Сlient_name на латинице.
            ("BDFGIJKNOPQRSTUVWXYZ", True),  # Правая граница Сlient_name на латинице в верхем регистре.
            ("ужебоольшоеимяклиента", False),  # Сlient_name > max значения.
            ("mщ", False),  # Сlient_name < min значения.
            (None, False),  # Сlient_name принимает null значение.
            ("", False),  # Сlient_name принимает пустое значение.
            ("  ", False),  # Сlient_name содержит только пробелы.
            ("J!ohn O'Grady", False),  # Сlient_name содержит спецсимволы.
            ("ἀλφάβητος", False),  # Сlient_name содержит невалидный алфавит.
            ("d123re", False)  # Сlient_name содержит числа.
        ]
    )
    def test_create_order_customer_name(self, client, client_name, is_valid, quantity=20, available=100):
        spice_id = client.spices.add_spice("Перец Красный", UnitType.GRAMS, available)
        try:
            order_id = client.orders.create_order(spice_id, quantity, client_name)
        except Exception:
            assert is_valid is False, f"Заказ с параметрами spice_id={spice_id}, quantity={quantity}, " \
                                      f"client_name={client_name} не был создан."
            spice_details = client.spices.get_spice(spice_id)
            assert spice_details.available == available, "Кол-во специи на складе уменьшилось при неудачном заказе."

        else:
            order_details = client.orders.get_order(order_id)
            spice_details = client.spices.get_spice(spice_id)
            expected_order = self._create_expected_order(
                order_id, quantity, client_name, spice_id
            )
            assert expected_order == order_details, "Данные заказа отличаются от ожидаемых."
            assert spice_details.available == available - quantity, "Кол-во специи на складе не уменьшилось."

    @pytest.mark.parametrize(
        "spice_id",
        [
            uuid4(),  # Spice_id содержит несуществующий id.
            None  # Spice_id принимает null значение.
        ]
    )
    def test_create_order_not_valid_spice_id(self, client, spice_id, client_name=DEFAULT_CLIENT_NAME, quantity=5):
        order_id = None
        try:
            order_id = client.orders.create_order(spice_id, quantity, client_name)
        except Exception:
            assert order_id is None, f"Заказ с параметрами spice_id={spice_id}, quantity={quantity}, " \
                                      f"client_name={client_name} не должен быть созданным."
        else:
            assert order_id is None, f"Заказ с параметрами spice_id={spice_id}, quantity={quantity}, " \
                                      f"client_name={client_name} не должен быть созданным."

    @staticmethod
    def _create_expected_order(eid, quantity, customer_name, spice_id) -> Order:
        return Order(
            eid=eid,
            quantity=quantity,
            customer_name=customer_name,
            spice_id=spice_id
        )
