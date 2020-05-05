import json, os

class Util:

    @staticmethod
    def load_json(parent_path = "configuration", sufix = ".json", file_name = ""):
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, parent_path, file_name + sufix)
        data = None
        try:
            with open(file_path, "r", 1024, "utf8") as f:
                data = f.read()
            if sufix == ".txt":
                return data
            return json.loads(data)
        except Exception as e:
            print("json file load failed!")

    @staticmethod
    def appendUnderLinePrefix(input):
        return "_%s" % input if input.isdigit() else input

    @staticmethod
    def stringToDate4Netease(data):
        arr = data.split(",")
        if len(arr) != 6:
            return data
        month = int(arr[1])+1
        day = int(arr[2])
        return "{}-{}-{} {}:{}:{}".format(arr[0], "0" + str(month) if month < 10 else month + 1, "0" + str(day) if day < 10 else day, arr[3], arr[4], arr[5])