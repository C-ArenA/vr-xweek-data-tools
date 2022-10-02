import os, json

class Model:
    def __init__(self, view, db_file_path) -> None:
        self.view = view
        self.db_file_path = os.path.normpath(db_file_path)
        try:
            with open(self.db_file_path, "r", encoding="utf-8") as db_file:
                self.db = json.load(db_file)
            self.xweekconfig = self.db["xweekconfig"]
            self.xweekevents = self.db["xweekevents"]
        except:
            self.db = {}
            self.view.no_model(self.db_file_path)
            
    def get_config(self):
        return self.xweekconfig
    def get_last_event(self):
        return self.xweekevents[-1]
    def get_last_event_data(self):
        return self.get_last_event()["data"]
    def get_last_event_paths(self):
        return self.get_last_event()["paths"]
    def get_last_event_now(self):
        return self.get_last_event()["now"]

    def save(self):
        with open(self.db_file_path, "w", encoding="utf-8") as db_file:
            json.dump(self.db, db_file, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    from xweekdatatools.views.view import View
    view = View()
    model = Model(view, "db.json")
    view.show_event_data(model.get_last_event_data())
    view.select_main_action()