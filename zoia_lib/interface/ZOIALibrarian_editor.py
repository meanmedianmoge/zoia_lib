import datetime
import json
import os
import copy
import html
from PySide6.QtWidgets import (
    QMainWindow,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QInputDialog,
    QMessageBox,
    QDialog,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QGroupBox,
    QScrollArea,
    QFormLayout,
    QAbstractItemView,
    QLineEdit,
    QMenu,
    QCheckBox,
    QTextEdit,
    QDialogButtonBox,
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from NodeGraphQt import NodeGraph, BaseNode, setup_context_menu
from zoia_lib.backend.patch_binary import PatchBinary
from zoia_lib.backend.patch_encode import PatchEncoder
from zoia_lib.backend.utilities import exit_after, meipass

class EditorButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("editor_btn")

class PageLayoutCell(QLabel):
    def __init__(self, page_index, position, on_drop, parent=None):
        super().__init__(parent)
        self._page_index = page_index
        self._position = position
        self._on_drop = on_drop
        self.module_number = None
        self._drag_start_pos = None
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.module_number is None:
            return
        if not (event.buttons() & Qt.LeftButton):
            return
        if self._drag_start_pos is None:
            return
        if (event.pos() - self._drag_start_pos).manhattanLength() < 8:
            return
        mime = QMimeData()
        mime.setData(
            "application/x-zoia-module",
            f"{self.module_number}:{self._position}".encode("utf-8"),
        )
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-zoia-module"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-zoia-module"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().hasFormat("application/x-zoia-module"):
            event.ignore()
            return
        payload = bytes(event.mimeData().data("application/x-zoia-module")).decode("utf-8")
        try:
            module_number, origin_pos = payload.split(":")
            module_number = int(module_number)
            origin_pos = int(origin_pos)
        except (ValueError, AttributeError):
            event.ignore()
            return
        if callable(self._on_drop):
            self._on_drop(module_number, origin_pos, self._page_index, self._position)
        event.acceptProposedAction()

class PatchBuilderEditor(QMainWindow):
    """Separate window for building a patch by selecting modules and configuring them."""
    def __init__(self, msg=None, save=None, window=None, patch_dict=None, patch_id=None, on_close=None):
        super().__init__(window)
        self.setWindowTitle("Patch Builder - New Patch")
        self.resize(1300, 1300)
        self.setWindowState(self.windowState() | Qt.WindowMaximized)
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
        self.module_overrides = {}
        self._pending_page_names = {}
        self._pending_pages = None

        # Create main container to hold everything
        main_container = QWidget()
        container_layout = QVBoxLayout(main_container)

        # Create the main layout for modules and details
        main_layout = QHBoxLayout()

        # Module list
        module_list_layout = QVBoxLayout()
        module_label = QLabel("Available Modules:")
        self.module_search = QLineEdit()
        self.module_search.setPlaceholderText("Search modules...")
        self.module_list = QTreeWidget()
        self.module_list.setHeaderHidden(True)
        self.module_list.setContextMenuPolicy(Qt.CustomContextMenu)
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
            child.setToolTip(0, self._module_tooltip(mod_id, mod["name"]))
            categories[category].addChild(child)
        # self.module_list.expandAll()
        module_list_layout.addWidget(module_label)
        module_list_layout.addWidget(self.module_search)
        module_list_layout.addWidget(self.module_list)
        self.supermodule_category = QTreeWidgetItem(["Supermodules"])
        self.supermodule_category.setData(0, 1, "supermodule_category")
        self.module_list.addTopLevelItem(self.supermodule_category)
        self.add_module_btn = EditorButton("Add Module to Patch →")
        module_list_layout.addWidget(self.add_module_btn)

        self.supermodules = []
        self.supermodule_delete_btn = EditorButton("Delete Selected Supermodule")
        self.supermodule_delete_btn.setEnabled(False)
        module_list_layout.addWidget(self.supermodule_delete_btn)
        main_layout.addLayout(module_list_layout, 1)

        # Selected modules
        selected_layout = QVBoxLayout()
        selected_label = QLabel("Patch Modules:")
        self.selected_list = QListWidget()
        self.selected_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selected_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.selected_list.setContextMenuPolicy(Qt.CustomContextMenu)
        selected_layout.addWidget(selected_label)
        selected_layout.addWidget(self.selected_list)
        self.remove_module_btn = EditorButton("Remove Selected Module(s)")
        selected_layout.addWidget(self.remove_module_btn)
        self.save_supermodule_btn = EditorButton("Save Selected as Supermodule")
        selected_layout.addWidget(self.save_supermodule_btn)
        main_layout.addLayout(selected_layout, 1)

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
        main_layout.addLayout(details_layout, 2)

        self.routing_graph = None
        self.routing_window = None
        self.routing_window_layout = None
        self.routing_window_placeholder = None
        self.routing_window_graph_widget = None
        self._routing_is_building = False
        self._routing_port_meta = {}
        self.page_layout_window = None
        self.page_layout_window_layout = None
        self.page_layout_window_placeholder = None
        self.page_layout_window_scroll = None
        self.page_layout_window_container = None
        self.page_layout_controls = None
        self.page_layout_add_btn = None
        self.page_layout_remove_btn = None
        container_layout.addLayout(main_layout, 1)

        # Bottom button layout
        bottom_layout = QHBoxLayout()
        self.toggle_routing_btn = EditorButton("Show Expanded Patch")
        self.toggle_page_layout_btn = EditorButton("Show Page Layout")
        self.export_btn = EditorButton("Export Patch")
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.toggle_routing_btn)
        bottom_layout.addWidget(self.toggle_page_layout_btn)
        bottom_layout.addWidget(self.export_btn)
        container_layout.addLayout(bottom_layout, 0)

        # Set the main container as central widget
        self.setCentralWidget(main_container)

        # Connections
        self.add_module_btn.clicked.connect(self.add_selected_module)
        self.module_list.itemDoubleClicked.connect(lambda _item: self.add_selected_module())
        self.remove_module_btn.clicked.connect(self.remove_selected_module)
        self.save_supermodule_btn.clicked.connect(self.save_selected_supermodule)
        self.supermodule_delete_btn.clicked.connect(self.delete_selected_supermodule)
        self.module_list.currentItemChanged.connect(self._update_supermodule_controls)
        self.module_list.customContextMenuRequested.connect(self._open_module_tree_context_menu)
        self.module_search.textChanged.connect(self._filter_module_tree)
        self.selected_list.itemSelectionChanged.connect(self.on_module_selected)
        self.selected_list.model().rowsAboutToBeMoved.connect(self._on_modules_about_to_move)
        self.selected_list.model().rowsMoved.connect(self._on_modules_moved)
        self.selected_list.customContextMenuRequested.connect(self._open_module_context_menu)
        self.export_btn.clicked.connect(self.export_patch)
        self.toggle_routing_btn.clicked.connect(self.toggle_routing_view)
        self.toggle_page_layout_btn.clicked.connect(self.toggle_page_layout_view)

        self._load_module_overrides()

        # If editing an existing patch, load its modules
        if self.patch_dict:
            self.setWindowTitle("Patch Editor - {}".format(self.patch_dict.get("name", "Untitled")))
            self.connections = list(self.patch_dict.get("connections", []))
            self._load_patch_modules()
        else:
            self.connections = []
            self._init_new_patch_defaults()

        self._load_supermodules()

    def add_selected_module(self):
        item = self.module_list.currentItem()
        if not item:
            return
        mod_id = item.data(0, 1)
        if mod_id in ("category", "supermodule_category") or mod_id is None:
            return
        if mod_id == "supermodule":
            self._add_supermodule_from_tree(item)
            return
        # For now, just add with default config
        insert_row = len(self.selected_modules)
        config = self._default_module_config(mod_id)
        self._assign_module_position(config, mod_id=mod_id)
        self.selected_modules.append((mod_id, config))
        self.selected_list.addItem(self._build_selected_list_item(mod_id, config))
        self.selected_list.setCurrentRow(insert_row)
        self._recalc_module_blocks_and_params(insert_row)
        self._refresh_routing_view()

    def _filter_module_tree(self, text):
        query = (text or "").strip().lower()
        root_count = self.module_list.topLevelItemCount()
        for i in range(root_count):
            category = self.module_list.topLevelItem(i)
            if category is None:
                continue
            visible_children = 0
            for j in range(category.childCount()):
                child = category.child(j)
                if child is None:
                    continue
                label = (child.text(0) or "").lower()
                match = not query or query in label
                if not match and category == self.supermodule_category:
                    super_index = child.data(0, Qt.UserRole)
                    if super_index is not None and 0 <= super_index < len(self.supermodules):
                        supermod = self.supermodules[super_index]
                        if isinstance(supermod, dict):
                            for entry in supermod.get("modules", []):
                                name = entry.get("name") or ""
                                if query in str(name).lower():
                                    match = True
                                    break
                child.setHidden(not match)
                if match:
                    visible_children += 1
            category.setHidden(visible_children == 0)
            if query:
                category.setExpanded(True)
            else:
                category.setExpanded(False)

    def _on_modules_about_to_move(self, _parent, _start, _end, _destination, _row):
        self._pre_reorder_indices = list(range(len(self.selected_modules)))
        self._pre_reorder_modules = list(self.selected_modules)

    def _on_modules_moved(self, _parent, start, end, _destination, row):
        if not getattr(self, "_pre_reorder_indices", None):
            return
        indices = self._pre_reorder_indices
        segment = indices[start:end + 1]
        del indices[start:end + 1]
        insert_at = row
        if insert_at > start:
            insert_at -= len(segment)
        for offset, value in enumerate(segment):
            indices.insert(insert_at + offset, value)

        if len(indices) != len(self.selected_modules):
            return

        mapping = {old: new for new, old in enumerate(indices)}
        new_order = [self._pre_reorder_modules[old] for old in indices]
        self.selected_modules = new_order

        if self.connections:
            updated = []
            for conn in self.connections:
                try:
                    source_mod, source_block = conn["source"].split(".")
                    dest_mod, dest_block = conn["destination"].split(".")
                    source_mod = mapping.get(int(source_mod), int(source_mod))
                    dest_mod = mapping.get(int(dest_mod), int(dest_mod))
                except (ValueError, AttributeError):
                    updated.append(conn)
                    continue
                conn["source"] = f"{source_mod}.{source_block}"
                conn["destination"] = f"{dest_mod}.{dest_block}"
                try:
                    conn["source_raw"] = int(source_mod)
                    conn["dest_raw"] = int(dest_mod)
                    conn["source_block_raw"] = int(source_block)
                    conn["dest_block_raw"] = int(dest_block)
                except ValueError:
                    conn.pop("source_raw", None)
                    conn.pop("source_block_raw", None)
                    conn.pop("dest_raw", None)
                    conn.pop("dest_block_raw", None)
                updated.append(conn)
            self.connections = updated

        self._refresh_current_details()
        self._refresh_routing_view()
        self._pre_reorder_indices = None
        self._pre_reorder_modules = None

    def _open_module_context_menu(self, pos):
        item = self.selected_list.itemAt(pos)
        if item is None:
            return
        menu = QMenu(self.selected_list)
        duplicate_action = menu.addAction("Duplicate Module")
        action = menu.exec(self.selected_list.mapToGlobal(pos))
        if action == duplicate_action:
            row = self.selected_list.row(item)
            self._duplicate_module_at_index(row)

    def _open_module_tree_context_menu(self, pos):
        item = self.module_list.itemAt(pos)
        if item is None or item.data(0, 1) != "supermodule":
            return
        super_index = item.data(0, Qt.UserRole)
        if super_index is None or super_index < 0 or super_index >= len(self.supermodules):
            return
        menu = QMenu(self.module_list)
        set_description_action = menu.addAction("Edit Supermodule")
        action = menu.exec(self.module_list.mapToGlobal(pos))
        if action == set_description_action:
            self._edit_supermodule_metadata(super_index)

    def _edit_supermodule_metadata(self, super_index):
        if super_index < 0 or super_index >= len(self.supermodules):
            return
        entry = self.supermodules[super_index]
        if not isinstance(entry, dict):
            entry = {"name": str(entry)}
        current_name = entry.get("name", f"Supermodule {super_index + 1}")
        current_desc = entry.get("description", "")
        if not isinstance(current_name, str):
            current_name = str(current_name)
        if not isinstance(current_desc, str):
            current_desc = str(current_desc)

        name, description, ok = self._prompt_supermodule_metadata(
            name=current_name,
            description=current_desc,
            title="Edit Supermodule",
        )
        if not ok:
            return

        conflict_index = None
        for idx, item in enumerate(self.supermodules):
            if idx == super_index:
                continue
            if isinstance(item, dict):
                existing_name = item.get("name", "")
            else:
                existing_name = str(item)
            if str(existing_name).strip().lower() == name.lower():
                conflict_index = idx
                break

        entry["name"] = name
        entry["description"] = description.strip()

        if conflict_index is not None:
            choice = QMessageBox.question(
                self,
                "Overwrite Supermodule",
                "A supermodule with this name already exists. Overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if choice != QMessageBox.Yes:
                return
            self.supermodules[conflict_index] = entry
            self.supermodules.pop(super_index)
        else:
            self.supermodules[super_index] = entry
        self._save_supermodules()
        self._refresh_supermodule_list()

    def _duplicate_module_at_index(self, index):
        if index < 0 or index >= len(self.selected_modules):
            return
        mod_id, config = self.selected_modules[index]
        new_config = copy.deepcopy(config)
        new_config.pop("position", None)
        self._assign_module_position(new_config, mod_id=mod_id)
        insert_row = index + 1
        self.selected_modules.insert(insert_row, (mod_id, new_config))
        self.selected_list.insertItem(insert_row, self._build_selected_list_item(mod_id, new_config))
        self._shift_connections(insert_row, 1)
        self.selected_list.setCurrentRow(insert_row)
        self._recalc_module_blocks_and_params(insert_row)
        self._refresh_routing_view()

    def remove_selected_module(self):
        """Remove the currently selected module from the patch."""
        selected_items = self.selected_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a module to remove.")
            return
        rows = sorted({self.selected_list.row(item) for item in selected_items}, reverse=True)
        for row in rows:
            if row < 0 or row >= len(self.selected_modules):
                continue
            self.selected_list.takeItem(row)
            self.selected_modules.pop(row)
            self._shift_connections(row, -1)
        self.clear_module_details()
        self._refresh_routing_view()

    def save_selected_supermodule(self):
        selected_items = self.selected_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Select one or more modules to save.")
            return

        selected_rows = sorted({self.selected_list.row(item) for item in selected_items})
        name, description, ok = self._prompt_supermodule_metadata(
            name="",
            description="",
            title="Save Supermodule",
        )
        if not ok:
            return

        modules = []
        index_map = {old: new for new, old in enumerate(selected_rows)}
        for old_index in selected_rows:
            mod_id, config = self.selected_modules[old_index]
            display_name = self._module_display_name(mod_id, config)
            modules.append(
                {
                    "mod_id": str(mod_id),
                    "name": display_name,
                    "config": copy.deepcopy(config),
                }
            )

        connections = []
        for conn in self.connections:
            source_mod, source_block = conn["source"].split(".")
            dest_mod, dest_block = conn["destination"].split(".")
            source_mod = int(source_mod)
            dest_mod = int(dest_mod)
            if source_mod in index_map and dest_mod in index_map:
                new_conn = copy.deepcopy(conn)
                new_conn["source"] = f"{index_map[source_mod]}.{source_block}"
                new_conn["destination"] = f"{index_map[dest_mod]}.{dest_block}"
                try:
                    new_conn["source_raw"] = int(index_map[source_mod])
                    new_conn["dest_raw"] = int(index_map[dest_mod])
                    new_conn["source_block_raw"] = int(source_block)
                    new_conn["dest_block_raw"] = int(dest_block)
                except ValueError:
                    new_conn.pop("source_raw", None)
                    new_conn.pop("source_block_raw", None)
                    new_conn.pop("dest_raw", None)
                    new_conn.pop("dest_block_raw", None)
                connections.append(new_conn)

        supermodule = {
            "name": name,
            "modules": modules,
            "connections": connections,
            "description": description.strip(),
            "created_at": "{:%Y-%m-%dT%H:%M:%S}".format(datetime.datetime.now()),
        }

        existing_index = None
        for idx, item in enumerate(self.supermodules):
            if isinstance(item, dict):
                existing_name = item.get("name", "")
            else:
                existing_name = str(item)
            if str(existing_name).strip().lower() == name.lower():
                existing_index = idx
                break
        if existing_index is not None:
            choice = QMessageBox.question(
                self,
                "Overwrite Supermodule",
                "A supermodule with this name already exists. Overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if choice != QMessageBox.Yes:
                return
            self.supermodules[existing_index] = supermodule
        else:
            self.supermodules.append(supermodule)

        self._save_supermodules()
        self._refresh_supermodule_list()

    def delete_selected_supermodule(self):
        item = self.module_list.currentItem()
        if not item or item.data(0, 1) != "supermodule":
            return
        super_index = item.data(0, Qt.UserRole)
        if super_index is None or super_index < 0 or super_index >= len(self.supermodules):
            return
        choice = QMessageBox.question(
            self,
            "Delete Supermodule",
            "Delete the selected supermodule?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if choice != QMessageBox.Yes:
            return
        self.supermodules.pop(super_index)
        self._save_supermodules()
        self._refresh_supermodule_list()

    def _insert_supermodule(self, supermodule, insert_row, keep_connections):
        modules = supermodule.get("modules", [])
        if not modules:
            return

        invalid = [
            entry.get("mod_id")
            for entry in modules
            if str(entry.get("mod_id")) not in self.module_index
        ]
        if invalid:
            QMessageBox.warning(
                self,
                "Supermodule Error",
                "This supermodule contains modules that are not available in the current module list.",
            )
            return

        valid_modules = [
            entry for entry in modules if str(entry.get("mod_id")) in self.module_index
        ]
        if not valid_modules:
            return

        preferred_start = 0
        preferred_page = 0
        if 0 <= insert_row < len(self.selected_modules):
            ref_cfg = self.selected_modules[insert_row][1]
            if ref_cfg.get("position"):
                preferred_start = ref_cfg["position"][0]
            preferred_page = ref_cfg.get("page", 0)

        self._shift_connections(insert_row, len(valid_modules))

        for offset, entry in enumerate(valid_modules):
            mod_id = str(entry.get("mod_id"))
            config = copy.deepcopy(entry.get("config", {}))
            config.pop("position", None)
            config["page"] = preferred_page
            self._assign_module_position(
                config,
                mod_id=mod_id,
                preferred_start=preferred_start,
                preferred_page=preferred_page,
            )
            self.selected_modules.insert(insert_row + offset, (mod_id, config))
            self.selected_list.insertItem(
                insert_row + offset, self._build_selected_list_item(mod_id, config)
            )
            self._recalc_module_blocks_and_params(insert_row + offset)
            if config.get("position"):
                preferred_start = config["position"][0] + self._module_span_length(config, mod_id)

        self._resolve_inserted_supermodule_cc_conflicts(insert_row, len(valid_modules))

        if keep_connections:
            for conn in supermodule.get("connections", []):
                new_conn = copy.deepcopy(conn)
                source_mod, source_block = new_conn["source"].split(".")
                dest_mod, dest_block = new_conn["destination"].split(".")
                try:
                    source_mod = int(source_mod) + insert_row
                    dest_mod = int(dest_mod) + insert_row
                except ValueError:
                    continue
                new_conn["source"] = f"{source_mod}.{source_block}"
                new_conn["destination"] = f"{dest_mod}.{dest_block}"
                try:
                    new_conn["source_raw"] = int(source_mod)
                    new_conn["dest_raw"] = int(dest_mod)
                    new_conn["source_block_raw"] = int(source_block)
                    new_conn["dest_block_raw"] = int(dest_block)
                except ValueError:
                    new_conn.pop("source_raw", None)
                    new_conn.pop("source_block_raw", None)
                    new_conn.pop("dest_raw", None)
                    new_conn.pop("dest_block_raw", None)
                self.connections.append(new_conn)

    def _resolve_inserted_supermodule_cc_conflicts(self, start_index, count):
        if count <= 0 or start_index < 0:
            return
        end_index = min(start_index + count, len(self.selected_modules))
        if start_index >= end_index:
            return

        used = set()
        for idx, (_mod_id, config) in enumerate(self.selected_modules):
            if start_index <= idx < end_index:
                continue
            cc_map = config.get("starred_cc")
            if not isinstance(cc_map, dict):
                continue
            for value in cc_map.values():
                try:
                    cc = int(value)
                except (TypeError, ValueError):
                    continue
                if 0 <= cc <= 127:
                    used.add(cc)

        def _next_free():
            for cc in range(128):
                if cc not in used:
                    return cc
            return None

        for idx in range(start_index, end_index):
            _mod_id, config = self.selected_modules[idx]
            starred_params = config.get("starred_params")
            if not starred_params:
                continue
            if not isinstance(starred_params, (set, list, tuple)):
                continue
            starred = sorted(str(name) for name in starred_params)
            cc_map = config.get("starred_cc")
            if not isinstance(cc_map, dict):
                cc_map = dict(cc_map) if cc_map else {}

            reassigned = {}
            for param_name in starred:
                desired = cc_map.get(param_name)
                cc_value = None
                try:
                    if desired is not None:
                        parsed = int(desired)
                        if 0 <= parsed <= 127:
                            cc_value = parsed
                except (TypeError, ValueError):
                    cc_value = None

                if cc_value is None or cc_value in used:
                    cc_value = _next_free()
                if cc_value is None:
                    continue

                reassigned[param_name] = cc_value
                used.add(cc_value)

            config["starred_cc"] = reassigned

    def _add_supermodule_from_tree(self, item):
        super_index = item.data(0, Qt.UserRole)
        if super_index is None or super_index < 0 or super_index >= len(self.supermodules):
            return
        supermodule = self.supermodules[super_index]

        insert_row = len(self.selected_modules)
        self._insert_supermodule(supermodule, insert_row, True)
        if insert_row < self.selected_list.count():
            self.selected_list.setCurrentRow(insert_row)
        self._refresh_routing_view()

    def _supermodule_storage_path(self):
        back_path = getattr(self.patch_save, "back_path", None)
        if not back_path:
            return None
        return os.path.join(back_path, "Editor", "supermodules.json")

    def _load_supermodules(self):
        path = self._supermodule_storage_path()
        if not path or not os.path.exists(path):
            self._refresh_supermodule_list()
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            raw = data.get("supermodules", [])
            if isinstance(raw, dict):
                try:
                    ordered = sorted(raw.items(), key=lambda pair: int(pair[0]))
                except (TypeError, ValueError):
                    ordered = raw.items()
                raw = [value for _, value in ordered]
            if not isinstance(raw, list):
                raw = []
            normalized = []
            for entry in raw:
                if isinstance(entry, dict):
                    name = entry.get("name")
                    if name is not None and not isinstance(name, str):
                        entry["name"] = str(name)
                    normalized.append(entry)
                else:
                    normalized.append({"name": str(entry)})
            self.supermodules = normalized
        except (OSError, json.JSONDecodeError):
            self.supermodules = []
        self._refresh_supermodule_list()

    def _save_supermodules(self):
        path = self._supermodule_storage_path()
        if not path:
            QMessageBox.warning(
                self,
                "Supermodule Save Failed",
                "Could not locate the backend directory to save supermodules.",
            )
            return
        try:
            def _json_safe(value):
                if isinstance(value, dict):
                    return {k: _json_safe(v) for k, v in value.items()}
                if isinstance(value, list):
                    return [_json_safe(v) for v in value]
                if isinstance(value, tuple):
                    return [_json_safe(v) for v in value]
                if isinstance(value, set):
                    return sorted(_json_safe(v) for v in value)
                return value

            payload = {"supermodules": _json_safe(self.supermodules)}
            with open(path, "w") as f:
                json.dump(payload, f, indent=2)
        except (OSError, TypeError, ValueError):
            QMessageBox.warning(self, "Supermodule Save Failed", "Unable to save supermodules.")

    def _refresh_supermodule_list(self):
        was_expanded = self.supermodule_category.isExpanded()
        self.supermodule_category.takeChildren()
        for idx, item in enumerate(self.supermodules):
            if isinstance(item, dict):
                name = item.get("name")
            else:
                name = item
            if not isinstance(name, str) or not name.strip():
                name = f"Supermodule {idx + 1}"
            else:
                name = name.strip()
            entry = QTreeWidgetItem([name])
            entry.setText(0, name)
            entry.setData(0, 1, "supermodule")
            entry.setData(0, Qt.UserRole, idx)
            entry.setToolTip(0, self._supermodule_tooltip(item, name))
            self.supermodule_category.addChild(entry)
        self.supermodule_category.setExpanded(was_expanded)
        self._update_supermodule_controls()

    def _supermodule_tooltip(self, entry, fallback_name):
        if isinstance(entry, dict):
            name = entry.get("name", fallback_name)
            modules = entry.get("modules", [])
            description = entry.get("description", "")
        else:
            name = fallback_name
            modules = []
            description = ""

        name = str(name).strip() if name is not None else fallback_name
        description = str(description).strip() if description is not None else ""

        safe_name = html.escape(name)
        tooltip = f"<b>{safe_name}</b>"
        if isinstance(modules, list) and modules:
            lines = []
            for module in modules:
                label = ""
                if isinstance(module, dict):
                    label = module.get("name", "")
                    mod_id = str(module.get("mod_id", ""))
                    if not isinstance(label, str) or not label.strip():
                        mod = self.module_index.get(mod_id, {})
                        label = mod.get("name", "")
                if not isinstance(label, str) or not label.strip():
                    label = "Unnamed Module"
                lines.append(f"• {html.escape(label.strip())}")
            tooltip = f"{tooltip}<br><br>{'<br>'.join(lines)}"
        if description:
            safe_description = html.escape(description).replace("\n", "<br>")
            tooltip = f"{tooltip}<br><br>{safe_description}"
        return tooltip

    def _prompt_supermodule_metadata(self, name, description, title):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel("Name:"))
        name_edit = QLineEdit(dialog)
        name_edit.setText(name or "")
        layout.addWidget(name_edit)

        layout.addWidget(QLabel("Description:"))

        text_edit = QTextEdit(dialog)
        text_edit.setAcceptRichText(False)
        text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        text_edit.setPlainText(description or "")
        text_edit.setMinimumSize(420, 160)
        layout.addWidget(text_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.Accepted:
            return "", "", False
        final_name = name_edit.text().strip()
        if not final_name:
            QMessageBox.warning(self, "Invalid Name", "Supermodule name cannot be empty.")
            return "", "", False
        return final_name, text_edit.toPlainText(), True

    def _update_supermodule_controls(self):
        item = self.module_list.currentItem()
        is_supermodule = bool(item) and item.data(0, 1) == "supermodule"
        self.supermodule_delete_btn.setEnabled(is_supermodule)

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
        module_type = mod.get("name", "")
        display_name = self._module_display_name(mod_id, config)
        # Module info header
        if display_name and display_name != module_type:
            info_text = f"<b>{display_name} [{module_type}]</b>"
        else:
            info_text = f"<b>{module_type}</b>"
        info_label = QLabel(info_text)
        info_label.setToolTip(self._module_tooltip(mod_id, module_type))
        self.details_layout.addWidget(info_label)

        # CPU info
        cpu_label = QLabel(f"CPU: {mod['cpu']}")
        self.details_layout.addWidget(cpu_label)

        override_row = QHBoxLayout()
        save_override_btn = EditorButton("Save as Default Override")
        save_override_btn.clicked.connect(lambda: self._save_module_override(mod_id, config))
        reset_btn = EditorButton("Reset to Module Defaults")
        reset_btn.clicked.connect(lambda: self._reset_options(module_index))
        override_row.addWidget(save_override_btn)
        override_row.addWidget(reset_btn)
        self.details_layout.addLayout(override_row)

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
            self._update_param_display(control_key)

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
            self._update_param_display(control_key)

    def on_param_star_toggled(self, checked):
        sender = self.sender()
        if sender is None:
            return
        param_name = sender.property("param_name")
        module_index = sender.property("module_index")
        if param_name is None or module_index is None:
            return
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        _mod_id, config = self.selected_modules[module_index]
        starred = config.get("starred_params")
        if not isinstance(starred, set):
            starred = set(starred) if starred else set()
        if checked:
            starred.add(param_name)
        else:
            starred.discard(param_name)
        config["starred_params"] = starred
        cc_map = config.get("starred_cc")
        if not isinstance(cc_map, dict):
            cc_map = dict(cc_map) if cc_map else {}
        if not checked:
            cc_map.pop(param_name, None)
        config["starred_cc"] = cc_map
        control_key = f"{module_index}_{param_name}"
        controls = self.param_controls.get(control_key, {})
        cc_spinbox = controls.get("cc_spinbox")
        if cc_spinbox:
            cc_spinbox.setEnabled(checked)
            if checked and cc_spinbox.value() < 0:
                self._assign_next_available_cc(module_index, param_name)
            elif not checked:
                cc_spinbox.blockSignals(True)
                cc_spinbox.setValue(-1)
                cc_spinbox.blockSignals(False)
        if checked:
            self._assign_next_available_cc(module_index, param_name)
        self._enforce_unique_cc(module_index, param_name if checked else None)

    def on_param_cc_changed(self, value):
        sender = self.sender()
        if sender is None:
            return
        param_name = sender.property("param_name")
        module_index = sender.property("module_index")
        if param_name is None or module_index is None:
            return
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        _mod_id, config = self.selected_modules[module_index]
        if int(value) < 0:
            return
        cc_map = config.get("starred_cc")
        if not isinstance(cc_map, dict):
            cc_map = dict(cc_map) if cc_map else {}
        cc_map[param_name] = int(value)
        config["starred_cc"] = cc_map
        self._enforce_unique_cc(module_index, param_name)

    def _enforce_unique_cc(self, module_index, changed_param=None):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        _mod_id, config = self.selected_modules[module_index]
        cc_map = config.get("starred_cc")
        if not isinstance(cc_map, dict):
            cc_map = dict(cc_map) if cc_map else {}

        # Gather starred params for this module
        starred_params = config.get("starred_params")
        if not isinstance(starred_params, set):
            starred_params = set(starred_params) if starred_params else set()

        # Build control map for params in this module
        controls_by_param = {}
        for key, controls in self.param_controls.items():
            if controls.get("module_index") == module_index:
                pname = controls.get("param_name")
                if pname:
                    controls_by_param[pname] = controls

        def _next_free(start=0):
            for v in range(start, 128):
                if v not in used:
                    return v
            return None

        # Build used set across whole patch
        used = self._all_starred_cc_values(exclude=(module_index, changed_param))

        # Rebuild deterministically: prefer changed_param to keep its value
        assigned = {}
        if changed_param and changed_param in starred_params:
            keep = int(cc_map.get(changed_param, 0))
            assigned[changed_param] = keep
            used.add(keep)

        for pname in sorted(starred_params):
            if pname == changed_param:
                continue
            desired = int(cc_map.get(pname, 0))
            if desired in used:
                desired = _next_free(0)
            if desired is None:
                continue
            assigned[pname] = desired
            used.add(desired)

        # Apply assignments to config + UI
        for pname, value in assigned.items():
            cc_map[pname] = int(value)
            controls = controls_by_param.get(pname, {})
            spinbox = controls.get("cc_spinbox")
            if spinbox and spinbox.value() != value:
                spinbox.blockSignals(True)
                spinbox.setValue(int(value))
                spinbox.blockSignals(False)
        config["starred_cc"] = cc_map

    def _all_starred_cc_values(self, exclude=None):
        used = set()
        for idx, (_mod_id, config) in enumerate(self.selected_modules):
            cc_map = config.get("starred_cc")
            if not isinstance(cc_map, dict):
                continue
            for pname, value in cc_map.items():
                if exclude and exclude == (idx, pname):
                    continue
                if value is None:
                    continue
                used.add(int(value))
        return used

    def _assign_next_available_cc(self, module_index, param_name):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        _mod_id, config = self.selected_modules[module_index]
        cc_map = config.get("starred_cc")
        if not isinstance(cc_map, dict):
            cc_map = dict(cc_map) if cc_map else {}
        if param_name in cc_map:
            return
        used = self._all_starred_cc_values()
        control_key = f"{module_index}_{param_name}"
        controls = self.param_controls.get(control_key, {})
        spinbox = controls.get("cc_spinbox")
        if spinbox:
            desired = int(spinbox.value())
            if desired >= 0 and desired not in used:
                cc_map[param_name] = desired
                config["starred_cc"] = cc_map
                return
        for v in range(128):
            if v not in used:
                cc_map[param_name] = v
                config["starred_cc"] = cc_map
                if spinbox:
                    spinbox.blockSignals(True)
                    spinbox.setValue(int(v))
                    spinbox.blockSignals(False)
                return
    def _update_param_display(self, control_key):
        controls = self.param_controls.get(control_key)
        if not controls:
            return
        spinbox = controls.get("spinbox")
        display_label = controls.get("display_label")
        display_meta = controls.get("display_meta")
        if not spinbox or not display_label:
            return
        display_label.setText(
            self._format_param_display(spinbox.value(), display_meta)
        )

    def _param_display_meta(self, mod_id, param_name, options=None):
        mod = self.module_index.get(str(mod_id), {})
        defaults = mod.get("param_defaults") or mod.get("param_default") or {}
        if isinstance(defaults, dict):
            meta = defaults.get(param_name)
            if isinstance(meta, dict):
                return self._scale_param_meta(mod_id, param_name, meta, options)
        return {"unit": None, "range": None, "value": None}

    def _scale_param_meta(self, mod_id, param_name, meta, options):
        unit = meta.get("unit")
        display_range = meta.get("range")
        scaled_range = display_range
        if isinstance(display_range, (list, tuple)) and display_range and isinstance(options, dict):
            if unit == "ms" and options.get("max_time") is not None:
                factor = self._max_time_scale(options.get("max_time"), base_seconds=16.0)
                if factor is not None and all(isinstance(v, (int, float)) for v in display_range):
                    scaled_range = [float(v) * factor for v in display_range]
            elif str(mod_id) == "30" and options.get("length_edit") == "on":
                if param_name in ("loop_length", "start_position") and unit == "s":
                    factor = self._max_time_scale(options.get("max_rec_time"), base_seconds=32.0)
                    if factor is not None and all(isinstance(v, (int, float)) for v in display_range):
                        scaled_range = [float(v) * factor for v in display_range]
            elif str(mod_id) == "83":
                if param_name in ("grain_size", "grain_position") and unit == "ms":
                    factor = self._max_time_scale(options.get("max_grain_size"), base_seconds=16.0)
                    if factor is not None and all(isinstance(v, (int, float)) for v in display_range):
                        scaled_range = [float(v) * factor for v in display_range]
        return {
            "unit": meta.get("unit"),
            "range": scaled_range,
            "value": meta.get("value"),
        }

    @staticmethod
    def _max_time_scale(max_time, base_seconds=16.0):
        if max_time is None:
            return None
        if isinstance(max_time, (int, float)):
            seconds = float(max_time)
        elif isinstance(max_time, str):
            s = max_time.strip().lower()
            if s.endswith("ms"):
                try:
                    seconds = float(s[:-2].strip()) / 1000.0
                except ValueError:
                    return None
            elif s.endswith("s"):
                try:
                    seconds = float(s[:-1].strip())
                except ValueError:
                    return None
            else:
                return None
        else:
            return None
        return seconds / float(base_seconds) if seconds > 0 and base_seconds else None

    def _format_param_display(self, value, meta):
        unit = None
        display_range = None
        default_value = None
        if isinstance(meta, dict):
            unit = meta.get("unit")
            display_range = meta.get("range")
            default_value = meta.get("value")
        if isinstance(display_range, (list, tuple)) and display_range:
            first = display_range[0]
            last = display_range[-1]
            if (
                unit == "dB"
                and isinstance(first, (int, float))
                and float(first) == float("-inf")
                and float(value) <= 0.0
            ):
                return "-inf dB"
            last_is_inf = isinstance(last, (int, float)) and float(last) == float("inf")
            if last_is_inf and float(value) >= 1.0:
                return f"inf {unit}".strip()
            display_range = [
                (487.68 if (unit == "s" and last_is_inf and isinstance(v, (int, float)) and float(v) == float("inf")) else
                 120.0 if (isinstance(v, (int, float)) and float(v) == float("inf")) else
                 -120.0 if (isinstance(v, (int, float)) and float(v) == float("-inf")) else v)
                for v in display_range
            ]
        mapped = float(value)
        if isinstance(display_range, (list, tuple)) and display_range:
            if (
                len(display_range) == 2
                and all(isinstance(v, (int, float)) for v in display_range)
            ):
                lo, hi = float(display_range[0]), float(display_range[1])
                mapped = lo + (hi - lo) * float(value)
            elif (
                len(display_range) == 5
                and all(isinstance(v, (int, float)) for v in display_range)
            ):
                anchors = [0.0, 0.25, 0.5, 0.75, 1.0]
                values = list(display_range)
                if (
                    unit == "dB"
                    and isinstance(default_value, (int, float))
                    and 0.0 not in values
                    and 0.0 < float(default_value) < 1.0
                ):
                    pairs = list(zip(anchors, values))
                    pairs.append((float(default_value), 0.0))
                    pairs.sort(key=lambda item: item[0])
                    anchors = [p[0] for p in pairs]
                    values = [p[1] for p in pairs]
                mapped = self._piecewise_interpolate(float(value), anchors, values)
        if unit:
            return f"{mapped:.1f} {unit}"
        return f"{mapped:.1f}"

    def _piecewise_interpolate(self, x, xs, ys):
        if x <= xs[0]:
            return float(ys[0])
        if x >= xs[-1]:
            return float(ys[-1])
        for i in range(1, len(xs)):
            x0, x1 = xs[i - 1], xs[i]
            if x <= x1:
                y0, y1 = float(ys[i - 1]), float(ys[i])
                if x1 == x0:
                    return y1
                t = (x - x0) / (x1 - x0)
                t = t ** 1.6
                return y0 + (y1 - y0) * t
        return float(ys[-1])

    def clear_module_details(self):
        """Clear the module details panel."""
        self.current_module_index = None
        self._reset_details_container()

    def export_patch(self):
        patch_dict = self._build_patch_dict()

        cpu_total = patch_dict.get("meta", {}).get("cpu")
        if cpu_total is not None and cpu_total >= 100:
            if cpu_total >= 105:
                message = f"This patch reports an extremely high CPU usage of {cpu_total}%, which is above the hardware limit. Export anyway?"
            else:
                message = f"This patch reports a high CPU usage of {cpu_total}%, which is close to the hardware limit. Export anyway?"
            choice = QMessageBox.warning(
                self,
                "High CPU Usage",
                message,
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Cancel,
            )
            if choice != QMessageBox.Ok:
                return

        if not self.patch_dict:
            title, ok = QInputDialog.getText(
                self, "Patch Title", "Enter a patch title:"
            )
            if not ok or not title.strip():
                return
            patch_name = title.strip()
            patch_dict["name"] = patch_name
            if "meta" in patch_dict:
                patch_dict["meta"]["name"] = patch_name
        else:
            choice = QDialog(self)
            choice.setWindowTitle("Export Patch")
            choice.setModal(True)
            layout = QVBoxLayout(choice)
            layout.addWidget(QLabel("How should this edited patch be saved?"))
            overwrite_btn = EditorButton("Overwrite Existing")
            new_version_btn = EditorButton("Create New Version")
            cancel_btn = EditorButton("Cancel")
            layout.addWidget(overwrite_btn)
            layout.addWidget(new_version_btn)
            layout.addWidget(cancel_btn)
            choice.setLayout(layout)

            result = {"button": None}

            def _choose(btn):
                result["button"] = btn
                choice.accept()

            overwrite_btn.clicked.connect(lambda: _choose(overwrite_btn))
            new_version_btn.clicked.connect(lambda: _choose(new_version_btn))
            cancel_btn.clicked.connect(choice.reject)
            choice.exec()

            if result["button"] not in (new_version_btn, overwrite_btn):
                return

            patch_name = patch_dict.get("name", "UserPatch")

        try:
            encoder = PatchEncoder()
            bin_data = encoder.encode(patch_dict, param_order_mode="order")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))
            return

        if not self.patch_dict:
            timestamp = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
            file_base = patch_name.replace(" ", "_")
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
                    {"id": patch_id, "filename": "000_zoia_{}.bin".format(file_base)}
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

        patch_id = self.patch_id
        version = None
        if patch_id:
            patch_id, version = self._split_versioned_patch_id(patch_id)
        meta = None
        if patch_id:
            meta, version = self._load_backend_metadata(patch_id, version=version)
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
            if result["button"] == new_version_btn:
                self.patch_save.save_to_backend((bin_bytes, meta), version=True)
            else:
                target = os.path.join(self.patch_save.back_path, str(patch_id))
                os.makedirs(target, exist_ok=True)
                if version is not None:
                    name_bin = os.path.join(target, "{}_v{}.bin".format(patch_id, version))
                else:
                    name_bin = os.path.join(target, "{}.bin".format(patch_id))
                with open(name_bin, "wb") as f:
                    f.write(bin_bytes)
                if version is not None:
                    self.patch_save.save_metadata_json(meta, version)
                else:
                    self.patch_save.save_metadata_json(meta)
            QMessageBox.information(self, "Export Success", "Patch saved to backend.")
            self._notify_close_refresh()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def closeEvent(self, event):
        if self.routing_window and self.routing_window.isVisible():
            self.routing_window.close()
        if self.page_layout_window and self.page_layout_window.isVisible():
            self.page_layout_window.close()
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

        starred = self.patch_dict.get("starred", [])
        for module in self.patch_dict["modules"]:
            mod_id = str(module["mod_idx"])
            mod = self.module_index.get(mod_id)
            if mod:
                self._normalize_options_order(mod_id, module)
                self._remap_params_from_block_order(mod_id, module)
                self._apply_starred_params(mod_id, module, starred)
                # Store the full module dict from the patch (includes parameters)
                self.selected_modules.append((mod_id, module))
                self.selected_list.addItem(self._build_selected_list_item(mod_id, module))

    def _init_new_patch_defaults(self):
        audio_in_id = "1"
        audio_out_id = "2"
        if audio_in_id not in self.module_index or audio_out_id not in self.module_index:
            return

        for mod_id in (audio_in_id, audio_out_id):
            config = self._default_module_config(mod_id)
            self._assign_module_position(config, mod_id=mod_id)
            self.selected_modules.append((mod_id, config))
            self.selected_list.addItem(self._build_selected_list_item(mod_id, config))

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
        starred = self._build_starred_params()

        max_page = 0
        for _, config in self.selected_modules:
            max_page = max(max_page, int(config.get("page", 0)))
        while len(pages) < max_page + 1:
            pages.append("")

        if self._pending_pages is not None:
            pages = list(self._pending_pages)
        if self._pending_page_names:
            pages = list(pages)
            for idx, name in self._pending_page_names.items():
                if idx < 0:
                    continue
                while len(pages) <= idx:
                    pages.append("")
                pages[idx] = name

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

    def _build_starred_params(self):
        starred = []
        for index, (mod_id, config) in enumerate(self.selected_modules):
            starred_params = config.get("starred_params")
            if not starred_params:
                continue
            if not isinstance(starred_params, (set, list, tuple)):
                continue
            blocks = config.get("blocks") or self.module_index.get(str(mod_id), {}).get("blocks", {})
            cc_map = config.get("starred_cc") if isinstance(config.get("starred_cc"), dict) else {}
            for param_name in starred_params:
                meta = blocks.get(param_name)
                if not meta or not meta.get("isParam"):
                    continue
                position = meta.get("position")
                if isinstance(position, list):
                    if not position:
                        continue
                    block_idx = position[0]
                else:
                    block_idx = position
                if block_idx is None:
                    continue
                midi_cc = cc_map.get(param_name, "None")
                if midi_cc is None:
                    midi_cc = "None"
                starred.append(
                    {"module": int(index), "block": int(block_idx), "midi_cc": midi_cc}
                )
        return starred

    def _apply_starred_params(self, mod_id, module, starred):
        if not isinstance(starred, list) or not starred:
            return
        mod_number = module.get("number")
        if mod_number is None:
            return
        blocks = module.get("blocks") or self.module_index.get(str(mod_id), {}).get("blocks", {})
        starred_params = set()
        starred_cc = {}
        for star in starred:
            if star.get("module") != mod_number:
                continue
            block_idx = star.get("block")
            if block_idx is None:
                continue
            for name, meta in blocks.items():
                position = meta.get("position")
                if isinstance(position, list) and block_idx in position:
                    starred_params.add(name)
                    if star.get("midi_cc") != "None":
                        starred_cc[name] = int(star.get("midi_cc"))
                    break
                if isinstance(position, int) and block_idx == position:
                    starred_params.add(name)
                    if star.get("midi_cc") != "None":
                        starred_cc[name] = int(star.get("midi_cc"))
                    break
        if starred_params:
            module["starred_params"] = starred_params
        if starred_cc:
            module["starred_cc"] = starred_cc

    def _module_to_patch_format(self, mod_id, position, number, config):
        mod = self.module_index[mod_id]

        # Use edited parameters from config if available
        if config and "parameters" in config:
            parameters = dict(config["parameters"])
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

        if config is not None and config.get("params_auto", True):
            blocks = config.get("blocks") or mod.get("blocks", {})
            for name, meta in blocks.items():
                if meta.get("isParam") and name not in parameters:
                    parameters[name] = float(self._param_default_value(mod_id, name))
            params_count = len(parameters)
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
            "parameters_raw": [],
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

        def refresh_source_blocks():
            source_idx = source_combo.currentData()
            if source_idx is None:
                return
            self._populate_block_combo(
                source_block,
                self.selected_modules[source_idx][0],
                self.selected_modules[source_idx][1],
                allowed_types={"audio_out", "cv_out"},
            )

        def refresh_dest_blocks():
            dest_idx = dest_combo.currentData()
            if dest_idx is None:
                return
            source_idx = source_combo.currentData()
            source_type = None
            if source_idx is not None:
                source_type = self._block_type_for_module(
                    self.selected_modules[source_idx][0],
                    self.selected_modules[source_idx][1],
                    source_block.currentData(),
                )
            allowed_types = self._matching_dest_types(source_type)
            self._populate_block_combo(
                dest_block,
                self.selected_modules[dest_idx][0],
                self.selected_modules[dest_idx][1],
                allowed_types=allowed_types,
            )

        def refresh_on_source_module_change():
            refresh_source_blocks()
            refresh_dest_blocks()

        refresh_on_source_module_change()
        refresh_dest_blocks()

        source_combo.currentIndexChanged.connect(refresh_on_source_module_change)
        source_block.currentIndexChanged.connect(refresh_dest_blocks)
        dest_combo.currentIndexChanged.connect(refresh_dest_blocks)
        strength = QSpinBox()
        strength.setRange(0, 100)
        strength.setValue(100)

        add_btn = EditorButton("Add Connection")
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

            adjust_btn = EditorButton("Adjust Connection Strength")
            adjust_btn.setEnabled(False)
            adjust_btn.clicked.connect(
                lambda: self._adjust_connection_strength(conn_list, module_index)
            )
            remove_btn = EditorButton("Remove Selected Connection")
            remove_btn.setEnabled(False)
            remove_btn.clicked.connect(
                lambda: self._remove_selected_connection(conn_list, module_index)
            )

            def toggle_buttons():
                has_selection = conn_list.currentItem() is not None
                adjust_btn.setEnabled(has_selection)
                remove_btn.setEnabled(has_selection)

            conn_list.itemSelectionChanged.connect(toggle_buttons)
            toggle_buttons()

            list_layout.addWidget(conn_list)
            btn_row = QHBoxLayout()
            btn_row.addWidget(adjust_btn)
            btn_row.addWidget(remove_btn)
            list_layout.addLayout(btn_row)
            connections_layout.addWidget(list_group)
        else:
            connections_layout.addWidget(QLabel("No connections for this module"))

        return connections_group

    def _add_connection(self, source_mod, source_block, dest_mod, dest_block, strength, module_index):
        if source_mod is None or dest_mod is None:
            return
        if source_block is None or dest_block is None:
            return
        if not self._is_valid_connection(
            source_mod, source_block, dest_mod, dest_block
        ):
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

    def _adjust_connection_strength(self, conn_list, module_index):
        item = conn_list.currentItem()
        if not item:
            return
        conn_index = item.data(1)
        if conn_index is None:
            return
        if not (0 <= conn_index < len(self.connections)):
            return

        conn = self.connections[conn_index]
        current_strength = int(conn.get("strength", 100))

        dialog = QDialog(self)
        dialog.setWindowTitle("Adjust Connection Strength")
        layout = QVBoxLayout(dialog)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(current_strength)

        spin = QSpinBox()
        spin.setRange(0, 100)
        spin.setValue(current_strength)

        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)

        btn_row = QHBoxLayout()
        ok_btn = EditorButton("Apply")
        cancel_btn = EditorButton("Cancel")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        btn_row.addStretch()
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)

        layout.addWidget(QLabel("Strength (%):"))
        layout.addWidget(slider)
        layout.addWidget(spin)
        layout.addLayout(btn_row)

        if dialog.exec() != QDialog.Accepted:
            return

        new_strength = int(slider.value())
        conn["strength"] = new_strength
        conn["strength_raw"] = new_strength * 100
        self._refresh_current_details()
        self._refresh_routing_view()

    def _module_display_name(self, mod_id, config):
        mod_id = str(mod_id)
        mod = self.module_index.get(mod_id, {})
        return config.get("name") if config and config.get("name") else mod.get("name", "")

    def _module_description(self, mod_id):
        mod = self.module_index.get(str(mod_id), {})
        raw = mod.get("description", "")
        if raw is None:
            return ""
        return " ".join(str(raw).split())

    def _module_tooltip(self, mod_id, display_name=None):
        mod = self.module_index.get(str(mod_id), {})
        name = display_name or mod.get("name", "")
        description = self._module_description(mod_id)
        if description:
            return f"<b>{name}</b><br><br>{description}"
        return f"<b>{name}</b>"

    def _build_selected_list_item(self, mod_id, config):
        mod = self.module_index.get(str(mod_id), {})
        module_type = mod.get("name", "")
        custom_name = config.get("name") if isinstance(config, dict) else None
        custom_name = custom_name.strip() if isinstance(custom_name, str) else ""

        if custom_name and custom_name != module_type:
            label = f"{custom_name} [{module_type}]"
        else:
            label = module_type

        item = QListWidgetItem(label)
        tooltip = self._module_tooltip(mod_id, module_type)
        if custom_name and custom_name != module_type:
            tooltip = f"{tooltip}<br><br>Custom Name: {custom_name}"
        item.setToolTip(tooltip)
        return item

    def _module_start_position(self, config):
        position = config.get("position", [0]) if config else [0]
        if isinstance(position, list) and position:
            try:
                return int(min(position))
            except (TypeError, ValueError):
                return 0
        if isinstance(position, int):
            return int(position)
        return 0

    def _module_relative_positions(self, config, mod_id):
        blocks = config.get("blocks", {}) if config else {}
        positions = []
        for meta in blocks.values():
            position = meta.get("position")
            if isinstance(position, list):
                for pos in position:
                    try:
                        positions.append(int(pos))
                    except (TypeError, ValueError):
                        continue
            elif isinstance(position, int):
                positions.append(int(position))

        if positions:
            unique = sorted(set(positions))
            return list(range(len(unique)))

        position = config.get("position", [0]) if config else [0]
        if isinstance(position, list) and len(position) > 1:
            cleaned = []
            for pos in position:
                try:
                    cleaned.append(int(pos))
                except (TypeError, ValueError):
                    continue
            if cleaned:
                unique = sorted(set(cleaned))
                return list(range(len(unique)))

        span = self.module_index.get(str(mod_id), {}).get("min_blocks", 1)
        return list(range(max(1, int(span))))

    def _module_absolute_positions(self, mod_id, config):
        start = self._module_start_position(config)
        rel_positions = self._module_relative_positions(config, mod_id)
        return [start + rel for rel in rel_positions]

    def _is_positions_free(self, page, positions, ignore_index=None):
        occupied = self._occupied_positions(ignore_index=ignore_index).get(page, set())
        return all(pos not in occupied for pos in positions)

    def _module_span_length(self, config, mod_id):
        rel_positions = self._module_relative_positions(config, mod_id)
        if rel_positions:
            return max(rel_positions) + 1
        return 1

    def _occupied_positions(self, ignore_index=None):
        occupied = {}
        for idx, (mod_id, cfg) in enumerate(self.selected_modules):
            if ignore_index is not None and idx == ignore_index:
                continue
            if not cfg.get("position"):
                continue
            page = cfg.get("page", 0)
            module_positions = self._module_absolute_positions(mod_id, cfg)
            occupied.setdefault(page, set())
            for pos in module_positions:
                occupied[page].add(pos)
        return occupied

    def _is_span_free(self, page, start, span, ignore_index=None):
        return self._is_positions_free(
            page, list(range(int(start), int(start) + int(span))), ignore_index=ignore_index
        )

    def _assign_module_position(self, config, mod_id=None, preferred_start=0, module_index=None, preferred_page=None):
        if mod_id is None:
            mod_id = config.get("mod_idx", 0)
        rel_positions = self._module_relative_positions(config, mod_id)
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
            candidates = [start] + list(range(0, max_pos - span + 2))
            checked = set()
            for candidate in candidates:
                if candidate in checked:
                    continue
                checked.add(candidate)
                positions = [candidate + rel for rel in rel_positions]
                if any(pos < 0 or pos > max_pos for pos in positions):
                    continue
                if self._is_positions_free(current_page, positions, module_index):
                    config["position"] = [candidate]
                    config["page"] = current_page
                    return

        new_page = max_page + 1
        config["position"] = [0]
        config["page"] = new_page

    def _default_module_config_base(self, mod_id):
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

        config = {
            "options": options,
            "options_binary": options_binary,
            "blocks": blocks,
            "params": mod.get("params", 0),
            "size_of_saveable_data": 0,
            "parameters": self._default_parameters_from_blocks(mod_id, {"blocks": blocks}),
            "params_auto": True,
            "page": 0,
        }
        return config

    def _default_module_config(self, mod_id):
        config = self._default_module_config_base(mod_id)
        return self._apply_module_overrides(mod_id, config)

    def _module_override_storage_path(self):
        back_path = getattr(self.patch_save, "back_path", None)
        if not back_path:
            return None
        return os.path.join(back_path, "Editor", "defaults.json")

    def _load_module_overrides(self):
        path = self._module_override_storage_path()
        if not path or not os.path.exists(path):
            self.module_overrides = {}
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            overrides = data.get("overrides", {})
            if isinstance(overrides, dict):
                self.module_overrides = overrides
            else:
                self.module_overrides = {}
        except (OSError, json.JSONDecodeError):
            self.module_overrides = {}

    def _save_module_overrides(self):
        path = self._module_override_storage_path()
        if not path:
            QMessageBox.warning(
                self,
                "Override Save Failed",
                "Could not locate the backend directory to save overrides.",
            )
            return
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump({"overrides": self.module_overrides}, f, indent=2)
        except OSError:
            QMessageBox.warning(self, "Override Save Failed", "Unable to save overrides.")

    def _apply_module_overrides(self, mod_id, config):
        overrides = self.module_overrides.get(str(mod_id))
        if not overrides:
            return config

        if isinstance(overrides, dict):
            override_color = overrides.get("color")
            if isinstance(override_color, str) and override_color:
                config["color"] = override_color

            override_options = overrides.get("options")
            if isinstance(override_options, dict):
                config["options"] = copy.deepcopy(override_options)
                options_binary = {}
                options_def = self.module_index.get(str(mod_id), {}).get("options", {})
                for name, values in options_def.items():
                    if not isinstance(values, list) or not values:
                        continue
                    selected = override_options.get(name, values[0])
                    try:
                        options_binary[name] = values.index(selected)
                    except ValueError:
                        options_binary[name] = 0
                config["options_binary"] = options_binary
                try:
                    config["blocks"] = self._patch_binary._calc_blocks(
                        {"mod_idx": int(mod_id), "version": 1, "options": config["options"]}
                    )
                except Exception:
                    pass

            override_params = overrides.get("parameters")
            if isinstance(override_params, dict):
                defaults = self._default_parameters_from_blocks(mod_id, config)
                for name, value in override_params.items():
                    if name in defaults:
                        defaults[name] = float(value)
                config["parameters"] = defaults

        return config

    def _save_module_override(self, mod_id, config):
        if not mod_id or not config:
            return
        mod_id = str(mod_id)
        override = {
            "color": config.get("color", "Blue"),
            "options": copy.deepcopy(config.get("options", {})),
            "parameters": copy.deepcopy(config.get("parameters", {})),
        }
        self.module_overrides[mod_id] = override
        self._save_module_overrides()
        QMessageBox.information(self, "Default Override Saved", "Module defaults updated.")

    def _default_parameters_from_blocks(self, mod_id, config):
        blocks = {}
        if config and config.get("blocks"):
            blocks = config["blocks"]
        else:
            blocks = self.module_index.get(str(mod_id), {}).get("blocks", {})

        params = {}
        ordered = self._param_order(mod_id, blocks, use_order_field=False)
        for name in ordered:
            if name in blocks and blocks[name].get("isParam"):
                params[name] = float(self._param_default_value(mod_id, name))
        return params

    def _param_default_value(self, mod_id, param_name):
        mod = self.module_index.get(str(mod_id), {})
        defaults = mod.get("param_defaults") or mod.get("param_default") or {}
        if isinstance(defaults, dict) and param_name in defaults:
            entry = defaults[param_name]
            if isinstance(entry, dict):
                return entry.get("value", 0.0)
            return entry
        return 0.0

    def _param_order(self, mod_id, blocks, use_order_field=True):
        mod = self.module_index.get(str(mod_id), {})
        defaults = mod.get("param_defaults") or mod.get("param_default") or {}
        if isinstance(defaults, dict) and defaults:
            if use_order_field and any(
                isinstance(meta, dict) and "order" in meta
                for _, meta in defaults.items()
            ):
                items = list(defaults.items())
                items.sort(
                    key=lambda item: item[1].get("order", 0)
                    if isinstance(item[1], dict)
                    else 0
                )
                return [name for name, _ in items if name in blocks]
            return [name for name in defaults.keys() if name in blocks]

        return [name for name, meta in blocks.items() if meta.get("isParam")]

    def _remap_params_from_block_order(self, mod_id, module):
        params = module.get("parameters")
        if not isinstance(params, dict) or not params:
            return

        blocks = module.get("blocks") or self.module_index.get(str(mod_id), {}).get("blocks", {})
        block_order = [name for name, meta in blocks.items() if meta.get("isParam")]
        if not block_order:
            return

        order_list = self._param_order(mod_id, blocks, use_order_field=True)
        if not order_list:
            return

        params_count = int(module.get("params", min(len(block_order), len(order_list))))
        block_order = block_order[:params_count]
        order_list = order_list[:params_count]
        if block_order == order_list:
            return

        values = [params.get(name, 0.0) for name in block_order]
        remapped = dict(params)
        for name, value in zip(order_list, values):
            remapped[name] = value
        module["parameters"] = remapped

    def _block_name_for_module(self, mod_id, config, block_index):
        blocks = self._module_blocks(mod_id, config)

        for name, meta in blocks.items():
            position = meta.get("position")
            if isinstance(position, list) and block_index in position:
                return name
            if isinstance(position, int) and block_index == position:
                return name
        return f"Block {block_index}"

    def _module_blocks(self, mod_id, config):
        if config and config.get("blocks"):
            return config["blocks"]
        return self.module_index.get(str(mod_id), {}).get("blocks", {})

    def _block_type_for_module(self, mod_id, config, block_index):
        if block_index is None:
            return None
        blocks = self._module_blocks(mod_id, config)
        for meta in blocks.values():
            position = meta.get("position")
            if isinstance(position, list) and block_index in position:
                return meta.get("type")
            if isinstance(position, int) and block_index == position:
                return meta.get("type")
        return None

    def _matching_dest_types(self, source_type):
        if source_type == "audio_out":
            return {"audio_in"}
        if source_type == "cv_out":
            return {"cv_in"}
        return {"audio_in", "cv_in"}

    def _is_valid_connection(self, source_mod, source_block, dest_mod, dest_block):
        source_type = self._block_type_for_module(
            self.selected_modules[int(source_mod)][0],
            self.selected_modules[int(source_mod)][1],
            int(source_block),
        )
        dest_type = self._block_type_for_module(
            self.selected_modules[int(dest_mod)][0],
            self.selected_modules[int(dest_mod)][1],
            int(dest_block),
        )
        if source_type == "audio_out":
            return dest_type == "audio_in"
        if source_type == "cv_out":
            return dest_type == "cv_in"
        return False

    def _populate_block_combo(self, combo, mod_id, config, allowed_types=None):
        combo.blockSignals(True)
        combo.clear()
        combo.setEnabled(True)
        blocks = self._module_blocks(mod_id, config)

        block_entries = []
        for name, meta in blocks.items():
            block_type = meta.get("type")
            if allowed_types and block_type and block_type not in allowed_types:
                continue
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
            if not blocks:
                for pos in range(0, 128):
                    combo.addItem(f"{pos}: Block {pos}", pos)
            else:
                combo.addItem("No valid blocks", None)
                combo.setEnabled(False)
        combo.blockSignals(False)

    def _build_options_section(self, mod_id, config, module_index):
        mod = self.module_index.get(str(mod_id), {})
        options_def = mod.get("options", {})

        if "options" not in config:
            config["options"] = {}
        if "options_binary" not in config:
            config["options_binary"] = {}

        options_group = QGroupBox("Module Options")
        options_grid = QGridLayout(options_group)

        color_names = [
            "Blue",
            "Green",
            "Red",
            "Yellow",
            "Aqua",
            "Magenta",
            "White",
            "Orange",
            "Lima",
            "Surf",
            "Sky",
            "Purple",
            "Pink",
            "Peach",
            "Mango",
        ]
        current_color = config.get("color", "Blue")
        color_combo = QComboBox()
        color_combo.blockSignals(True)
        for idx, name in enumerate(color_names):
            color_combo.addItem(name.lower(), idx)
            if name == current_color:
                color_combo.setCurrentIndex(idx)
        config["color"] = color_names[color_combo.currentIndex()]
        color_combo.blockSignals(False)
        color_combo.currentIndexChanged.connect(
            lambda idx, mi=module_index, colors=color_names: self._on_color_changed(
                mi, colors, idx
            )
        )
        option_rows = [(QLabel("color"), color_combo)]

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
            option_rows.append((QLabel(opt_name), combo))

        for idx, (label, widget) in enumerate(option_rows):
            row = idx // 2
            col = (idx % 2) * 2
            options_grid.addWidget(label, row, col)
            options_grid.addWidget(widget, row, col + 1)

        # Reset button moved to top section next to override button.
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

    def _on_color_changed(self, module_index, colors, index):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        mod_id, config = self.selected_modules[module_index]
        config["color"] = colors[index]
        self._refresh_routing_view()
        self._recalc_module_blocks_and_params(module_index)
        self._refresh_current_details()
        self._refresh_routing_view()

    def _reset_options(self, module_index):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return
        mod_id, config = self.selected_modules[module_index]
        self.module_overrides.pop(str(mod_id), None)
        self._save_module_overrides()
        defaults = self._default_module_config_base(mod_id)
        config["options"] = defaults.get("options", {})
        config["options_binary"] = defaults.get("options_binary", {})
        config["color"] = defaults.get("color", "Blue")
        config["blocks"] = defaults.get("blocks", {})
        config["parameters"] = defaults.get("parameters", {})
        config["params"] = defaults.get("params", config.get("params", 0))
        config["params_auto"] = defaults.get("params_auto", True)
        config["size_of_saveable_data"] = defaults.get("size_of_saveable_data", 0)
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

        starred_params = config.get("starred_params")
        if not isinstance(starred_params, set):
            starred_params = set(starred_params) if starred_params else set()
        starred_cc = config.get("starred_cc")
        if not isinstance(starred_cc, dict):
            starred_cc = dict(starred_cc) if starred_cc else {}

        order = self._param_order(
            mod_id, self._module_blocks(mod_id, config), use_order_field=False
        )
        if order:
            ordered_params = {name: parameters[name] for name in order if name in parameters}
            # Preserve any extra params not in the order list.
            for name, value in parameters.items():
                if name not in ordered_params:
                    ordered_params[name] = value
            parameters = ordered_params

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

            param_meta = self._param_display_meta(mod_id, param_name, options=config.get("options"))
            display_label = QLabel(self._format_param_display(param_value, param_meta))
            display_label.setMinimumWidth(70)
            param_h_layout.addWidget(display_label)
            star_checkbox = QCheckBox("")
            star_checkbox.setChecked(param_name in starred_params)
            star_checkbox.setProperty("param_name", param_name)
            star_checkbox.setProperty("module_index", module_index)
            star_checkbox.toggled.connect(self.on_param_star_toggled)
            param_h_layout.addWidget(star_checkbox)
            cc_label = QLabel("Starred CC")
            param_h_layout.addWidget(cc_label)
            cc_spinbox = QSpinBox()
            cc_spinbox.setMinimum(-1)
            cc_spinbox.setMaximum(127)
            cc_spinbox.setSpecialValueText("")
            if param_name in starred_cc:
                cc_value = int(starred_cc.get(param_name, 0))
            else:
                cc_value = -1
            cc_spinbox.setValue(cc_value)
            cc_spinbox.setProperty("param_name", param_name)
            cc_spinbox.setProperty("module_index", module_index)
            cc_spinbox.valueChanged.connect(self.on_param_cc_changed)
            cc_spinbox.setEnabled(param_name in starred_params)
            param_h_layout.addWidget(cc_spinbox)

            control_key = f"{module_index}_{param_name}"
            self.param_controls[control_key] = {
                "slider": param_slider,
                "spinbox": param_spinbox,
                "display_label": display_label,
                "display_meta": param_meta,
                "star_checkbox": star_checkbox,
                "cc_label": cc_label,
                "cc_spinbox": cc_spinbox,
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
        self._normalize_options_order(mod_id, config)
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
        starred_params = config.get("starred_params")
        if isinstance(starred_params, set):
            config["starred_params"] = {
                name for name in starred_params if name in new_params
            }
        starred_cc = config.get("starred_cc")
        if isinstance(starred_cc, dict):
            config["starred_cc"] = {
                name: value for name, value in starred_cc.items() if name in new_params
            }
        if config.get("params_auto"):
            config["params"] = len(new_params)
        if config.get("position"):
            positions = self._module_absolute_positions(mod_id, config)
            if not self._is_positions_free(config.get("page", 0), positions, module_index):
                self._assign_module_position(config, mod_id=mod_id, module_index=module_index)

    def _normalize_options_order(self, mod_id, config):
        options_def = self.module_index.get(str(mod_id), {}).get("options", {})
        if not options_def:
            return
        options = config.get("options", {})
        ordered = {}
        for name, values in options_def.items():
            if name in options:
                ordered[name] = options[name]
            elif isinstance(values, list) and values:
                ordered[name] = values[0]
        if ordered:
            config["options"] = ordered

    def toggle_routing_view(self):
        if self.routing_window and self.routing_window.isVisible():
            self.routing_window.close()
            return
        self._open_routing_window()
        self._refresh_routing_view()

    def toggle_page_layout_view(self):
        if self.page_layout_window and self.page_layout_window.isVisible():
            self.page_layout_window.close()
            return
        self._open_page_layout_window()
        self._refresh_page_layout_view()

    def _open_page_layout_window(self):
        if self.page_layout_window and self.page_layout_window.isVisible():
            self.page_layout_window.raise_()
            self.page_layout_window.activateWindow()
            return

        if self.patch_dict is None:
            name = "New Patch"
        else:
            name = self.patch_dict.get("name", "New Patch")

        self.page_layout_window = QMainWindow(self)
        self.page_layout_window.setWindowTitle("Page Layout - {}".format(name))
        self.page_layout_window.setAttribute(Qt.WA_DeleteOnClose, True)
        self.page_layout_window.destroyed.connect(self._on_page_layout_window_closed)

        window_container = QWidget()
        self.page_layout_window_layout = QVBoxLayout(window_container)
        self.page_layout_window_placeholder = QLabel("No page data to display.")
        self.page_layout_window_layout.addWidget(self.page_layout_window_placeholder)

        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.addWidget(QLabel("Pages:"))
        self.page_layout_add_btn = EditorButton("+")
        self.page_layout_remove_btn = EditorButton("-")
        self.page_layout_add_btn.setFixedWidth(28)
        self.page_layout_remove_btn.setFixedWidth(28)
        self.page_layout_add_btn.clicked.connect(self._add_page_layout_page)
        self.page_layout_remove_btn.clicked.connect(self._remove_page_layout_page)
        controls_layout.addWidget(self.page_layout_add_btn)
        controls_layout.addWidget(self.page_layout_remove_btn)
        controls_layout.addStretch()
        self.page_layout_controls = controls
        self.page_layout_window_layout.addWidget(controls)

        self.page_layout_window_scroll = QScrollArea()
        self.page_layout_window_scroll.setWidgetResizable(True)
        self.page_layout_window_container = QWidget()
        self.page_layout_window_scroll.setWidget(self.page_layout_window_container)
        self.page_layout_window_layout.addWidget(self.page_layout_window_scroll)

        self.page_layout_window.setCentralWidget(window_container)
        self.page_layout_window.resize(900, 700)
        self.page_layout_window.show()

    def _on_page_layout_window_closed(self, _obj=None):
        self.page_layout_window = None
        self.page_layout_window_layout = None
        self.page_layout_window_placeholder = None
        self.page_layout_window_scroll = None
        self.page_layout_window_container = None
        self.page_layout_controls = None
        self.page_layout_add_btn = None
        self.page_layout_remove_btn = None

    def _refresh_page_layout_view(self):
        if not (self.page_layout_window and self.page_layout_window.isVisible()):
            return

        patch = self._build_patch_dict()
        if not patch["modules"]:
            if self.page_layout_window_placeholder:
                self.page_layout_window_placeholder.setText("No page data to display.")
            if self.page_layout_remove_btn:
                self.page_layout_remove_btn.setEnabled(False)
            return

        if self.page_layout_window_placeholder:
            self.page_layout_window_placeholder.setText("")

        if self.page_layout_window_scroll is None:
            return

        container = QWidget()
        pages_layout = QVBoxLayout(container)
        old_container = self.page_layout_window_container
        self.page_layout_window_container = container
        self.page_layout_window_scroll.setWidget(container)
        if old_container is not None:
            try:
                old_container.setParent(None)
                old_container.deleteLater()
            except RuntimeError:
                pass

        page_count = max(1, patch.get("pages_count", 1))
        page_names = patch.get("pages", ["Page 1"])
        while len(page_names) < page_count:
            page_names.append(f"Page {len(page_names) + 1}")

        # Build a map of modules per page.
        modules_by_page = {idx: [] for idx in range(page_count)}
        for module in patch["modules"]:
            page = int(module.get("page", 0))
            if page not in modules_by_page:
                modules_by_page[page] = []
            modules_by_page[page].append(module)

        if self.page_layout_remove_btn:
            last_page_modules = modules_by_page.get(page_count - 1, [])
            self.page_layout_remove_btn.setEnabled(len(last_page_modules) == 0 and page_count > 1)

        max_pos = 39
        cols = 8

        for page_index in range(page_count):
            page_group = QGroupBox()
            page_group.setObjectName(f"page_group_{page_index}")
            group_layout = QVBoxLayout(page_group)
            header_layout = QHBoxLayout()
            page_label = QLabel("Page Name:")
            page_name_edit = QLineEdit(page_names[page_index] or f"Page {page_index + 1}")
            page_name_edit.setObjectName(f"page_name_{page_index}")
            page_name_edit.editingFinished.connect(
                lambda idx=page_index, edit=page_name_edit: self._update_page_name(idx, edit.text())
            )
            header_layout.addWidget(page_label)
            header_layout.addWidget(page_name_edit)
            group_layout.addLayout(header_layout)

            grid = QGridLayout()
            grid.setSpacing(2)

            # Initialize empty grid.
            cells = {}
            for pos in range(max_pos + 1):
                row = pos // cols
                col = pos % cols
                cell = PageLayoutCell(
                    page_index,
                    pos,
                    self._on_page_layout_drop,
                )
                cell.setText("")
                cell.setMinimumSize(60, 24)
                cell.setAlignment(Qt.AlignCenter)
                cell.setStyleSheet("border: 1px solid #333333; background: #1b1b1b;")
                grid.addWidget(cell, row, col)
                cells[pos] = cell

            for module in modules_by_page.get(page_index, []):
                module_positions = self._module_absolute_positions(
                    module.get("mod_idx", 0),
                    module,
                )
                color = module.get("color", "Blue")
                text_color = "#ffffff" if color == "Blue" else "#000000"
                label = module.get("name") or module.get("type") or "Module"
                for offset, pos in enumerate(module_positions):
                    if pos > max_pos:
                        continue
                    cell = cells.get(pos)
                    if not cell:
                        continue
                    cell.module_number = module.get("number")
                    cell.setStyleSheet(
                        "border: 1px solid #333333; background: {}; color: {};".format(
                            self._get_color_hex(color),
                            text_color,
                        )
                    )
                    if offset == 0:
                        cell.setText(label)
                    else:
                        cell.setText("")

            group_layout.addLayout(grid)
            pages_layout.addWidget(page_group)

    def _module_positions_for_index(self, module_index):
        if module_index < 0 or module_index >= len(self.selected_modules):
            return [], None
        mod_id, config = self.selected_modules[module_index]
        page = int(config.get("page", 0))
        return self._module_absolute_positions(mod_id, config), page

    def _occupied_positions_exact(self, page, ignore_index=None):
        occupied = set()
        for idx in range(len(self.selected_modules)):
            if ignore_index is not None and idx == ignore_index:
                continue
            positions, mod_page = self._module_positions_for_index(idx)
            if mod_page != page:
                continue
            occupied.update(positions)
        return occupied

    def _move_module_to_position(self, module_index, target_page, target_pos, origin_pos=None):
        positions, _old_page = self._module_positions_for_index(module_index)
        if not positions:
            return
        if origin_pos is None:
            origin_pos = min(positions)
        delta = int(target_pos) - int(origin_pos)
        new_positions = [p + delta for p in positions]

        max_pos = 39
        if any(p < 0 or p > max_pos for p in new_positions):
            return

        occupied = self._occupied_positions_exact(target_page, ignore_index=module_index)
        if any(p in occupied for p in new_positions):
            return

        mod_id, config = self.selected_modules[module_index]
        if isinstance(config.get("position"), list) and len(config.get("position")) > 1:
            config["position"] = new_positions
        else:
            config["position"] = [min(new_positions)]
        config["page"] = int(target_page)
        self._refresh_current_details()
        self._refresh_page_layout_view()
        self._refresh_routing_view()

    def _on_page_layout_drop(self, module_number, origin_pos, target_page, target_pos):
        self._move_module_to_position(module_number, target_page, target_pos, origin_pos=origin_pos)

    def _update_page_name(self, page_index, name):
        if page_index < 0:
            return
        self._ensure_pending_pages()
        while len(self._pending_pages) <= page_index:
            self._pending_pages.append("")
        self._pending_pages[int(page_index)] = name.strip()
        self._pending_page_names[int(page_index)] = name.strip()

    def _ensure_pending_pages(self):
        if self._pending_pages is not None:
            return
        pages = ["Page 1"]
        if self.patch_dict:
            pages = self.patch_dict.get("pages", ["Page 1"])
        max_page = 0
        for _, config in self.selected_modules:
            max_page = max(max_page, int(config.get("page", 0)))
        while len(pages) < max_page + 1:
            pages.append("")
        self._pending_pages = list(pages)

    def _add_page_layout_page(self):
        self._ensure_pending_pages()
        next_index = len(self._pending_pages) + 1
        self._pending_pages.append(f"Page {next_index}")
        self._refresh_page_layout_view()

    def _remove_page_layout_page(self):
        self._ensure_pending_pages()
        if len(self._pending_pages) <= 1:
            return
        last_index = len(self._pending_pages) - 1
        if any(int(cfg.get("page", 0)) == last_index for _, cfg in self.selected_modules):
            return
        self._pending_pages.pop()
        self._pending_page_names.pop(last_index, None)
        self._refresh_page_layout_view()

    def _open_routing_window(self):
        if self.routing_window and self.routing_window.isVisible():
            self.routing_window.raise_()
            self.routing_window.activateWindow()
            return

        if self.patch_dict is None:
            name = "New Patch"
        else:
            name = self.patch_dict.get("name", "New Patch")

        self.routing_window = QMainWindow(self)
        self.routing_window.setWindowTitle("Patch Expander - {}".format(name))
        self.routing_window.setAttribute(Qt.WA_DeleteOnClose, True)
        self.routing_window.destroyed.connect(self._on_routing_window_closed)

        window_container = QWidget()
        self.routing_window_layout = QVBoxLayout(window_container)
        self.routing_window_placeholder = QLabel("No routing data to display.")
        self.routing_window_layout.addWidget(self.routing_window_placeholder)
        self.routing_window_graph_widget = None

        self.routing_window.setCentralWidget(window_container)
        self.routing_window.resize(900, 700)
        self.routing_window.show()

    def _on_routing_window_closed(self, _obj=None):
        self.routing_window = None
        self.routing_window_layout = None
        self.routing_window_placeholder = None
        self.routing_window_graph_widget = None

    def _refresh_routing_view(self):
        if not (self.routing_window and self.routing_window.isVisible()):
            if self.page_layout_window and self.page_layout_window.isVisible():
                self._refresh_page_layout_view()
            return

        layout = self.routing_window_layout
        placeholder = self.routing_window_placeholder
        if self.routing_window_graph_widget:
            layout.removeWidget(self.routing_window_graph_widget)
            self.routing_window_graph_widget.setParent(None)
            self.routing_window_graph_widget.deleteLater()
            self.routing_window_graph_widget = None

        patch = self._build_patch_dict()
        if not patch["modules"]:
            placeholder.setText("No routing data to display.")
            if placeholder.parent() is None:
                layout.addWidget(placeholder)
            return

        placeholder.setText("")
        self.routing_graph = NodeGraph()
        self.routing_graph.set_acyclic(False)
        setup_context_menu(self.routing_graph)
        self.routing_graph.register_nodes([BaseNode])
        self.routing_graph.viewer().use_alt_navigation = False
        self.routing_window_graph_widget = self.routing_graph.widget
        layout.addWidget(self.routing_window_graph_widget)
        self._bind_routing_graph_signals()

        nodes = {}
        self._routing_port_meta = {}
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
            self._register_routing_ports(module["number"], node, in_pos, out_pos)

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

        self._routing_is_building = True
        try:
            for conn in patch["connections"]:
                mod, block = conn["source"].split(".")
                nmod, nblock = conn["destination"].split(".")
                src = data[int(mod)]
                dest = data[int(nmod)]
                try:
                    make_connections(mod, block, nmod, nblock, src, dest)
                except KeyboardInterrupt:
                    break
        finally:
            self._routing_is_building = False

        try:
            self.routing_graph.auto_layout_nodes()
        except (KeyError, RecursionError):
            self.routing_graph.reset_zoom()
        self.routing_graph.fit_to_selection()
        if self.page_layout_window and self.page_layout_window.isVisible():
            self._refresh_page_layout_view()

    def _bind_routing_graph_signals(self):
        if not self.routing_graph:
            return
        signals = getattr(self.routing_graph, "signals", None)
        if signals:
            if hasattr(signals, "connection_created"):
                signals.connection_created.connect(self._on_routing_connection_created)
            if hasattr(signals, "connection_deleted"):
                signals.connection_deleted.connect(self._on_routing_connection_deleted)
            if hasattr(signals, "connection_changed"):
                signals.connection_changed.connect(self._on_routing_connection_changed)
            if hasattr(signals, "port_connected"):
                signals.port_connected.connect(self._on_routing_connection_created)
            if hasattr(signals, "port_disconnected"):
                signals.port_disconnected.connect(self._on_routing_connection_deleted)
        if hasattr(self.routing_graph, "port_connected"):
            self.routing_graph.port_connected.connect(self._on_routing_connection_created)
        if hasattr(self.routing_graph, "port_disconnected"):
            self.routing_graph.port_disconnected.connect(self._on_routing_connection_deleted)

    def _register_routing_ports(self, module_index, node, in_pos, out_pos):
        mod_id, cfg = self.selected_modules[int(module_index)]
        for idx, pos in enumerate(in_pos):
            try:
                port = node.input(idx)
            except Exception:
                continue
            block_type = self._block_type_for_module(mod_id, cfg, pos)
            self._routing_port_meta[id(port)] = {
                "module_index": int(module_index),
                "block_index": int(pos),
                "direction": "in",
                "block_type": block_type,
            }
        for idx, pos in enumerate(out_pos):
            try:
                port = node.output(idx)
            except Exception:
                continue
            block_type = self._block_type_for_module(mod_id, cfg, pos)
            self._routing_port_meta[id(port)] = {
                "module_index": int(module_index),
                "block_index": int(pos),
                "direction": "out",
                "block_type": block_type,
            }

    def _on_routing_connection_changed(self, *args):
        if not args:
            return
        connected = args[0]
        if not isinstance(connected, bool):
            return
        if connected:
            self._on_routing_connection_created(*args[1:])
        else:
            self._on_routing_connection_deleted(*args[1:])

    def _on_routing_connection_created(self, *args):
        if self._routing_is_building:
            return
        ports = self._extract_routing_ports(*args)
        if not ports:
            return
        source_meta, dest_meta = self._routing_source_dest_meta(*ports)
        if not source_meta or not dest_meta:
            self._routing_disconnect_ports(*ports)
            return
        if not self._is_valid_connection(
            source_meta["module_index"],
            source_meta["block_index"],
            dest_meta["module_index"],
            dest_meta["block_index"],
        ):
            self._routing_disconnect_ports(*ports)
            return
        if self._connection_exists(
            source_meta["module_index"],
            source_meta["block_index"],
            dest_meta["module_index"],
            dest_meta["block_index"],
        ):
            return
        self.connections.append(
            {
                "source": f"{int(source_meta['module_index'])}.{int(source_meta['block_index'])}",
                "destination": f"{int(dest_meta['module_index'])}.{int(dest_meta['block_index'])}",
                "strength": 100,
                "source_raw": int(source_meta["module_index"]),
                "source_block_raw": int(source_meta["block_index"]),
                "dest_raw": int(dest_meta["module_index"]),
                "dest_block_raw": int(dest_meta["block_index"]),
                "strength_raw": 100 * 100,
            }
        )
        self._refresh_current_details()

    def _on_routing_connection_deleted(self, *args):
        if self._routing_is_building:
            return
        ports = self._extract_routing_ports(*args)
        if not ports:
            return
        source_meta, dest_meta = self._routing_source_dest_meta(*ports)
        if not source_meta or not dest_meta:
            return
        self._remove_connection_by_meta(source_meta, dest_meta)
        self._refresh_current_details()

    def _extract_routing_ports(self, *args):
        if not args:
            return None
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            candidates = list(args[0])
        else:
            candidates = list(args)
        candidates = [c for c in candidates if not isinstance(c, bool)]
        ports = []
        for cand in candidates:
            port = self._normalize_routing_port(cand)
            if port is not None and id(port) in self._routing_port_meta:
                ports.append(port)
        if len(ports) >= 2:
            return ports[0], ports[1]
        for cand in candidates:
            ports = self._ports_from_edge(cand)
            if ports:
                return ports
        return None

    def _normalize_routing_port(self, port):
        if port is None:
            return None
        if id(port) in self._routing_port_meta:
            return port
        for attr in ("model", "port", "_port"):
            obj = getattr(port, attr, None)
            if obj is not None and id(obj) in self._routing_port_meta:
                return obj
        return port

    def _ports_from_edge(self, edge):
        if edge is None:
            return None
        candidates = []
        for attr in (
            "input_port",
            "output_port",
            "in_port",
            "out_port",
            "src_port",
            "dst_port",
            "source_port",
            "dest_port",
        ):
            val = getattr(edge, attr, None)
            if callable(val):
                try:
                    val = val()
                except Exception:
                    val = None
            if val is not None:
                val = self._normalize_routing_port(val)
                if id(val) in self._routing_port_meta:
                    candidates.append(val)
        if len(candidates) >= 2:
            return candidates[0], candidates[1]
        return None

    def _routing_source_dest_meta(self, port_a, port_b):
        meta_a = self._routing_port_meta.get(id(port_a))
        meta_b = self._routing_port_meta.get(id(port_b))
        if not meta_a or not meta_b:
            return None, None
        if meta_a["direction"] == "out" and meta_b["direction"] == "in":
            return meta_a, meta_b
        if meta_b["direction"] == "out" and meta_a["direction"] == "in":
            return meta_b, meta_a
        return None, None

    def _routing_disconnect_ports(self, port_a, port_b):
        graph = self.routing_graph
        if not graph:
            return
        for method in ("disconnect_ports", "disconnect_port", "disconnect"):
            if hasattr(graph, method):
                try:
                    getattr(graph, method)(port_a, port_b)
                    return
                except TypeError:
                    try:
                        getattr(graph, method)(port_a)
                        return
                    except Exception:
                        pass
                except Exception:
                    pass
        for method in ("disconnect_from", "disconnect"):
            if hasattr(port_a, method):
                try:
                    getattr(port_a, method)(port_b)
                    return
                except Exception:
                    pass
        for method in ("disconnect_from", "disconnect"):
            if hasattr(port_b, method):
                try:
                    getattr(port_b, method)(port_a)
                    return
                except Exception:
                    pass

    def _connection_exists(self, source_mod, source_block, dest_mod, dest_block):
        source_key = f"{int(source_mod)}.{int(source_block)}"
        dest_key = f"{int(dest_mod)}.{int(dest_block)}"
        for conn in self.connections:
            if conn.get("source") == source_key and conn.get("destination") == dest_key:
                return True
        return False

    def _remove_connection_by_meta(self, source_meta, dest_meta):
        source_key = f"{int(source_meta['module_index'])}.{int(source_meta['block_index'])}"
        dest_key = f"{int(dest_meta['module_index'])}.{int(dest_meta['block_index'])}"
        for idx, conn in enumerate(list(self.connections)):
            if conn.get("source") == source_key and conn.get("destination") == dest_key:
                self.connections.pop(idx)
                break

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

    @staticmethod
    def _split_versioned_patch_id(patch_id):
        if not patch_id:
            return patch_id, None
        if "_v" not in patch_id:
            return patch_id, None
        base_id, suffix = patch_id.rsplit("_v", 1)
        if not base_id or not suffix.isdigit():
            return patch_id, None
        return base_id, int(suffix)

    def _load_backend_metadata(self, patch_id, version=None):
        if not patch_id:
            return None, version
        back_path = self.patch_save.back_path
        if not back_path or not os.path.isdir(back_path):
            return None, version
        patch_dir = os.path.join(back_path, str(patch_id))
        if not os.path.isdir(patch_dir):
            return None, version
        if version is not None:
            json_path = os.path.join(
                patch_dir, "{}_v{}.json".format(patch_id, version)
            )
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r") as f:
                        return json.load(f), version
                except (OSError, json.JSONDecodeError):
                    return None, version
        json_path = os.path.join(patch_dir, "{}.json".format(patch_id))
        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as f:
                    return json.load(f), version
            except (OSError, json.JSONDecodeError):
                return None, version
        if version is None:
            latest = None
            for fname in os.listdir(patch_dir):
                if not (fname.startswith("{}_v".format(patch_id)) and fname.endswith(".json")):
                    continue
                suffix = fname.split("_v")[-1].split(".")[0]
                if not suffix.isdigit():
                    continue
                curr_version = int(suffix)
                if latest is None or curr_version > latest:
                    latest = curr_version
            if latest is not None:
                json_path = os.path.join(
                    patch_dir, "{}_v{}.json".format(patch_id, latest)
                )
                try:
                    with open(json_path, "r") as f:
                        return json.load(f), latest
                except (OSError, json.JSONDecodeError):
                    return None, version
        return None, version

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
