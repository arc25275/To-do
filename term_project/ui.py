import customtkinter as ctk
import tkinter as tk
import zmq
import json
from typing import Self


# TODO: When functions are done, improve docstring with more info


class Client:
    """TODO"""

    def __init__(self, connection):
        self.root = ctk.CTk()
        self.tasks = []
        self.attributes = []
        self.connection = connection
        self.UI = {
            "root": self.root,
            "task_container": None,
            "detail_container": None,
            "help_page": None,
        }

    # Build default UI
    def build_initial_ui(self):
        """TODO:Build containers, task list, details, and help page"""
        pass

    def build_menu(self):
        """TODO:Build menu bar"""
        pass

    def build_task_container(self):
        """TODO:Build container for task list. Add scrollable canvas"""
        pass

    def build_detail_container(self):
        """TODO:Build container for task details"""
        pass

    def build_help_page(self):
        """TODO:Build help page"""
        # Move text to file
        pass

    def build_task_list(self):
        """TODO:Build task list for each task"""
        pass

    def build_task_details(self):
        """TODO:Build task details for each task"""
        pass

    def open_attribute_options(self, n):
        """TODO:Open attribute options for task n"""
        pass

    # Updating Data
    def fetch_tasks(self):
        """TODO:Fetch tasks from server"""
        pass

    def fetch_attributes(self):
        """TODO:Fetch attributes from server"""
        pass

    # Updating UI
    def update_list(self):
        """TODO:
        Update the task list to match server data.
        Checks if any tasks have been added, removed or updated
        """
        pass

    def update_details(self, n):
        """TODO:Update the task details to match server data"""
        pass

    def add_task(self):
        """TODO:Add new task to the server and UI"""
        pass

    def edit_task(self, n):
        """TODO:Toggle editing task"""
        pass

    def update_task(self, n):
        """TODO:Update UI to match task data"""
        pass

    def delete_task(self, n):
        """TODO:Delete task from server and UI"""
        pass

    def toggle_active(self, n):
        """TODO:Toggle task status"""
        # Change checkmark and colors
        pass

    def change_task(self, n):
        """TODO:Change the task being viewed"""
        pass

    def toggle_help(self):
        """TODO:Toggle help page"""
        pass

    def add_attribute(self, n, name, value):
        """TODO:Add attribute to task n"""
        pass

    def remove_attribute(self, n, index):
        """TODO:Remove attribute from task n"""
        pass

    def update_attribute(self, n, name, value):
        """TODO:Update attribute in task n"""
        pass


class Task:
    """TODO"""

    def __init__(self, client, task_id, name, date, description, attributes, status):
        self.client = client
        self.id = task_id
        self.name = name
        self.date = date
        self.description = description
        self.attributes = attributes
        self.status = status
        self.UI = {
            "list_item": self.build_list_item(self.client.UI["task_container"]),
            "detail_view": self.build_detail_view(self.client.UI["detail_container"]),
            "attribute_options": self.build_attribute_options(self.client.UI["detail_container"])
        }

    def __str__(self):
        return f"{self.name} - {self.date} - {self.description} - {self.attributes} - {self.status}"

    def __repr__(self):
        return f"{self.name} - {self.date} - {self.description} - {self.attributes} - {self.status}"

    # Update Data
    def edit(self, new_data) -> Self | None:
        """Edit task with new data
        :param new_data: The new data for the task. Will include the new name, date, description, and attributes
        :return: Updated task
        """
        # Compare new data to old data
        response = self.client.connection.put(f"tasks/{self.id}", new_data)
        if response["code"] == 200:
            for key, value in new_data.items():
                if self.__dict__[key] != value:
                    self.__dict__[key] = value
            return self
        else:
            print(f"Error updating task: {response["code"]} : {response["message"]}")
            return None

    def delete(self) -> bool:
        """Delete task from server
        :return: True if successful, False if not
        """
        response = self.client.connection.delete(f"tasks/{self.id}")
        if response["code"] == 200:
            self.client.tasks.remove(self)
            return True
        else:
            print("Error deleting task")
            return False

    def toggle_active(self) -> str:
        """Toggle task status between active and complete
        :return: New status
        """
        if self.status == "open":
            self.status = "closed"
        else:
            self.status = "open"
        self.edit({
            "status": self.status
        })
        return self.status

    # UI
    def build_list_item(self, parent) -> dict:
        """Build the list item that shows on the left side. Will include name, date, and attributes
        :param parent: Parent of the CtkButton
        :return: UI item
        """
        button = ctk.CTkButton(parent, command=lambda index=self.id: self.client.change_task(index), text="", width=400,
                               height=100)
        if self.status == "closed":
            button.configure(bg_color="gray20", fg_color="gray20")

        # Name for task title
        name = ctk.CTkLabel(button, text=f'{self.date} - {self.name}', font=("Arial", 20), padx=10, pady=10,
                            fg_color="transparent", bg_color="transparent")
        name.grid(row=0, column=0, sticky="nsw")
        # Bind the click event to the label, so you can click anywhere on the task
        name.bind("<Button-1>", lambda event, index=self.id: change_task(index))

        # Filler for checkmark and empty space
        filler = ctk.CTkLabel(button, text="", padx=10)
        if self.status == "closed":
            filler.configure(text="✓", font=("Arial", 20))
        filler.grid(row=1, column=0, sticky="w")

        # Attributes for task
        attr_list = ", ".join(attr.value for attr in self.attributes)
        attributes = ctk.CTkLabel(button, text=f'{attr_list}', font=("Arial", 20), padx=10, pady=10)
        attributes.grid(row=2, column=0, sticky="nsw")
        attributes.bind("<Button-1>", lambda event, index=self.id: change_task(index))

        return {
            "button": button,
            "filler": filler,
            "name": name,
            "attributes": attributes
        }

    def build_detail_view(self, parent):
        """TODO:Build task detail view"""
        pass

    def build_attribute_options(self, parent):
        """TODO:Build attribute options for task. Hide below task details"""
        # Grid frames for current attributes, existing attributes, and new attributes
        # Update value when closed
        pass

    # Manage Attributes
    def create_attribute(self, attr_id, name, value):
        """TODO:Create attribute for task"""
        pass

    def add_attribute(self, attr_id, value):
        """TODO:Add attribute to task"""
        # Build label and options
        pass

    def remove_attribute(self, attr_id):
        """TODO:Remove attribute from task"""
        pass

    def update_attribute(self, attr_id, value):
        """TODO:Update attribute with new value"""
        pass


class Attribute:
    """Attribute for tasks. Can belong to a task, or be standalone"""

    def __init__(self, client, attr_id, name, value, task=None):
        self.client = client
        self.id = attr_id
        self.name = name
        self.value = value
        self.task = task
        self.UI = {
            "label": self.build_label(self.task.UI["detail_view"]) if self.task is not None else None,
            "option": self.build_option(self.task.UI["detail_view"]) if self.task is not None else None
        }

    def __str__(self):
        return f"{self.name} - {self.value}"

    def __repr__(self):
        return f"{self.name} - {self.value}"

    def edit(self, new_value: str) -> Self | None:
        """Edit attribute value
        :param new_value: New value to replace previous
        :return: Updated attribute
        """
        response = self.client.connection.put(f"tasks/{self.task.id}/attributes", {"id": self.id, "value": new_value})
        if response["code"] == 200:
            self.value = new_value
            if self.task is not None:
                self.UI["label"].configure(text=f'{self.name}: {self.value}')
                self.UI["option"]["value"].delete("1.0", "end")
                self.UI["option"]["value"].insert("1.0", f'{self.value}')
            return self
        else:
            print("Error updating attribute")
            return None

    def update_value_temp(self, value: str):
        """Update the value of the attribute temporarily while typing
            :param value: The new value of the attribute
            """
        self.value = value

    def remove(self) -> bool:
        """Remove attribute from task
        :return: True if successful, False if not
        """
        if self.task is None:
            print("No task to remove attribute from")
            return False
        response = self.client.connection.delete(f"tasks/{self.task.id}/attributes/", {"id": self.id})
        if response["code"] == 200:
            self.task.attributes.remove(self)
            return True
        else:
            print("Error removing attribute")
            return False

    def delete(self) -> bool:
        """Delete attribute from server
        :return: True if successful, False if not
        """
        response = self.client.connection.delete(f"attributes/{self.id}")
        if response["code"] == 200:
            self.client.attributes.remove(self)
            return True
        else:
            print("Error deleting attribute")
            return False

    def build_label(self, parent) -> ctk.CTkLabel:
        """Build the label for the attribute
        :param parent: Parent of the label
        :return: Completed label
        """
        attr_text = f'{self.name}: {self.value}'
        attribute_label = ctk.CTkLabel(parent, text=attr_text, font=("Arial", 25),
                                       fg_color="gray20", corner_radius=10)
        return attribute_label

    def build_option(self, parent) -> dict:
        """Build the option for the attribute
        :param parent: Parent of the option
        :return: Completed option with all parts, and status. Will include frame, name, value, and remove button
        """
        if self.task is not None:
            attr_frame = ctk.CTkFrame(parent, bg_color="gray14", fg_color="gray14")
            attr_frame.columnconfigure(0, weight=1)
            attr_frame.columnconfigure(1, weight=1)
            attr_frame.columnconfigure(2, weight=1)

            attr_name = ctk.CTkLabel(attr_frame, text=f'{self.name}', font=("Arial", 25),
                                     fg_color="gray20", corner_radius=10, padx=10, pady=10)
            attr_name.grid(row=0, column=0, sticky="nsw", pady=10, padx=10)
            attr_value = ctk.CTkTextbox(attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
                                        fg_color="royal blue", wrap="none")
            # On Typing, update the attribute
            attr_value.bind("<KeyRelease>", lambda: self.update_value_temp(attr_value.get("1.0", "end-1c")))
            attr_value.insert('1.0', f'{self.value}')
            attr_value.grid(row=0, column=1, sticky="nsw", pady=10, padx=10)

            remove_button = ctk.CTkButton(attr_frame, text="Remove", font=("Arial", 25), width=80, bg_color="gray20")
            remove_button.grid(row=0, column=2, sticky="nsw", pady=10, padx=10)
            remove_button.bind("<Button-1>", lambda: self.task.remove_attribute(self.id))

            return {
                "type": "current",
                "frame": attr_frame,
                "name": attr_name,
                "value": attr_value,
                "remove": remove_button
            }
        else:
            attr_frame = ctk.CTkFrame(parent, bg_color="gray14", fg_color="gray14")
            attr_frame.columnconfigure(0, weight=1)
            attr_frame.columnconfigure(1, weight=1)
            attr_frame.columnconfigure(2, weight=1)

            attr_name = ctk.CTkTextbox(attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
                                       fg_color="gray20", wrap="none", corner_radius=10, )
            attr_name.insert('1.0', f'{self.name}')
            attr_name.grid(row=0, column=0, sticky="nsw", pady=10, padx=10)

            attr_value = ctk.CTkTextbox(attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
                                        fg_color="royal blue", wrap="none", corner_radius=10)
            attr_value.insert('1.0', "value")
            attr_value.grid(row=0, column=1, sticky="nsw", pady=10, padx=10)

            add_button = ctk.CTkButton(attr_frame, text="Add", font=("Arial", 25), width=80, bg_color="gray20")
            add_button.grid(row=0, column=2, sticky="nsw", pady=10, padx=10)
            add_button.bind("<Button-1>", lambda: self.task.add_attribute(self.id, attr_value.get("1.0", "end-1c")))
            return {
                "type": "new",
                "frame": attr_frame,
                "name": attr_name,
                "value": attr_value,
                "add": add_button
            }


class Connection:
    """The ZMQ Socket Connection to the server"""

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def get(self, path: str) -> dict:
        """Get data from server
        :param path: The path to the data to be accessed. Format will be [tasks|attributes]/[all|id]
        :return: Response from server
        """
        return self.request("get", path)

    def post(self, path: str, data: dict) -> dict:
        """Add data to server
        :param path: The path to the data to be added. Format will be [tasks|attributes]
        :param data: The data to be added. Will include the new data for the task or attribute
        :return: Response from server
        """
        return self.request("post", path, data)

    def put(self, path: str, data: dict) -> dict:
        """Update data on server
        :param path: The path to the data to be updated. Format will be [tasks|attributes]/[id]
        :param data: The data to be updated. Will include the new data for the task or attribute
        :return: Response from server
        """
        return self.request("put", path, data)

    def delete(self, path: str, data) -> dict:
        """Delete data from server
        :param path: The path to the data to be deleted. Format will be [tasks|attributes]/[id]
        :param data: The data to be deleted. Will be empty for most delete requests
        :return: Response from server
        """
        return self.request("delete", path, data)

    def request(self, action: str, path: str, data: dict = None) -> dict:
        """Send a request to server and return response
        :param action: The type of request to be made. Can be "get", "post", "put", or "delete"
        :param path: The path to the data to be accessed. Format will be [tasks|attributes]/[all|id]
        :param data: The data to be sent to the server. Will be empty for get and delete requests
        :return: The response from the server. Will include the data and a status code
        """
        payload = {
            "type": action,
            "path": path,
            "data": data
        }

        self.socket.send_string(json.dumps(payload))
        response = json.loads(self.socket.recv_string())
        print(f"Action {action} to {path} gave response: {response}")

        return response

# REMOVE
# client = Client(Connection())
# task = Task(client, 1, "Task 1", "2021-12-31", "This is a task", [], "open")
# attribute = Attribute(client, 1, "Attribute 1", "Value 1", task)
# task.attributes.append(attribute)
# print(task.attributes)
# attribute.remove()
# print(task.attributes)

context = zmq.Context()
print("Connecting to task server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# UI Setup and Shape
root = ctk.CTk()
root.configure(background="gray14")
root.geometry('1200x800')
# Adding columns and rows
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=50)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=20)

# Add container for tasks in left column
task_container = ctk.CTkFrame(root)
task_container.grid(row=1, column=0, sticky='nsew')
task_container.columnconfigure(0, weight=1)
task_container.rowconfigure(0, weight=1)
# Create a canvas that can be scrollable
left_canvas = ctk.CTkCanvas(task_container, bg="gray14", highlightthickness=0)
left_canvas.grid(row=0, column=0, sticky='nsew')
left_scrollbar = ctk.CTkScrollbar(task_container, orientation='vertical', command=left_canvas.yview)
left_scrollbar.grid(row=0, column=1, sticky='nsew')
left_canvas['yscrollcommand'] = left_scrollbar.set
left_canvas['yscrollincrement'] = 30
left_canvas.columnconfigure(0, weight=1)
left_canvas.rowconfigure(0, weight=1)
left_final_window = ctk.CTkFrame(left_canvas)
left_canvas.create_window((0, 0), window=left_final_window, anchor='nw', tags='expand1')
left_final_window.columnconfigure(0, weight=1)

left_canvas.bind('<Configure>', lambda event: left_canvas.itemconfigure('expand1', width=event.width))
left_final_window.update_idletasks()
left_canvas.config(scrollregion=left_canvas.bbox('all'))


def update_scrollregion_left(event):
    left_canvas.configure(scrollregion=left_canvas.bbox('all'))


left_final_window.bind('<Configure>', update_scrollregion_left)

# Add ability to scroll


# Creating details panel
right_container = ctk.CTkFrame(root, bg_color="gray14", fg_color="gray14")
right_container.grid(row=1, column=1, sticky='nsew')
right_container.columnconfigure(0, weight=1)
right_container.rowconfigure(0, weight=1)

right_canvas = ctk.CTkCanvas(right_container, bg="gray14", highlightthickness=0)
right_canvas.grid(row=0, column=0, sticky='nsew')

right_scrollbar = ctk.CTkScrollbar(right_container, orientation='vertical', command=right_canvas.yview)
right_scrollbar.grid(row=0, column=1, sticky='nsew')
right_canvas['yscrollcommand'] = right_scrollbar.set
right_canvas['yscrollincrement'] = 30
right_canvas.columnconfigure(0, weight=1)
right_canvas.rowconfigure(0, weight=1)
right_final_window = ctk.CTkFrame(right_canvas)
right_canvas.create_window((0, 0), window=right_final_window, anchor='nw', tags='expand')
right_final_window.columnconfigure(0, weight=1)

right_canvas.bind('<Configure>', lambda event: right_canvas.itemconfigure('expand', width=event.width))
right_final_window.update_idletasks()
right_canvas.config(scrollregion=right_canvas.bbox('all'))


def update_scrollregion_right(event):
    right_canvas.configure(scrollregion=right_canvas.bbox('all'))


right_final_window.bind('<Configure>', update_scrollregion_right)


def scroll(event, widget):
    widget.yview_scroll(int(-1 * (event.delta / 120)), "units")


def final_scroll(event, widget, func):
    widget.bind_all("<MouseWheel>", func)


def stop_scroll(event, widget):
    widget.unbind_all("<MouseWheel>")


# Make sure scrolling happens in the right place
left_canvas.bind("<Enter>", lambda event: final_scroll(event, left_canvas, lambda event: scroll(event, left_canvas)))
left_canvas.bind("<Leave>", lambda event: stop_scroll(event, left_canvas))

right_canvas.bind("<Enter>", lambda event: final_scroll(event, right_canvas, lambda event: scroll(event, right_canvas)))
right_canvas.bind("<Leave>", lambda event: stop_scroll(event, right_canvas))


def fetch_tasks():
    # Get Tasks
    payload = {
        "type": "get",
        "path": "tasks/all",
        "data": ""
    }
    socket.send_string(json.dumps(payload))

    response = json.loads(socket.recv_string())
    print(f"Fetching tasks gave response: {response}")

    if response["response"] == 400:
        print("Server Error")
        tasks = []
    else:
        tasks = response["response"]
    return tasks


def fetch_attributes():
    payload = {
        "type": "get",
        "path": "attributes/all",
        "data": ""
    }
    socket.send_string(json.dumps(payload))

    response = json.loads(socket.recv_string())
    print(f"Fetching attributes gave response: {response}")

    if response["response"] == 400:
        print("Server Error")
        attributes = []
    else:
        attributes = response["response"]
    return attributes


tasks = fetch_tasks()
attribute_list = fetch_attributes()

# Help Page
help_page = ctk.CTkFrame(right_final_window, bg_color="gray14", fg_color="gray14")
help_page.grid(row=1, column=0, columnspan=4, sticky='nsew')
help_page.columnconfigure(0, weight=1)
help_page.rowconfigure(0, weight=1)
help_page.rowconfigure(1, weight=2)
help_page.rowconfigure(2, weight=1)
help_page.rowconfigure(3, weight=2)

info_text = '''View
- You are now able to view all of your tasks on the main page, 
  and you can click on a task to show more of its details
Add
- You are now able to add more tasks, from a button on the main page.
- When adding a task, the parts you need to fill out are highlighted in blue.
- If you want, you can add attributes to your tasks to better categorize them.
Edit
- You are now able to edit tasks, and change change any of the details that 
  you added originally, like attributes, or the date.'''

help_text = '''Viewing
- To view a task, click on the task in the list on the left.
- The task details will appear on the right.
- If you want to see more tasks, you can scroll through the list on the left.
Adding
- To add a task, click the "Add Task" button on the main page.
- Fill out the name, date, and description of the task.
- If you want, you can add attributes to your task to better categorize it.
- Attributes can be things like "Urgency", "Importance", or "Type".
- To add an attribute, click the "Attributes" button on the task detail view.
- You can add new attributes, or existing ones in other tasks.
Editing
- To edit a task, click the "Edit" button on the task detail view.
- You can change the name, date, description, and attributes of the task.
- To edit an attribute, click the "Attributes" button on the task detail view.
- You can change the value of the attribute.
- To remove an attribute, click the "Remove" button next to the attribute.
- To add an attribute, click the "Add" button next to the attribute, which can be an existing one, or brand new.
- To save your changes, click the "Save" button on the task detail view.
'''

# New Info
new_title = ctk.CTkLabel(help_page, text="What's New?", font=("Arial", 30), bg_color="gray14", fg_color="gray14",
                         height=2)
new_title.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
new_info = ctk.CTkTextbox(help_page, font=("Arial", 20), bg_color="gray14", fg_color="gray14",
                          width=700, spacing1=10, height=400, activate_scrollbars=False)
new_info.insert('1.0', info_text)
new_info.configure(state="disabled")
new_info.grid(row=1, column=0, sticky="nsw", padx=10)
# Help
help_title = ctk.CTkLabel(help_page, text="Help", font=("Arial", 30), bg_color="gray14", fg_color="gray14", height=2)
help_title.grid(row=2, column=0, sticky="nsw", padx=10, pady=10)
help_info = ctk.CTkTextbox(help_page, font=("Arial", 20), bg_color="gray14", fg_color="gray14",
                           width=700, spacing1=10, height=1000, activate_scrollbars=False)
help_info.insert('1.0', help_text)
help_info.configure(state="disabled")
help_info.grid(row=3, column=0, sticky="nsw", padx=10)

# Create a dictionary to store the state of each textbox

textbox_states = {}


def edit_task(n):
    name, date, description, attributes, attribute_label, complete, edit_button = task_detail_frames[n][1].values()
    # If the textbox is not in the dictionary, assume it is disabled
    if textbox_states.get(name, "disabled") == "normal":
        payload = {
            "type": "put",
            "path": f"tasks/{n + 1}",
            "data": {
                "id": n + 1,
                "name": name.get("1.0", "end-1c"),
                "date": date.get("1.0", "end-1c"),
                "description": description.get("1.0", "end-1c"),
                "attributes": tasks[n]["attributes"],
                "status": "closed" if complete.get() else "open"
            }
        }
        socket.send_string(json.dumps(payload))
        response = json.loads(socket.recv_string())
        print(f"Editing task {n + 1} gave response: {response}")
        for task_detail in task_detail_frames:
            task_detail[0].destroy()
        task_detail_frames.clear()
        build_task_details()
        build_task_list()
        change_task(n)
    else:
        name.configure(state="normal", fg_color="royal blue")
        name.focus_set()
        date.configure(state="normal", fg_color="royal blue")
        description.configure(state="normal", fg_color="royal blue")
        attribute_label.configure(state="normal", fg_color="royal blue")
        # Update the states in the dictionary
        textbox_states[name] = "normal"
        textbox_states[date] = "normal"
        textbox_states[description] = "normal"
        edit_button.configure(text="Save")


attribute_options = [None for _ in range(1000)]


def build_attribute_options(n):
    name, date, description, attributes, attribute_label, complete, edit_button = task_detail_frames[n][1].values()
    print("Building attribute options", tasks[n]["attributes"], n)
    if attribute_options[n] is not None:
        # Close Menu
        for attr in attributes:
            attr.tkraise()
        attribute_options[n].destroy()
        attribute_options[n] = None
        edit_button.configure(state="normal")
    else:
        edit_button.configure(state="disabled")
        attr_options_frame = ctk.CTkFrame(task_detail_frames[n][0], bg_color="gray14", fg_color="gray14")
        attribute_options[n] = attr_options_frame
        attributes = task_detail_frames[n][1]["attributes"]
        for attr in attributes:
            attr.lower()
        attr_options_frame.grid(row=3, column=0, columnspan=3, rowspan=3, sticky="nsw")
        attr_options_frame.columnconfigure(0, weight=1)
        attr_options_frame.columnconfigure(1, weight=1)
        attr_options_frame.columnconfigure(2, weight=1)
        # Current Attr Label
        current_attr_label = ctk.CTkLabel(attr_options_frame, text="Current Attributes", font=("Arial", 30), padx=15)
        current_attr_label.grid(row=0, column=0, sticky="nsw")
        # Current Attributes
        max_i = 0
        for i, attr in enumerate(tasks[n]["attributes"]):
            # attr_frame = ctk.CTkFrame(attr_options_frame, bg_color="gray14", fg_color="gray14")
            # attr_frame.grid(row=i + 1, column=0, columnspan=3, sticky="nsw")
            # attr_frame.columnconfigure(0, weight=1)
            # attr_frame.columnconfigure(1, weight=1)
            # attr_frame.columnconfigure(2, weight=1)
            # attr_name = ctk.CTkLabel(attr_frame, text=f'{attr["name"]}', font=("Arial", 25),
            #                             fg_color="gray20", corner_radius=10, padx=10, pady=10)
            # attr_name.grid(row=0, column=0, sticky="nsw", pady=10, padx=10)
            # attr_value = ctk.CTkTextbox(attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
            #                             fg_color="royal blue", wrap="none")
            # # On Typing, update the attribute
            # attr_value.bind("<KeyRelease>", lambda event, index=i: update_attribute(n, attr["name"] , attr_value.get(
            #     "1.0",
            #                                                                                              "end-1c")))
            # attr_value.insert('1.0', f'{attr["value"]}')
            # attr_value.grid(row=0, column=1, sticky="nsw", pady=10, padx=10)
            # remove_button = ctk.CTkButton(attr_frame, text="Remove", font=("Arial", 25), width=80, bg_color="gray20")
            # remove_button.grid(row=0, column=2, sticky="nsw", pady=10, padx=10)
            # remove_button.bind("<Button-1>", lambda event, index=i: remove_attribute(n, index))
            max_i = i

        # Existing Attributes & Label
        existing_attributes = []
        for i, attr in enumerate(attribute_list):
            if attr["name"] not in [a["name"] for a in tasks[n]["attributes"]]:
                existing_attributes.append(attr)
        if len(existing_attributes) > 0:
            existing_attr_label = ctk.CTkLabel(attr_options_frame, text="Existing Attributes", font=("Arial", 30),
                                               padx=15)
            existing_attr_label.grid(row=max_i + 2, column=0, sticky="nsw")
            for i, attr in enumerate(existing_attributes):
                # attr_frame = ctk.CTkFrame(attr_options_frame, bg_color="gray14", fg_color="gray14")
                # attr_frame.grid(row=max_i + i + 3, column=0, columnspan=3, sticky="nsw")
                # attr_frame.columnconfigure(0, weight=1)
                # attr_frame.columnconfigure(1, weight=1)
                # attr_frame.columnconfigure(2, weight=1)
                # attr_name = ctk.CTkTextbox(attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
                #                             fg_color="gray20", wrap="none", corner_radius=10,)
                # attr_name.insert('1.0', f'{attr["name"]}')
                # attr_name.grid(row=0, column=0, sticky="nsw", pady=10, padx=10)
                # attr_value = ctk.CTkTextbox(attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
                #                             fg_color="royal blue", wrap="none", corner_radius=10)
                # attr_value.insert('1.0', "value")
                # attr_value.grid(row=0, column=1, sticky="nsw", pady=10, padx=10)
                # add_button = ctk.CTkButton(attr_frame, text="Add", font=("Arial", 25), width=80, bg_color="gray20")
                # add_button.grid(row=0, column=2, sticky="nsw", pady=10, padx=10)
                # add_button.bind("<Button-1>", lambda event, index=i: add_attribute(n, attr_name.get("1.0", "end-1c"), attr_value.get("1.0", "end-1c")))
                max_i = i
            max_i += 2

        # New Attr Label (Just 2 blank textboxes and a button to add. If one is added, add another)
        new_attr_label = ctk.CTkLabel(attr_options_frame, text="New Attributes", font=("Arial", 30), padx=15)
        new_attr_label.grid(row=max_i + 4, column=0, sticky="nsw")
        new_attr_frame = ctk.CTkFrame(attr_options_frame, bg_color="gray14", fg_color="gray14")
        new_attr_frame.grid(row=max_i + 5, column=0, columnspan=3, sticky="nsw")
        new_attr_frame.columnconfigure(0, weight=1)
        new_attr_frame.columnconfigure(1, weight=1)
        new_attr_frame.columnconfigure(2, weight=1)
        new_attr_name = ctk.CTkTextbox(new_attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
                                       fg_color="royal blue", wrap="none", corner_radius=10)
        new_attr_name.insert('1.0', "name")
        new_attr_name.grid(row=0, column=0, sticky="nsw", pady=10, padx=10)
        new_attr_value = ctk.CTkTextbox(new_attr_frame, font=("Arial", 25), border_width=0, height=1, width=150,
                                        fg_color="royal blue", wrap="none", corner_radius=10)
        new_attr_value.insert('1.0', "value")
        new_attr_value.grid(row=0, column=1, sticky="nsw", pady=10, padx=10)
        add_button = ctk.CTkButton(new_attr_frame, text="Add", font=("Arial", 25), width=80, bg_color="gray14",
                                   corner_radius=10)
        add_button.grid(row=0, column=2, sticky="nsw")
        add_button.bind("<Button-1>", lambda event: add_attribute(n, new_attr_name.get("1.0", "end-1c"),
                                                                  new_attr_value.get("1.0", "end-1c")))
        max_i += 1
        attr_options_frame.rowconfigure(index=max_i + 5, weight=1, uniform="row")
        attr_options_frame.grid(row=3, column=0, columnspan=3, rowspan=3, sticky="nsw")


def update_attribute(n, name, value):
    print("Updating attribute")
    # Get attribute with name
    for i, attr in enumerate(tasks[n]["attributes"]):
        if attr["name"] == name:
            tasks[n]["attributes"][i]["value"] = value
            payload = {
                "type": "put",
                "path": f"tasks/{n + 1}",
                "data": {
                    "id": n + 1,
                    "name": task_detail_frames[n][1]["name"].get("1.0", "end-1c"),
                    "date": task_detail_frames[n][1]["date"].get("1.0", "end-1c"),
                    "description": task_detail_frames[n][1]["description"].get("1.0", "end-1c"),
                    "attributes": tasks[n]["attributes"],
                    "status": tasks[n]["status"]
                }
            }
            socket.send_string(json.dumps(payload))
            response = json.loads(socket.recv_string())
            print(f"Updating attribute {name} to {value} gave response: {response}")
            break


def add_attribute(n, name, value):
    tasks[n]["attributes"].append({
        "name": name,
        "value": value
    })
    attribute_list.append({
        "name": name
    })
    # If attribute not in db, add it
    if name not in [attr["name"] for attr in attribute_list]:
        payload = {
            "type": "post",
            "path": "attributes/",
            "data": {
                "name": name
            }
        }
        socket.send_string(json.dumps(payload))
        response = json.loads(socket.recv_string())
        print(f"Adding attribute {name}, with value {value} gave response: {response}")
    attribute_options[n].destroy()
    attribute_options[n] = None
    build_attribute_options(n)


def remove_attribute(n, index):
    attr_name = tasks[n]["attributes"][index]["name"]
    tasks[n]["attributes"].pop(index)
    payload = {
        "type": "put",
        "path": f"tasks/{n + 1}",
        "data": {
            "id": n + 1,
            "name": task_detail_frames[n][1]["name"].get("1.0", "end-1c"),
            "date": task_detail_frames[n][1]["date"].get("1.0", "end-1c"),
            "description": task_detail_frames[n][1]["description"].get("1.0", "end-1c"),
            "attributes": tasks[n]["attributes"],
            "status": tasks[n]["status"]
        }
    }
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    print(f"Removing attribute {attr_name} gave response: {response}")
    attribute_options[n].destroy()
    attribute_options[n] = None
    build_attribute_options(n)


# Add tasks to right side

task_detail_frames = []

extra_space = ctk.CTkLabel(right_final_window, text="", bg_color="gray14", fg_color="gray14", height=500)
extra_space.grid(row=0, rowspan=3, column=0, columnspan=4, sticky="nsew")


def build_task_details():
    print("Building Task Details")
    extra_space.tkraise()
    for i in range(len(tasks)):
        # Create a new frame for the task detail view and add it to the list
        task_detail_frame = ctk.CTkFrame(right_final_window, bg_color="gray14", fg_color="gray14", height=800)

        task_detail_frame.columnconfigure(index=0, weight=1, uniform="column")
        task_detail_frame.columnconfigure(index=1, weight=1)
        task_detail_frame.columnconfigure(index=2, weight=1, uniform="column")
        task_detail_frame.rowconfigure(index=0, weight=1)
        task_detail_frame.rowconfigure(index=1, weight=1)

        # Name Frame
        name_frame = ctk.CTkFrame(task_detail_frame, bg_color="gray14", fg_color="gray14")
        name_frame.grid(row=0, column=0, sticky="nsw")
        name_frame.columnconfigure(0, weight=1)
        name_frame.columnconfigure(1, weight=1)

        # Name Label
        name_label = ctk.CTkLabel(name_frame, text=f'Task {tasks[i]["id"]} - ', font=("Arial", 30))

        # Name Textbox
        task_name = ctk.CTkTextbox(name_frame, font=("Arial", 30), border_width=0,
                                   height=1, width=300, fg_color="gray14", wrap="none")
        task_name.insert('1.0', f'{tasks[i]["name"]}')
        task_name.configure(state="disabled")
        task_name.grid(row=0, column=1, sticky="nsw", pady=10)

        name_label.grid(row=0, column=0, sticky="nsw", padx=(10, 0))

        # Completion Checkbox
        complete_frame = ctk.CTkFrame(task_detail_frame, fg_color="gray14", width=100)
        complete_text = ctk.CTkLabel(complete_frame, text="Complete ", font=("Arial", 30))
        task_var = ctk.BooleanVar(value=True if tasks[i]["status"] == "closed" else False)
        complete_box = ctk.CTkCheckBox(complete_frame, variable=task_var, command=lambda index=i: toggle_active(index),
                                       text="",
                                       checkbox_width=30,
                                       checkbox_height=30)
        complete_text.grid(column=0, row=0, sticky="nsew", pady=10)
        complete_box.grid(column=1, row=0, sticky="nsew")
        complete_frame.grid(column=1, row=0, sticky="nsw", pady=10, padx=10)

        # Editing Button
        edit_button = ctk.CTkButton(task_detail_frame, text="Edit", command=lambda index=i: edit_task(index),
                                    font=("Arial", 30), width=80, bg_color="gray20")
        edit_button.grid(column=2, row=0, sticky="nsw", pady=10)

        # Date
        date = ctk.CTkTextbox(task_detail_frame, font=("Arial", 30), border_width=0, height=1,
                              width=175,
                              fg_color="gray20", wrap="none")
        date.insert('1.0', tasks[i]["date"])
        date.configure(state="disabled")
        date.grid(row=1, column=0, columnspan=3, sticky="nsw", padx=15, pady=10)

        # Attribute Label
        attribute_label = ctk.CTkButton(task_detail_frame, text="Attributes", font=("Arial", 30), command=lambda
            index=i: build_attribute_options(index), state="disabled", bg_color="gray14", fg_color="gray14")
        attribute_label.grid(row=2, column=0, columnspan=3, sticky="nsw", pady=10, padx=15)
        # Attributes
        max_j = 0
        attributes = []
        for j, attr in enumerate(tasks[i]["attributes"]):
            # attr_text = f'{attr["name"].strip()}: {attr["value"].strip()}'
            # attribute = ctk.CTkLabel(task_detail_frame, text=attr_text, font=("Arial", 25),
            #                                fg_color="gray20", corner_radius=10)
            # attribute.grid(row=3+j, column=0, columnspan=3, sticky="nsw", pady=10, padx=10)
            # attributes.append(attribute)
            task_detail_frame.rowconfigure(index=3 + j, weight=1, uniform="row")
            max_j = j

        # Description Label
        description_label = ctk.CTkLabel(task_detail_frame, text="Description", font=("Arial", 30), padx=15)
        description_label.grid(row=max_j + 4, column=0, columnspan=3, sticky="nsw")
        # Description
        description = ctk.CTkTextbox(task_detail_frame, font=("Arial", 20), padx=15, wrap='word', width=800,
                                     height=300, spacing2=10)
        description.insert('1.0', tasks[i]["description"])
        description.configure(state="disabled")
        description.grid(row=max_j + 5, column=0, columnspan=3, sticky="nsw", padx=15, pady=10)

        # Create a Scrollbar and attach it to the Text widget
        scrollbar = ctk.CTkScrollbar(task_detail_frame, command=description.yview)
        scrollbar.grid(row=max_j + 5, column=3, sticky='nsew')
        description['yscrollcommand'] = scrollbar.set

        task_detail_frame.rowconfigure(index=max_j + 4, weight=1)
        task_detail_frame.rowconfigure(index=max_j + 5, weight=1)

        task_detail_frame.grid(row=1, column=1, columnspan=3, sticky='new')
        task_detail_frames.append((task_detail_frame, {
            "name": task_name,
            "date": date,
            "description": description,
            "attributes": attributes,
            "attribute_label": attribute_label,
            "complete": task_var,
            "edit_button": edit_button

        }))


def toggle_active(n):
    if task_detail_frames[n][1]["complete"].get():
        payload = {
            "type": "put",
            "path": f"tasks/{n + 1}",
            "data": {
                "id": n + 1,
                "name": tasks[n]["name"],
                "date": tasks[n]["date"],
                "description": tasks[n]["description"],
                "attributes": tasks[n]["attributes"],
                "status": "closed"
            }
        }
    else:
        payload = {
            "type": "put",
            "path": f"tasks/{n + 1}",
            "data": {
                "id": n + 1,
                "name": tasks[n]["name"],
                "date": tasks[n]["date"],
                "description": tasks[n]["description"],
                "attributes": tasks[n]["attributes"],
                "status": "open"
            }
        }
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    build_task_list()
    print(f"Toggle Task {n + 1} gave response: {response}")


def add_task():
    new_task = {
        "id": len(tasks) + 1,
        "name": "New Task Name",
        "date": "2024/01/01",
        "description": "New Description",
        "attributes": [],
        "status": "open"
    }
    tasks.append(new_task)
    payload = {
        "type": "post",
        "path": "tasks/",
        "data": new_task
    }
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    print(f"Add task gave response: {response}")
    for task_detail in task_detail_frames:
        task_detail[0].destroy()
    task_detail_frames.clear()
    build_task_details()
    build_task_list()
    change_task(len(tasks) - 1)
    edit_task(len(tasks) - 1)


def open_help():
    help_page.tkraise()


def change_task(n):
    # Bring the frame of the selected task detail view to the top
    extra_space.tkraise()
    task_detail_frames[n][0].tkraise()


task_buttons = []


def build_task_list():
    print("Building Task List")
    for button in task_buttons:
        button.destroy()
    task_buttons.clear()
    # Create Tasks on left side
    tasks = fetch_tasks()
    button_queue_disabled = []
    button_queue = []
    # for i in range(len(tasks)):

    # button = ctk.CTkButton(left_final_window, command=lambda index=i: change_task(index), text="", width=400,
    #                        height=100)
    # if tasks[i]["status"] == "closed":
    #     button.configure(bg_color="gray20", fg_color="gray20")
    #     button_queue_disabled.append(button)
    # else:
    #     button_queue.append(button)
    # name = ctk.CTkLabel(button, text=f'{tasks[i]["date"]} - {tasks[i]["name"]}', font=("Arial", 20), padx=10, pady=10,
    #                           fg_color="transparent", bg_color="transparent")
    # name.grid(row=0, column=0, sticky="nsw")
    # name.bind("<Button-1>", lambda event, index=i: change_task(index))  # Bind the click event to the label
    # filler = ctk.CTkLabel(button, text="", padx=10)
    # if tasks[i]["status"] == "closed":
    #     filler.configure(text="✓", font=("Arial", 20))
    # filler.grid(row=1, column=0, sticky="w")
    # attr_list = ", ".join(attr["value"] for attr in tasks[i]["attributes"])
    # attributes = ctk.CTkLabel(button, text=f'{attr_list}', font=("Arial", 20), padx=10, pady=10)
    # attributes.grid(row=2, column=0, sticky="nsw")
    # attributes.bind("<Button-1>", lambda event, index=i: change_task(index))
    # task_buttons.append(button)
    i = 0
    for button in button_queue:
        button.grid(row=i, column=0, sticky="nsew", pady=1)
        i += 1
    for button in button_queue_disabled:
        button.grid(row=i, column=0, sticky="nsew", pady=1)
        i += 1


build_task_list()
build_task_details()
change_task(0)

# Add menu
menu_bar = ctk.CTkFrame(root)
menu_bar.grid(row=0, column=0, columnspan=4, sticky='nsew')

# Sort & Filter
sorting_button = ctk.CTkButton(menu_bar, text="Sort and Filter", font=("Arial", 20), width=40, height=20)
sorting_button.grid(row=0, column=0, sticky="nsw", pady=10, padx=10)

# Add
add_task_button = ctk.CTkButton(menu_bar, text="Add Task", font=("Arial", 20), width=20, height=20, command=add_task)
add_task_button.grid(row=0, column=2, sticky="nsw", pady=10, padx=10)

# Help Button
help_button = ctk.CTkButton(menu_bar, text="What's New? / Help", font=("Arial", 20), width=20, height=20,
                            command=open_help)
help_button.grid(row=0, column=4, sticky="nsew", pady=10, padx=10)

# Config menu bar grid
menu_bar.columnconfigure(0, weight=1)
menu_bar.columnconfigure(1, weight=1)
menu_bar.columnconfigure(2, weight=4)
menu_bar.columnconfigure(3, weight=4)
menu_bar.columnconfigure(4, weight=1)

root.mainloop()