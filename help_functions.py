def get_dict(self, data_type, data, key):

        if data_type == "weapon":
            for category in data.keys():
                for weapon in data[category]:
                    if weapon["key"] == key:
                        return weapon
        elif data_type == "agent":
            for agent in data["list"]:
                if agent["key"] == key:
                    return agent
            