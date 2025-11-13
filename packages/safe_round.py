import math
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Iterator, List, Optional, Union


class NumberRounder:
    """
    یک کلاس حرفه‌ای برای گرد کردن اعداد با روش‌های مختلف
    و جلوگیری از ایجاد خطا های مختلف در طی برنامه
    """

    def __init__(self, zero_return: bool = True):
        self.zero_return: bool = zero_return
        self._history: List[dict] = []  # تاریخچه عملیات

    def __call__(
        self, number: Union[int, float, str, None]
    ) -> Optional[Union[float, int]]:
        """can use in this format : rounder(3.141618)"""
        return self.round(number)

    def __str__(self) -> str:
        """see how this class work"""
        return f"NumberRounder(zero_return={self.zero_return}, history_operations={len(self._history)})"

    def __repr__(self) -> str:
        """for developers : repr(rounder)"""
        return f"NumberRounder(zero_return={self.zero_return}, history_size={len(self._history)})"

    def __len__(self) -> int:
        """number of useing this class"""
        return len(self._history)

    def __iter__(self) -> Iterator[dict]:
        """امکان پیمایش در تاریخچه: for op in rounder"""
        return iter(self._history)

    def __contains__(self, number: Union[int, float]) -> bool:
        """یک تابع خیلی کاربردیه که امکان بررسی وجود یک عدد در تاریخچه کلاس را با دستور
        rounder = NumberRounder()
        rounder.round(3.14)
        3.14 in rounder
        True
        فراهم میکند.
        """
        for op in self._history:
            # اضافه کردن بررسی برای None
            if op["input"] is None:
                continue
            if math.isclose(op["input"], number, rel_tol=1e-9):
                return True
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        """پاکسازی هنگام خروج از context manager"""
        if exc_type:
            print(f"Error occurred: {exc_val}")
        return False  # خطا propagate شود

    def _add_to_history(
        self,
        input_num: Union[int, float, str, None],
        result: Optional[Union[float, int]],
    ):
        """افزودن عملیات به تاریخچه (متد کمکی)"""
        self._history.append(
            {
                "input": input_num if input_num is None else float(input_num),
                "output": result,
                "timestamp": len(self._history) + 1,
            }
        )

    def round(
        self, number: Union[int, float, str, None], zero_return: Optional[bool] = None
    ) -> Optional[Union[float, int]]:
        """
        عدد را به دو رقم اعشار گرد می‌کند
        """
        if number is None:
            return None

        if zero_return is None:
            zero_return = self.zero_return

        try:
            numeric_value: Decimal = Decimal(str(number)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            result = float(numeric_value)

            # بررسی صفر بودن
            if result == 0:
                self._add_to_history(number, result)
                return 0 if zero_return else None
            else:
                self._add_to_history(number, result)
                return result

        except (ValueError, TypeError):
            return None

    def round_list(
        self,
        numbers: List[Union[int, float, str, None]],
        zero_return: Optional[bool] = None,
    ) -> List[Optional[Union[float, int]]]:
        """
        گرد کردن لیستی از اعداد
        """
        return [self.round(num, zero_return) for num in numbers]

    def clear_history(self):
        """پاک کردن تاریخچه"""
        self._history.clear()

    def get_history_stats(self) -> dict:
        """آمار تاریخچه عملیات"""
        if not self._history:
            return {}

        successful_ops = [op for op in self._history if op["output"] is not None]
        failed_ops = [op for op in self._history if op["output"] is None]

        return {
            "total_operations": len(self._history),
            "successful_operations": len(successful_ops),
            "failed_operations": len(failed_ops),
            "success_rate": (
                len(successful_ops) / len(self._history) if self._history else 0
            ),
        }


# how to use
# from packages.safe_round import NumberRounder

# if __name__ == "__main__":
#     rounder = NumberRounder()

#     # تست عملکردها
#     print(rounder.round(1.23))  # 1.23

#     print(rounder(3.1411615))  # 3.14

#     result_list: List[float | int | None] = rounder.round_list(
#         [1.25153, 2.355158, 0, None], zero_return=False
#     )
#     print(result_list)  # [1.25, 2.36, None, None]

#     # تست تاریخچه
#     print(f"History length: {len(rounder)}")
#     print(f"Stats: {rounder.get_history_stats()}")

#     # تست contains
#     print(3.14 in rounder)  # True
