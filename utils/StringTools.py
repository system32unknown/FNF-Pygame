class StringTools:
    @staticmethod
    def fill_number(value: float, digits: int, code: int) -> str:
        """
        Fill numbers with a specified number of digits and right-align with the number.
        :param value: Floating-point number
        :param digits: Integer (minimum width)
        :param code: Integer (ASCII code of padding char)
        :return: String
        """
        s = str(value)
        length = len(s)

        if length < digits:
            return chr(code) * (digits - length) + s
        else:
            return s

    @classmethod
    def format_time(cls, time: float, precision: int = 0, time_pre: int = 0) -> str:
        """
        Formats a given time in seconds into a human-readable string (weeks, days, hours, minutes, seconds).
        :param time: Floating-point number representing total seconds
        :param precision: Integer specifying decimal precision
        :param time_pre: Integer for additional time formatting
        :return: Formatted time string
        """
        secs = str(int(time) % 60)
        mins = str(int(time // 60) % 60)
        hour = str(int(time // 3600) % 24)
        days = str(int(time // 86400) % 7)
        weeks = str(int(time // (86400 * 7)))

        if len(secs) < 2:
            secs = "0" + secs

        formatted_time = f"{mins}:{secs}"

        if hour != "0" and days == "0":
            if len(mins) < 2:
                mins = "0" + mins
            formatted_time = f"{hour}:{mins}:{secs}"

        if days != "0" and weeks == "0":
            formatted_time = f"{days}d {hour}h {mins}m {secs}s"
        if weeks != "0":
            formatted_time = f"{weeks}w {days}d {hour}h {mins}m {secs}s"

        if precision > 0:
            seconds_for_ms = time % 60
            seconds = int((seconds_for_ms - int(seconds_for_ms)) * precision)
            formatted_time += "." + cls.fill_number(seconds, time_pre, ord("0"))

        return formatted_time
    
    @staticmethod
    def format_bytes(num_bytes: float, precision: int = 2) -> str:
        """
        Takes an amount of bytes and finds the fitting unit.
        Makes sure that the value is below 1024.
        Example: format_bytes(123456789) -> "117.74MB"
        """
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        cur_unit = 0

        while num_bytes >= 1024 and cur_unit < len(units) - 1:
            num_bytes /= 1024
            cur_unit += 1

        return f"{round(num_bytes, precision)}{units[cur_unit]}"