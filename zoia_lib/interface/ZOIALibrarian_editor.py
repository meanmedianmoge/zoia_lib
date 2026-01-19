import datetime
import json
import os
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QMainWindow,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QStyle,
    QStylePainter,
    QStyleOptionComboBox,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QGroupBox,
    QScrollArea,
    QFormLayout,
    QSplitter,
)
from PySide6.QtCore import Qt
from NodeGraphQt import NodeGraph, BaseNode, setup_context_menu
from zoia_lib.backend.patch_binary import PatchBinary
from zoia_lib.backend.patch_encode import PatchEncoder
from zoia_lib.backend.utilities import exit_after, meipass

class PatchBuilderEditor(QMainWindow):
    """Separate window for building a patch by selecting modules and configuring them."""
    def __init__(self, msg=None, save=None, window=None, patch_dict=None, patch_id=None, on_close=None):
        super().__init__(window)
        self.setWindowTitle("ZOIA Patch Builder")
        self.resize(1300, 700)
        self.msg = msg
        self.window = window
        self.patch_dict = patch_dict  # For editing existing patches
        self.patch_id = patch_id
        self.on_close = on_close
        self._refreshed = False
        self.param_controls = {}  # Store references to parameter sliders/spinboxes
        self.current_module_index = None
        self.patch_save = save

        # Load module index
        with open(meipass("zoia_lib/common/schemas/ModuleIndex.json")) as f:
            self.module_index = json.load(f)
        self._patch_binary = PatchBinary()

        self.selected_modules = []  # List of (module_id, config_dict)
        self.connections = []

        # Create main container to hold everything
        main_container = QWidget()
        container_layout = QVBoxLayout(main_container)
        
        # Create the main layout for modules and details
        main_layout = QHBoxLayout()

        # Module list
        module_list_layout = QVBoxLayout()
        module_label = QLabel("Available Modules:")
        self.module_list = QTreeWidget()
        self.module_list.setHeaderHidden(True)
        categories = {}
        for mod_id, mod in self.module_index.items():
            name = mod.get("name", "")
            if "euro" in name.lower():
                continue
            category = mod.get("category", "Uncategorized")
            if category not in categories:
                categories[category] = QTreeWidgetItem([category])
                categories[category].setData(0, 1, "category")
                self.module_list.addTopLevelItem(categories[category])
            child = QTreeWidgetItem([mod["name"]])
            child.setData(0, 1, mod_id)
            categories[category].addChild(child)
        # self.module_list.expandAll()
        module_list_layout.addWidget(module_label)
        module_list_layout.addWidget(self.module_list)
        self.add_module_btn = QPushButton("Add Module to Patch →")
        module_list_layout.addWidget(self.add_module_btn)
        self.insert_module_btn = QPushButton("Insert Module Before Selected →")
        module_list_layout.addWidget(self.insert_module_btn)
        main_layout.addLayout(module_list_layout)

        # Selected modules
        selected_layout = QVBoxLayout()
        selected_label = QLabel("Patch Modules:")
        self.selected_list = QListWidget()
        selected_layout.addWidget(selected_label)
        selected_layout.addWidget(self.selected_list)
        self.order_audio_btn = QPushButton("Order by Audio Path")
        selected_layout.addWidget(self.order_audio_btn)
        self.remove_module_btn = QPushButton("Remove Selected Module")
        selected_layout.addWidget(self.remove_module_btn)
        main_layout.addLayout(selected_layout)

        # Module details panel (right side)
        details_layout = QVBoxLayout()
        details_label = QLabel("Module Details:")
        self.details_scroll = QScrollArea()
        self.details_scroll.setWidgetResizable(True)
        details_widget = QWidget()
        self.details_layout = QVBoxLayout(details_widget)
        self.details_layout.addStretch()
        self.details_scroll.setWidget(details_widget)
        details_layout.addWidget(details_label)
        details_layout.addWidget(self.details_scroll)
        main_layout.addLayout(details_layout)

        # Build routing view container
        routing_container = QWidget()
        self.routing_layout = QVBoxLayout(routing_container)
        routing_header = QLabel("Patch Routing View")
        self.routing_layout.addWidget(routing_header)
        self.routing_placeholder = QLabel("No routing data to display.")
        self.routing_layout.addWidget(self.routing_placeholder)
        self.routing_graph = None
        self.routing_graph_widget = None
        self.routing_container = routing_container
        self.routing_container.setVisible(False)

        # Split main layout and routing view
        main_panel = QWidget()
        main_panel.setLayout(main_layout)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(main_panel)
        self.splitter.addWidget(routing_container)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 3)

        # Add splitter to container
        container_layout.addWidget(self.splitter, 1)

        # Bottom button layout
        bottom_layout = QHBoxLayout()
        self.toggle_routing_btn = QPushButton("Toggle Routing View")
        self.export_btn = QPushButton("Export Patch")
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.toggle_routing_btn)
        bottom_layout.addWidget(self.export_btn)
        container_layout.addLayout(bottom_layout, 0)
        
        # Set the main container as central widget
        self.setCentralWidget(main_container)

        # Connections
        self.add_module_btn.clicked.connect(self.add_selected_module)
        self.insert_module_btn.clicked.connect(self.insert_selected_module)
        self.remove_module_btn.clicked.connect(self.remove_selected_module)
        self.selected_list.itemSelectionChanged.connect(self.on_module_selected)
        self.export_btn.clicked.connect(self.export_patch)
        self.toggle_routing_btn.clicked.connect(self.toggle_routing_view)
        self.order_audio_btn.clicked.connect(self.order_by_audio_path)
        
        # If editing an existing patch, load its modules
        if self.patch_dict:
            self.setWindowTitle("ZOIA Patch Editor")
            self.connections = list(self.patch_dict.get("connections", []))
            self._load_patch_modules()
        else:
            self.connections = []
            self._init_new_patch_defaults()

    def add_selected_module(self):
        item = self.module_list.currentItem()
        if not item:
            return
        mod_id = item.data(0, 1)
        if mod_id == "category" or mod_id is None:
            return
        mod = self.module_index[mod_id]
        # For now, just add with default config
        insert_row = len(self.selected_modules)
        config = self._default_module_config(mod_id)
        self._assign_module_position(config, mod_id=mod_id)
        self.selected_modules.append((mod_id, config))
        self.selected_list.addItem(f"{mod['name']} ({mod['category']})")
        self.selected_list.setCurrentRow(insert_row)
        self._refresh_routing_view()

    def insert_selected_module(self):
        item = self.module_list.currentItem()
        if not item:
            return
        mod_id = item.data(0, 1)
        if mod_id == "category" or mod_id is None:
            return
        insert_row = self.selected_list.currentRow()
        if insert_row < 0:
            insert_row = len(self.selected_modules)
        mod = self.module_index[mod_id]
        config = self._default_module_config(mod_id)
        preferred_start = 0
        preferred_page = 0
        if 0 <= insert_row < len(self.selected_modules):
            ref_cfg = self.selected_modules[insert_row][1]
            if ref_cfg.get("position"):
                preferred_start = ref_cfg["position"][0]
            preferred_page = ref_cfg.get("page", 0)
        self._assign_module_position(
            config, mod_id=mod_id, preferred_start=preferred_start, preferred_page=preferred_page
        )
        self.selected_modules.insert(insert_row, (mod_id, config))
        self.selected_list.insertItem(insert_row, f"{mod['name']} ({mod['category']})")
        self._shift_connections(insert_row, 1)
        self.selected_list.setCurrentRow(insert_row)
        self._refresh_routing_view()

    def remove_selected_module(self):
        """Remove the currently selected module from the patch."""
        current_row = self.selected_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a module to remove.")
            return
        self.selected_list.takeItem(current_row)
        self.selected_modules.pop(current_row)
        self._shift_connections(current_row, -1)
        self.clear_module_details()
        self._refresh_routing_view()

    def on_module_selected(self):
        """Handle module selection in the selected list."""
        current_row = self.selected_list.currentRow()
        if current_row < 0:
            self.clear_module_details()
            return
        
        self.current_module_index = current_row
        mod_id, config = self.selected_modules[current_row]
        self.show_module_details(mod_id, config, current_row)

    def show_module_details(self, mod_id, config, module_index):
        """Display details and editable parameters for the selected module."""
        self._reset_details_container()

        # Clear parameter control references
        self.param_controls = {}

        mod = self.module_index[mod_id]

        # Module info header
        info_label = QLabel(f"<b>{mod['name']}</b>\nCategory: {mod['category']}")
        self.details_layout.addWidget(info_label)

        # CPU info
        cpu_label = QLabel(f"CPU: {mod['cpu']}")
        self.details_layout.addWidget(cpu_label)

        options_group = self._build_options_section(mod_id, config, module_index)
        if options_group:
            self.details_layout.addWidget(options_group)

        params_group = self._build_params_section(mod_id, config, module_index)
        if params_group:
            self.details_layout.addWidget(params_group)

        connections_group = self._build_connections_section(module_index)
        if connections_group:
            self.details_layout.addWidget(connections_group)

        self.details_layout.addStretch()

    def on_parameter_changed(self, value):
        """Handle parameter value changes."""
        sender = self.sender()
        param_name = sender.property("param_name")
        module_index = sender.property("module_index")
        
        if module_index >= 0 and module_index < len(self.selected_modules):
            mod_id, config = self.selected_modules[module_index]
            
            # Ensure config has parameters dict
            if "parameters" not in config:
                config["parameters"] = {}
            
            # Update parameter value (normalize to 0.0-1.0)
            if isinstance(sender, QSlider):
                normalized_value = value / 100.0
            else:  # QDoubleSpinBox
                normalized_value = value
            
            config["parameters"][param_name] = normalized_value

    def on_parameter_slider_changed(self, value):
        """Handle slider changes and update spinbox in real time."""
        sender = self.sender()
        param_name = sender.property("param_name")
        module_index = sender.property("module_index")
        
        # Update config
        if module_index >= 0 and module_index < len(self.selected_modules):
            mod_id, config = self.selected_modules[module_index]
            if "parameters" not in config:
                config["parameters"] = {}
            normalized_value = value / 100.0
            config["parameters"][param_name] = normalized_value
        
        # Update spinbox without triggering its signal
        control_key = f"{module_index}_{param_name}"
        if control_key in self.param_controls:
            spinbox = self.param_controls[control_key]["spinbox"]
            spinbox.blockSignals(True)
            spinbox.setValue(value / 100.0)
            spinbox.blockSignals(False)

    def on_parameter_spinbox_changed(self, value):
        """Handle spinbox changes and update slider in real time."""
        sender = self.sender()
        param_name = sender.property("param_name")
        module_index = sender.property("module_index")
        
        # Update config
        if module_index >= 0 and module_index < len(self.selected_modules):
            mod_id, config = self.selected_modules[module_index]
            if "parameters" not in config:
                config["parameters"] = {}
            config["parameters"][param_name] = value
        
        # Update slider without triggering its signal
        control_key = f"{module_index}_{param_name}"
        if control_key in self.param_controls:
            slider = self.param_controls[control_key]["slider"]
            slider.blockSignals(True)
            slider.setValue(int(value * 100))
            slider.blockSignals(False)

    def clear_module_details(self):
        """Clear the module details panel."""
        self.current_module_index = None
        self._reset_details_container()

    def export_patch(self):
        patch_dict = self._build_patch_dict()
        try:
            encoder = PatchEncoder()
            bin_data = encoder.encode(patch_dict)
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))
            return

        if not self.patch_dict:
            title, ok = QInputDialog.getText(
                self, "Patch Title", "Enter a patch title:"
            )
            if not ok or not title.strip():
                return
            patch_name = title.strip()
            timestamp = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
            file_base = patch_name.lower().replace(" ", "_")
            patch_id = self.patch_save._generate_patch_id(f"{patch_name}-{timestamp}")
            bin_bytes = bytes(bin_data)
            meta = {
                "id": patch_id,
                "created_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                    datetime.datetime.now()
                ),
                "updated_at": "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
                    datetime.datetime.now()
                ),
                "title": patch_name,
                "revision": "1",
                "preview_url": "",
                "rating": 0,
                "like_count": 0,
                "download_count": 0,
                "view_count": 0,
                "author": {"name": ""},
                "files": [
                    {"id": patch_id, "filename": "{}.bin".format(file_base)}
                ],
                "categories": [],
                "tags": [],
                "content": "",
                "license": {"name": ""},
            }
            try:
                self.patch_save.save_to_backend((bin_bytes, meta))
                QMessageBox.information(self, "Export Success", "Patch saved to backend.")
                self._notify_close_refresh()
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", str(e))
            return

        choice = QMessageBox(self)
        choice.setWindowTitle("Export Patch")
        choice.setText("How should this edited patch be saved?")
        new_version_btn = choice.addButton("Create New Version", QMessageBox.AcceptRole)
        overwrite_btn = choice.addButton("Overwrite Existing", QMessageBox.DestructiveRole)
        choice.addButton(QMessageBox.Cancel)
        choice.exec()

        if choice.clickedButton() not in (new_version_btn, overwrite_btn):
            return

        patch_name = patch_dict.get("name", "UserPatch")
        patch_id = self.patch_id
        meta = None
        if patch_id:
            meta = self._load_backend_metadata(patch_id)
        if not meta:
            found = self._find_backend_patch_by_title(patch_name)
            if found:
                patch_id, meta = found
        if not meta:
            QMessageBox.critical(
                self,
                "Export Failed",
                "Could not locate the patch in the backend to save changes.",
            )
            return

        meta["updated_at"] = "{:%Y-%m-%dT%H:%M:%S+00:00}".format(
            datetime.datetime.now()
        )
        bin_bytes = bytes(bin_data)
        try:
            if choice.clickedButton() == new_version_btn:
                self.patch_save.save_to_backend((bin_bytes, meta), version=True)
            else:
                target = os.path.join(self.patch_save.back_path, str(patch_id))
                os.makedirs(target, exist_ok=True)
                name_bin = os.path.join(target, "{}.bin".format(patch_id))
                with open(name_bin, "wb") as f:
                    f.write(bin_bytes)
                self.patch_save.save_metadata_json(meta)
            QMessageBox.information(self, "Export Success", "Patch saved to backend.")
            self._notify_close_refresh()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def closeEvent(self, event):
        self._notify_close_refresh()
        super().closeEvent(event)

    def _notify_close_refresh(self):
        if self._refreshed:
            return
        if callable(self.on_close):
            try:
                self.on_close()
            except Exception:
                pass
        self._refreshed = True

    def _load_patch_modules(self):
        """Load modules from an existing patch dict into the editor."""
        if not self.patch_dict or "modules" not in self.patch_dict:
            return
        
        for module in self.patch_dict["modules"]:
            mod_id = str(module["mod_idx"])
            mod = self.module_index.get(mod_id)
            if mod:
                # Store the full module dict from the patch (includes parameters)
                self.selected_modules.append((mod_id, module))
                # Show module with its name
                display_name = module.get("name", mod["name"]) or mod["name"]
                self.selected_list.addItem(f"{display_name} ({mod['category']})")

    def _init_new_patch_defaults(self):
        audio_in_id = "1"
        audio_out_id = "2"
        if audio_in_id not in self.module_index or audio_out_id not in self.module_index:
            return

        for mod_id in (audio_in_id, audio_out_id):
            mod = self.module_index[mod_id]
            config = self._default_module_config(mod_id)
            self._assign_module_position(config, mod_id=mod_id)
            self.selected_modules.append((mod_id, config))
            self.selected_list.addItem(f"{mod['name']} ({mod['category']})")

        if self.selected_modules:
            self.selected_list.setCurrentRow(0)

    def _build_patch_dict(self):
        modules = []
        current_pos = 0
        for i, (mod_id, config) in enumerate(self.selected_modules):
            if not config.get("position"):
                self._assign_module_position(config, mod_id=mod_id)
            mod_dict = self._module_to_patch_format(mod_id, current_pos, i, config)
            modules.append(mod_dict)
            current_pos += self.module_index[mod_id]["min_blocks"]
        
        cpu_total = sum(self.module_index[mod_id]["cpu"] for mod_id, _ in self.selected_modules)
        
        # If editing, preserve original patch name; otherwise use default
        patch_name = self.patch_dict.get("name", "UserPatch") if self.patch_dict else "UserPatch"
        
        # Preserve connections and other data from original patch if editing
        connections = list(self.connections)
        pages = ["Page 1"]
        starred = []
        if self.patch_dict:
            pages = self.patch_dict.get("pages", ["Page 1"])
            starred = self.patch_dict.get("starred", [])

        max_page = 0
        for _, config in self.selected_modules:
            max_page = max(max_page, int(config.get("page", 0)))
        while len(pages) < max_page + 1:
            pages.append("")
        
        return {
            "size": 0,  # Encoder will calculate this
            "name": patch_name,
            "modules": modules,
            "connections": connections,
            "pages": pages,
            "pages_count": len(pages),
            "starred": starred,
            "meta": {
                "name": patch_name,
                "cpu": cpu_total,
                "n_modules": len(modules),
                "n_connections": len(connections),
                "n_pages": len(pages),
                "n_starred": len(starred),
                "i_o": "0/0/0/0/0"  # Default I/O
            }
        }

    def _module_to_patch_format(self, mod_id, position, number, config):
        mod = self.module_index[mod_id]
        
        # Use edited parameters from config if available
        if config and "parameters" in config:
            parameters = config["parameters"]
        else:
            parameters = {}
        
        # Preserve other module data from original config if editing
        options_binary = {i: 0 for i in range(8)}
        if config and "options_binary" in config:
            options_binary = config["options_binary"]
        
        if config and "params" in config:
            params_count = config["params"]
        else:
            params_count = mod.get("params", len(parameters))
        if config and "size" in config:
            module_size = config["size"]
        else:
            saved_data_len = 0
            if config and "saved_data" in config:
                saved_data_len = len(config["saved_data"])
            module_size = 14 + params_count + int((saved_data_len + 3) / 4)
        
        # Use config data if available, otherwise use module index
        return {
            "number": number,
            "category": config.get("category", mod["category"]) if config else mod["category"],
            "mod_idx": int(mod_id),
            "name": config.get("name", mod["name"]) if config else mod["name"],
            "cpu": config.get("cpu", mod["cpu"]) if config else mod["cpu"],
            "type": config.get("type", mod["name"]) if config else mod["name"],
            "size": module_size,
            "size_of_saveable_data": config.get("size_of_saveable_data", 0) if config else 0,
            "version": config.get("version", 1) if config else 1,
            "page": config.get("page", 0) if config else 0,
            "position": config.get("position", [position]) if config else [position],
            "color": config.get("color", "Blue") if config else "Blue",
            "options": config.get("options", {}) if config else {},
            "options_binary": options_binary,
            "params": params_count,
            "parameters": parameters,
            "blocks": config.get("blocks", {}) if config else {},
            "connections": config.get("connections", []) if config else [],
            "starred": config.get("starred", []) if config else []
        }

    def _shift_connections(self, start_index, delta):
        if not self.connections or delta == 0:
            return

        updated = []
        for conn in self.connections:
            source_mod, source_block = conn["source"].split(".")
            dest_mod, dest_block = conn["destination"].split(".")
            source_mod = int(source_mod)
            dest_mod = int(dest_mod)

            if delta < 0 and (source_mod == start_index or dest_mod == start_index):
                continue

            if source_mod >= start_index:
                source_mod += delta
            if dest_mod >= start_index:
                dest_mod += delta

            conn["source"] = f"{source_mod}.{source_block}"
            conn["destination"] = f"{dest_mod}.{dest_block}"
            try:
                conn["source_raw"] = int(source_mod)
                conn["source_block_raw"] = int(source_block)
                conn["dest_raw"] = int(dest_mod)
                conn["dest_block_raw"] = int(dest_block)
            except ValueError:
                conn.pop("source_raw", None)
                conn.pop("source_block_raw", None)
                conn.pop("dest_raw", None)
                conn.pop("dest_block_raw", None)
            updated.append(conn)

        self.connections = updated

    def _build_connections_section(self, module_index):
        if not self.selected_modules:
            return QLabel("No modules available")

        connections_group = QGroupBox("Connections")
        connections_layout = QVBoxLayout(connections_group)

        module_connections = [
            (idx, c)
            for idx, c in enumerate(self.connections)
            if int(c["source"].split(".")[0]) == module_index
            or int(c["destination"].split(".")[0]) == module_index
        ]

        if module_connections:
            list_group = QGroupBox("Module Connections")
            list_layout = QVBoxLayout(list_group)
            conn_list = QListWidget()
            for conn_index, conn in module_connections:
                source_mod, source_block_val = conn["source"].split(".")
                dest_mod, dest_block_val = conn["destination"].split(".")
                strength_val = conn.get("strength", 100)

                source_name = self._module_display_name(
                    self.selected_modules[int(source_mod)][0],
                    self.selected_modules[int(source_mod)][1],
                )
                dest_name = self._module_display_name(
                    self.selected_modules[int(dest_mod)][0],
                    self.selected_modules[int(dest_mod)][1],
                )
                source_block_name = self._block_name_for_module(
                    self.selected_modules[int(source_mod)][0],
                    self.selected_modules[int(source_mod)][1],
                    int(source_block_val),
                )
                dest_block_name = self._block_name_for_module(
                    self.selected_modules[int(dest_mod)][0],
                    self.selected_modules[int(dest_mod)][1],
                    int(dest_block_val),
                )

                label = (
                    f"{source_name}.{source_block_val} ({source_block_name}) → "
                    f"{dest_name}.{dest_block_val} ({dest_block_name}) ({strength_val}%)"
                )
                item = QListWidgetItem(label)
                item.setData(1, conn_index)
                conn_list.addItem(item)

            if conn_list.count() > 0:
                row_height = conn_list.sizeHintForRow(0)
                if row_height <= 0:
                    row_height = 22
                conn_list.setMinimumHeight(row_height * 5 + conn_list.frameWidth() * 2)

            remove_btn = QPushButton("Remove Selected Connection")
            remove_btn.clicked.connect(
                lambda: self._remove_selected_connection(conn_list, module_index)
            )

            list_layout.addWidget(conn_list)
            list_layout.addWidget(remove_btn)
            connections_layout.addWidget(list_group)
        else:
            connections_layout.addWidget(QLabel("No connections for this module"))

        add_group = QGroupBox("Add Connection")
        add_layout = QFormLayout(add_group)

        source_combo = QComboBox()
        dest_combo = QComboBox()
        for idx, (mod_id, config) in enumerate(self.selected_modules):
            name = self._module_display_name(mod_id, config)
            source_combo.addItem(f"{idx}: {name}", idx)
            dest_combo.addItem(f"{idx}: {name}", idx)

        if module_index < source_combo.count():
            source_combo.setCurrentIndex(module_index)

        source_block = QComboBox()
        dest_block = QComboBox()
        if source_combo.currentData() is not None:
            self._populate_block_combo(
                source_block,
                self.selected_modules[source_combo.currentData()][0],
                self.selected_modules[source_combo.currentData()][1],
            )
        if dest_combo.currentData() is not None:
            self._populate_block_combo(
                dest_block,
                self.selected_modules[dest_combo.currentData()][0],
                self.selected_modules[dest_combo.currentData()][1],
            )
        source_combo.currentIndexChanged.connect(
            lambda: self._populate_block_combo(
                source_block,
                self.selected_modules[source_combo.currentData()][0],
                self.selected_modules[source_combo.currentData()][1],
            )
        )
        dest_combo.currentIndexChanged.connect(
            lambda: self._populate_block_combo(
                dest_block,
                self.selected_modules[dest_combo.currentData()][0],
                self.selected_modules[dest_combo.currentData()][1],
            )
        )
        strength = QSpinBox()
        strength.setRange(0, 100)
        strength.setValue(100)

        add_btn = QPushButton("Add Connection")
        add_btn.clicked.connect(
            lambda: self._add_connection(
                source_combo.currentData(),
                source_block.currentData(),
                dest_combo.currentData(),
                dest_block.currentData(),
                strength.value(),
                module_index,
            )
        )

        add_layout.addRow(QLabel("Source module:"), source_combo)
        add_layout.addRow(QLabel("Source block:"), source_block)
        add_layout.addRow(QLabel("Destination module:"), dest_combo)
        add_layout.addRow(QLabel("Destination block:"), dest_block)
        add_layout.addRow(QLabel("Strength (%):"), strength)
        add_layout.addRow(add_btn)
        connections_layout.addWidget(add_group)

        return connections_group

    def _add_connection(self, source_mod, source_block, dest_mod, dest_block, strength, module_index):
        if source_mod is None or dest_mod is None:
            return

        self.connections.append(
            {
                "source": f"{int(source_mod)}.{int(source_block or 0)}",
                "destination": f"{int(dest_mod)}.{int(dest_block or 0)}",
                "strength": int(strength),
                "source_raw": int(source_mod),
                "source_block_raw": int(source_block or 0),
                "dest_raw": int(dest_mod),
                "dest_block_raw": int(dest_block or 0),
                "strength_raw": int(strength) * 100,
            }
        )
        self._refresh_current_details()
        self._refresh_routing_view()

    def _remove_selected_connection(self, conn_list, module_index):
        item = conn_list.currentItem()
        if not item:
            return
        conn_index = item.data(1)
        if conn_index is None:
            return
        if 0 <= conn_index < len(self.connections):
            self.connections.pop(conn_index)
        self._refresh_current_details()
        self._refresh_routing_view()

    def _module_display_name(self, mod_id, config):
        mod_id = str(mod_id)
        mod = self.module_index.get(mod_id, {})
        return config.get("name") if config and config.get("name") else mod.get("name", "")

    def order_by_audio_path(self):
        if not self.selected_modules:
            return

        current_idx = self.current_module_index
        audio_nodes = set()
        edges = []
        for conn in self.connections:
            source_mod, source_block = conn["source"].split(".")
            dest_mod, dest_block = conn["destination"].split(".")
            source_idx = int(source_mod)
            dest_idx = int(dest_mod)

            if self._is_cv_connection(source_idx, int(source_block), dest_idx, int(dest_block)):
                continue

            edges.append((source_idx, dest_idx))
            audio_nodes.add(source_idx)
            audio_nodes.add(dest_idx)

        order = self._toposort_indices(len(self.selected_modules), edges)
        audio_order = [idx for idx in order if idx in audio_nodes]
        tail = [idx for idx in order if idx not in audio_nodes]
        new_order = audio_order + tail

        if not new_order:
            return

        old_to_new = {old: new for new, old in enumerate(new_order)}
        self.selected_modules = [self.selected_modules[i] for i in new_order]
        self._remap_connections(old_to_new)
        self._rebuild_selected_list()

        if current_idx is not None and current_idx in old_to_new:
            self.selected_list.setCurrentRow(old_to_new[current_idx])
        else:
            self.clear_module_details()

        self._refresh_routing_view()

    def _toposort_indices(self, count, edges):
        indegree = {i: 0 for i in range(count)}
        graph = {i: [] for i in range(count)}
        for src, dst in edges:
            if src == dst:
                continue
            graph[src].append(dst)
            indegree[dst] += 1

        order = []
        queue = [i for i in range(count) if indegree[i] == 0]
        queue.sort()
        while queue:
            node = queue.pop(0)
            order.append(node)
            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
                    queue.sort()

        if len(order) < count:
            remaining = [i for i in range(count) if i not in order]
            order.extend(remaining)
        return order

    def _is_cv_connection(self, source_idx, source_block, dest_idx, dest_block):
        source_meta = self._block_meta_for_module(source_idx, source_block)
        dest_meta = self._block_meta_for_module(dest_idx, dest_block)
        if dest_meta.get("isParam"):
            return True

        source_name = source_meta.get("name", "").lower()
        dest_name = dest_meta.get("name", "").lower()
        if "cv" in source_name or "cv" in dest_name:
            return True
        return False

    def _block_meta_for_module(self, module_index, block_index):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return {"name": "", "isParam": False}
        mod_id, config = self.selected_modules[module_index]
        blocks = config.get("blocks") or self.module_index.get(str(mod_id), {}).get("blocks", {})
        for name, meta in blocks.items():
            position = meta.get("position")
            if isinstance(position, list) and block_index in position:
                data = dict(meta)
                data["name"] = name
                return data
            if isinstance(position, int) and block_index == position:
                data = dict(meta)
                data["name"] = name
                return data
        return {"name": "", "isParam": False}

    def _remap_connections(self, old_to_new):
        updated = []
        for conn in self.connections:
            source_mod, source_block = conn["source"].split(".")
            dest_mod, dest_block = conn["destination"].split(".")
            source_mod = int(source_mod)
            dest_mod = int(dest_mod)
            if source_mod not in old_to_new or dest_mod not in old_to_new:
                continue
            source_mod = old_to_new[source_mod]
            dest_mod = old_to_new[dest_mod]
            conn["source"] = f"{source_mod}.{source_block}"
            conn["destination"] = f"{dest_mod}.{dest_block}"
            conn["source_raw"] = source_mod
            conn["source_block_raw"] = int(source_block)
            conn["dest_raw"] = dest_mod
            conn["dest_block_raw"] = int(dest_block)
            updated.append(conn)
        self.connections = updated

    def _rebuild_selected_list(self):
        self.selected_list.blockSignals(True)
        self.selected_list.clear()
        for mod_id, config in self.selected_modules:
            mod = self.module_index.get(str(mod_id), {})
            display_name = config.get("name", mod.get("name", "")) or mod.get("name", "")
            self.selected_list.addItem(f"{display_name} ({mod.get('category', '')})")
        self.selected_list.blockSignals(False)

    def _module_span_length(self, config, mod_id):
        blocks = config.get("blocks", {})
        positions = []
        for meta in blocks.values():
            position = meta.get("position")
            if isinstance(position, list):
                positions.extend(position)
            elif isinstance(position, int):
                positions.append(position)
        if positions:
            return max(positions) + 1
        return self.module_index.get(str(mod_id), {}).get("min_blocks", 1)

    def _occupied_positions(self, ignore_index=None):
        occupied = {}
        for idx, (mod_id, cfg) in enumerate(self.selected_modules):
            if ignore_index is not None and idx == ignore_index:
                continue
            if not cfg.get("position"):
                continue
            start = cfg["position"][0]
            page = cfg.get("page", 0)
            span = self._module_span_length(cfg, mod_id)
            occupied.setdefault(page, set())
            for pos in range(start, start + span):
                occupied[page].add(pos)
        return occupied

    def _is_span_free(self, page, start, span, ignore_index=None):
        occupied = self._occupied_positions(ignore_index=ignore_index).get(page, set())
        for pos in range(start, start + span):
            if pos in occupied:
                return False
        return True

    def _assign_module_position(self, config, mod_id=None, preferred_start=0, module_index=None, preferred_page=None):
        if mod_id is None:
            mod_id = config.get("mod_idx", 0)
        span = self._module_span_length(config, mod_id)
        start = max(0, int(preferred_start))
        max_pos = 39
        page = config.get("page", 0) if preferred_page is None else preferred_page
        occupied_by_page = self._occupied_positions(ignore_index=module_index)
        max_page = max(occupied_by_page.keys(), default=0)

        if span > max_pos + 1:
            config["position"] = [0]
            config["page"] = max_page + 1
            return

        for current_page in range(page, max_page + 1):
            if start + span - 1 <= max_pos and self._is_span_free(
                current_page, start, span, module_index
            ):
                config["position"] = [start]
                config["page"] = current_page
                return
            for candidate in range(0, max_pos - span + 2):
                if self._is_span_free(current_page, candidate, span, module_index):
                    config["position"] = [candidate]
                    config["page"] = current_page
                    return

        new_page = max_page + 1
        config["position"] = [0]
        config["page"] = new_page

    def _default_module_config(self, mod_id):
        mod_id = str(mod_id)
        mod = self.module_index.get(mod_id, {})
        options_def = mod.get("options", {})
        options = {}
        options_binary = {}
        for name, values in options_def.items():
            if isinstance(values, list) and values:
                options[name] = values[0]
                options_binary[name] = 0
        blocks = mod.get("blocks", {})
        try:
            blocks = self._patch_binary._calc_blocks(
                {"mod_idx": int(mod_id), "version": 1, "options": options}
            )
        except Exception:
            blocks = mod.get("blocks", {})

        return {
            "options": options,
            "options_binary": options_binary,
            "blocks": blocks,
            "params": mod.get("params", 0),
            "size_of_saveable_data": 0,
            "parameters": self._default_parameters_from_blocks(mod_id, {"blocks": blocks}),
            "params_auto": True,
            "page": 0,
        }

    def _default_parameters_from_blocks(self, mod_id, config):
        blocks = {}
        if config and config.get("blocks"):
            blocks = config["blocks"]
        else:
            blocks = self.module_index.get(str(mod_id), {}).get("blocks", {})

        params = {}
        for name, meta in blocks.items():
            if meta.get("isParam"):
                params[name] = float(self._param_default_value(mod_id, name))
        return params

    def _param_default_value(self, mod_id, param_name):
        mod = self.module_index.get(str(mod_id), {})
        defaults = mod.get("param_defaults") or mod.get("param_default") or {}
        if isinstance(defaults, dict) and param_name in defaults:
            return defaults[param_name]
        return 0.0

    def _block_name_for_module(self, mod_id, config, block_index):
        blocks = {}
        if config and config.get("blocks"):
            blocks = config["blocks"]
        else:
            blocks = self.module_index.get(str(mod_id), {}).get("blocks", {})

        for name, meta in blocks.items():
            position = meta.get("position")
            if isinstance(position, list) and block_index in position:
                return name
            if isinstance(position, int) and block_index == position:
                return name
        return f"Block {block_index}"

    def _populate_block_combo(self, combo, mod_id, config):
        combo.blockSignals(True)
        combo.clear()
        blocks = {}
        if config and config.get("blocks"):
            blocks = config["blocks"]
        else:
            blocks = self.module_index.get(str(mod_id), {}).get("blocks", {})

        block_entries = []
        for name, meta in blocks.items():
            position = meta.get("position")
            if isinstance(position, list):
                for pos in position:
                    block_entries.append((pos, name))
            else:
                block_entries.append((position, name))

        block_entries = [b for b in block_entries if b[0] is not None]
        block_entries.sort(key=lambda x: x[0])
        for pos, name in block_entries:
            combo.addItem(f"{pos}: {name}", pos)

        if combo.count() == 0:
            for pos in range(0, 128):
                combo.addItem(f"{pos}: Block {pos}", pos)
        combo.blockSignals(False)

    def _build_options_section(self, mod_id, config, module_index):
        mod = self.module_index.get(str(mod_id), {})
        options_def = mod.get("options", {})
        if not options_def:
            return QLabel("No options for this module")

        if "options" not in config:
            config["options"] = {}
        if "options_binary" not in config:
            config["options_binary"] = {}

        options_group = QGroupBox("Module Options")
        options_form = QFormLayout(options_group)

        for opt_name, values in options_def.items():
            if not isinstance(values, list) or not values:
                continue

            current_value = config["options"].get(opt_name, values[0])
            combo = QComboBox()
            combo.blockSignals(True)
            for idx, value in enumerate(values):
                combo.addItem(str(value), idx)
                if value == current_value:
                    combo.setCurrentIndex(idx)

            config["options"][opt_name] = values[combo.currentIndex()]
            config["options_binary"][opt_name] = combo.currentIndex()

            combo.blockSignals(False)
            combo.currentIndexChanged.connect(
                lambda idx, name=opt_name, vals=values, mi=module_index: self._on_option_changed(
                    mi, name, vals, idx
                )
            )
            options_form.addRow(QLabel(opt_name), combo)

        reset_btn = QPushButton("Reset Options to Defaults")
        reset_btn.clicked.connect(lambda: self._reset_options(module_index))
        options_form.addRow(reset_btn)
        return options_group

    def _on_option_changed(self, module_index, option_name, values, index):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        mod_id, config = self.selected_modules[module_index]
        if "options" not in config:
            config["options"] = {}
        if "options_binary" not in config:
            config["options_binary"] = {}
        config["options"][option_name] = values[index]
        config["options_binary"][option_name] = index
        self._recalc_module_blocks_and_params(module_index)
        self._refresh_current_details()
        self._refresh_routing_view()

    def _reset_options(self, module_index):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        mod_id, config = self.selected_modules[module_index]
        defaults = self._default_module_config(mod_id)
        config["options"] = defaults.get("options", {})
        config["options_binary"] = defaults.get("options_binary", {})
        self._recalc_module_blocks_and_params(module_index)
        self._refresh_current_details()
        self._refresh_routing_view()

    def _build_params_section(self, mod_id, config, module_index):
        if config and "parameters" in config and config["parameters"]:
            parameters = config["parameters"]
        else:
            parameters = self._default_parameters_from_blocks(mod_id, config)

        if not parameters:
            return None

        params_group = QGroupBox("Parameters")
        params_form_layout = QVBoxLayout(params_group)

        for param_name, param_value in parameters.items():
            param_h_layout = QHBoxLayout()
            param_label = QLabel(f"{param_name}:")
            param_h_layout.addWidget(param_label)

            param_slider = QSlider(Qt.Horizontal)
            param_slider.setMinimum(0)
            param_slider.setMaximum(100)
            param_slider.setValue(int(param_value * 100))
            param_slider.setProperty("param_name", param_name)
            param_slider.setProperty("module_index", module_index)
            param_h_layout.addWidget(param_slider)

            param_spinbox = QDoubleSpinBox()
            param_spinbox.setMinimum(0.0)
            param_spinbox.setMaximum(1.0)
            param_spinbox.setSingleStep(0.01)
            param_spinbox.setValue(param_value)
            param_spinbox.setProperty("param_name", param_name)
            param_spinbox.setProperty("module_index", module_index)
            param_h_layout.addWidget(param_spinbox)

            control_key = f"{module_index}_{param_name}"
            self.param_controls[control_key] = {
                "slider": param_slider,
                "spinbox": param_spinbox,
                "module_index": module_index,
                "param_name": param_name,
            }

            param_slider.valueChanged.connect(self.on_parameter_slider_changed)
            param_spinbox.valueChanged.connect(self.on_parameter_spinbox_changed)

            params_form_layout.addLayout(param_h_layout)

        return params_group

    def _reset_details_container(self):
        old_widget = self.details_scroll.takeWidget()
        new_widget = QWidget()
        self.details_layout = QVBoxLayout(new_widget)
        self.details_scroll.setWidget(new_widget)
        if old_widget is not None:
            old_widget.deleteLater()

    def _refresh_current_details(self):
        if self.current_module_index is None:
            return
        if self.current_module_index < 0 or self.current_module_index >= len(self.selected_modules):
            return
        mod_id, config = self.selected_modules[self.current_module_index]
        self.show_module_details(mod_id, config, self.current_module_index)

    def _recalc_module_blocks_and_params(self, module_index):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        mod_id, config = self.selected_modules[module_index]
        if "options" not in config:
            config["options"] = {}
        module_stub = {
            "mod_idx": int(mod_id),
            "version": config.get("version", 1),
            "options": config.get("options", {}),
        }
        try:
            blocks = self._patch_binary._calc_blocks(module_stub)
        except Exception:
            return

        config["blocks"] = blocks
        existing_params = config.get("parameters", {})
        new_params = {}
        for name, meta in blocks.items():
            if meta.get("isParam"):
                new_params[name] = existing_params.get(
                    name, float(self._param_default_value(mod_id, name))
                )
        config["parameters"] = new_params
        if config.get("params_auto"):
            config["params"] = len(new_params)
        if config.get("position"):
            span = self._module_span_length(config, mod_id)
            if not self._is_span_free(config.get("page", 0), config["position"][0], span, module_index):
                self._assign_module_position(config, mod_id=mod_id, module_index=module_index)

    def toggle_routing_view(self):
        self.routing_container.setVisible(not self.routing_container.isVisible())
        self._refresh_routing_view()

    def _refresh_routing_view(self):
        if not self.routing_container.isVisible():
            return

        if self.routing_graph_widget:
            self.routing_layout.removeWidget(self.routing_graph_widget)
            self.routing_graph_widget.setParent(None)
            self.routing_graph_widget.deleteLater()
            self.routing_graph_widget = None

        patch = self._build_patch_dict()
        if not patch["modules"]:
            self.routing_placeholder.setText("No routing data to display.")
            if self.routing_placeholder.parent() is None:
                self.routing_layout.addWidget(self.routing_placeholder)
            return

        self.routing_placeholder.setText("")
        self.routing_graph = NodeGraph()
        self.routing_graph.set_acyclic(False)
        setup_context_menu(self.routing_graph)
        self.routing_graph.register_nodes([BaseNode])
        self.routing_graph_widget = self.routing_graph.widget
        self.routing_layout.addWidget(self.routing_graph_widget)

        nodes = {}
        for module in patch["modules"]:
            node = self.routing_graph.create_node(
                "nodeGraphQt.nodes.BaseNode",
                name=(module["type"] if module["name"] == "" else module["name"]),
                color=self._get_color_hex(module["color"]),
                text_color="000000" if module["color"] != "Blue" else "ffffff",
            )
            inp, outp, in_pos, out_pos = [], [], [], []
            for key, param in module["blocks"].items():
                if "in" in key or param.get("isParam"):
                    node.add_input(key, multi_input=True)
                    inp.append(key)
                    in_pos.append(int(param["position"]))
                elif "out" in key:
                    node.add_output(key)
                    outp.append(key)
                    out_pos.append(int(param["position"]))
            nodes[module["number"]] = node, inp, outp, in_pos, out_pos

        def node_pos_map(node):
            inpts = node[1]
            outps = node[2]
            in_pos = node[3]
            out_pos = node[4]
            node_pos_start = [x for x in range(0, len(inpts))]
            node_pos_end = [x for x in range(0, len(outps))]
            data_input = dict(zip(in_pos, node_pos_start))
            data_output = dict(zip(out_pos, node_pos_end))
            return {**data_input, **data_output}

        data = []
        for _, node in nodes.items():
            data.append(node_pos_map(node))

        @exit_after(3)
        def make_connections(mod, block, nmod, nblock, src, dest):
            try:
                nodes[int(mod)][0].set_output(
                    src[int(block)], nodes[int(nmod)][0].input(dest[int(nblock)])
                )
            except (KeyError, IndexError):
                pass

        for conn in patch["connections"]:
            mod, block = conn["source"].split(".")
            nmod, nblock = conn["destination"].split(".")
            src = data[int(mod)]
            dest = data[int(nmod)]
            try:
                make_connections(mod, block, nmod, nblock, src, dest)
            except KeyboardInterrupt:
                break

        try:
            self.routing_graph.auto_layout_nodes()
        except (KeyError, RecursionError):
            self.routing_graph.reset_zoom()
        self.routing_graph.fit_to_selection()

    def _find_backend_patch_by_title(self, title):
        if not title:
            return None
        back_path = self.patch_save.back_path
        if not back_path or not os.path.isdir(back_path):
            return None

        title = title.strip().lower()
        for entry in os.listdir(back_path):
            entry_path = os.path.join(back_path, entry)
            if not os.path.isdir(entry_path):
                continue
            if entry in ("Banks", "Folders", "Samples", "temp"):
                continue
            json_path = os.path.join(entry_path, "{}.json".format(entry))
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r") as f:
                        meta = json.load(f)
                    if meta.get("title", "").lower() == title:
                        return meta.get("id", entry), meta
                except (OSError, json.JSONDecodeError):
                    continue
            for fname in os.listdir(entry_path):
                if not fname.endswith(".json"):
                    continue
                try:
                    with open(os.path.join(entry_path, fname), "r") as f:
                        meta = json.load(f)
                    if meta.get("title", "").lower() == title:
                        return meta.get("id", entry), meta
                except (OSError, json.JSONDecodeError):
                    continue
        return None

    def _load_backend_metadata(self, patch_id):
        if not patch_id:
            return None
        back_path = self.patch_save.back_path
        if not back_path or not os.path.isdir(back_path):
            return None
        patch_dir = os.path.join(back_path, str(patch_id))
        if not os.path.isdir(patch_dir):
            return None
        json_path = os.path.join(patch_dir, "{}.json".format(patch_id))
        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                return None
        return None

    @staticmethod
    def _get_color_hex(color):
        return {
            "Blue": "#0000FF",
            "Green": "#00FF00",
            "Red": "#FF0000",
            "Yellow": "#FFFF00",
            "Aqua": "#00FFFF",
            "Magenta": "#FF00FF",
            "White": "#FFFFFF",
            "Orange": "#FFA500",
            "Lima": "#BFFF00",
            "Surf": "#3627F6",
            "Sky": "#87CEEB",
            "Purple": "#A020F0",
            "Pink": "#FF007F",
            "Peach": "#FFE5B4",
            "Mango": "#FF8243",
        }[color]


class ZOIALibrarianEditor(QMainWindow):
    """Consistent class interface for launching the patch builder/editor."""
    def __init__(self, ui, path, msg, save, window, local):
        """Initializes the class with the required parameters.

        ui: The UI component of ZOIALibrarianMain
        path: A String representing the path to the backend application
              directory.
        sd: Helper class to access UI-related SD methods.
        msg: A template QMessageBox.
        window: A reference to the main UI window for icon consistency.
        """

        super().__init__()

        # Variable init.
        self.ui = ui
        self.path = path
        self.msg = msg
        self.save = save
        self.window = window
        self.local = local
        self.widget = None

    def new_patch(self):
        """Launch the patch builder/editor window as a separate window."""
        self.widget = PatchBuilderEditor(
            msg=self.msg,
            save=self.save,
            window=self.window,
            on_close=self._refresh_local_patches,
        )
        self.widget.show()

    def edit_patch(self):
        """Launch the patch editor with an existing patch for modifications.
        
        patch_dict: A parsed patch dict (from PatchBinary.parse_data or similar)
                   containing modules, connections, pages, etc.
        """

        patch_dict = self.local.get_viz()
        patch_id = self.local.get_local_selected()
        self.widget = PatchBuilderEditor(
            msg=self.msg,
            save=self.save,
            window=self.window,
            patch_dict=patch_dict,
            patch_id=patch_id,
            on_close=self._refresh_local_patches,
        )
        self.widget.show()

    def _refresh_local_patches(self):
        if self.local:
            self.local.get_local_patches()
