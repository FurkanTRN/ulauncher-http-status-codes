import json
import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

def load_http_status_codes():
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'http_status_codes.json')
        
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: http_status_codes.json not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON in http_status_codes.json")
        return {}

class HTTPStatusExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.status_codes = load_http_status_codes()

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        items = []

        filtered_codes = {code: description for code, description in extension.status_codes.items() if query in code}

        max_results = 5
        filtered_codes = dict(list(filtered_codes.items())[:max_results])

        if filtered_codes:
            for code, description in filtered_codes.items():
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=f"HTTP {code}",
                    description=description,
                    on_enter=OpenUrlAction(f"https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{code}")
                ))
        else:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name="No matching status codes",
                description="Please enter a valid HTTP status code.",
                on_enter=None
            ))

        return RenderResultListAction(items)

if __name__ == '__main__':
    HTTPStatusExtension().run()
