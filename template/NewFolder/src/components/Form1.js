import { useState } from "react";
import CreatableSelect from "react-select/creatable";
import Select from "react-select";
import Template from "./Template";
import ValidationBox from "./ValidationBox";
import Generated from "./Generated";
import SubmitList from "./SubmitList";
import Button from "./Button";
import Map from "./Map";
import { dateArray, amountArray, dateFormat, template1, template2 } from "./Options";

export default function Form() {
  // State for the form fields
  const [form, setForm] = useState({
    isCustom: false,
    columnName: "",
    headerName: "",
    defaultValue: "",
    amountFormat: "paisa",
    dateFormat: "",
    map: "",
  });

  // State for the list of added items
  const [items, setItems] = useState([]);
  // State for editing
  const [editingIndex, setEditingIndex] = useState(null);
  // State for template selection
  const [selectedTemplate, setSelectedTemplate] = useState("template1");
  // State for generated JSON
  const [generatedJSON, setGeneratedJSON] = useState("");
  // State for showing/hiding generated JSON
  const [showGenerated, setShowGenerated] = useState(false);
  // State for showing/hiding validation box
  const [showValidation, setShowValidation] = useState(false);
  // State for validation input and message
  const [validationInput, setValidationInput] = useState("");
  const [validationMessage, setValidationMessage] = useState("");
  // State for resetting Map fields
  const [mapResetCounter, setMapResetCounter] = useState(0);
  // State for editing Map fields
  const [editingMap, setEditingMap] = useState([]);

  // Get options for the selected template
  const templateOptions = selectedTemplate === "template2" ? template2 : template1;

  // Handle template change
  function handleTemplateChange(e) {
    const newTemplate = e.target.value;
    if (items.length > 0) {
      if (!window.confirm("Switching template will remove all fields. Continue?")) return;
      setItems([]);
      setEditingIndex(null);
      setForm({
        isCustom: false,
        columnName: "",
        headerName: "",
        defaultValue: "",
        amountFormat: "paisa",
        dateFormat: "",
        map: "",
      });
    }
    setSelectedTemplate(newTemplate);
  }

  // Handle form field changes
  function handleChange(e) {
    const { name, value } = e.target;
    if (name === "isCustom") {
      setForm((prev) => ({
        ...prev,
        isCustom: value === "true",
        defaultValue: value === "true" ? prev.defaultValue : "",
      }));
    } else {
      setForm((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  }

  // Handle column select change
  function handleColumnSelect(option) {
    if (form.isCustom ===false &&
      (amountArray.includes(form.columnName)) &&
        (form.columnName !== ""))
    {
      setForm({
        isCustom: false,
        columnName: "",
        headerName: "",
        defaultValue: "",
        dateFormat: "",
        map: "",
      });
    }
    else{
      setForm((prev) => ({
        ...prev,
        columnName: option.value,
      }));
    }
  }

  // Handle date format select change
  function handleDateFormatSelect(option) {
    setForm((prev) => ({
      ...prev,
      dateFormat: option ? option.value : "",
    }));
  }

  // Handle Map result (convert array to object, ensure Default is "_BLANK" if empty)
  let mapData = {};
  function handleMapResult(data) {
    const mapped = data.reduce((acc, curr) => {
      if (curr.key) acc[curr.key] = curr.value;
      return acc;
    }, {});
    if (!mapped.Default || mapped.Default.trim() === "") {
      mapped.Default = "_BLANK";
    }
    mapData = mapped;
  }

  // Handle form submit (add or update item)
  function handleSubmit(e) {
    e.preventDefault();

    // Simple validation
    if (!form.isCustom && !form.columnName.trim()) {
      alert("Please enter the column name");
      return;
    }

    // Prepare item to add/update
    const item = {
      ...form,
      map: mapData,
      orderId: editingIndex !== null ? items[editingIndex].orderId : items.length + 1,
      headerName: form.headerName || form.columnName.replaceAll("_", " "),
      amountFormat: form.amountFormat === "paisa" ? undefined : form.amountFormat,
      dateFormat: form.dateFormat || undefined,
      columnName: form.isCustom ? "" : form.columnName,
      defaultValue: form.isCustom ? form.defaultValue : "",
    };

    // Add or update item
    if (editingIndex !== null) {
      const updated = [...items];
      updated[editingIndex] = item;
      setItems(updated);
      setEditingIndex(null);
    } else {
      setItems([...items, item]);
    }

    // Reset form and Map
    setForm({
      isCustom: false,
      columnName: "",
      headerName: "",
      defaultValue: "",
      amountFormat: "paisa",
      dateFormat: "",
      map: "",
    });
    setMapResetCounter((c) => c + 1);
  }

  // Handle edit
  function handleEdit(index) {
    const item = items[index];
    // Prepare Map fields for editing
    let defaultValue = "";
    let rest = [];
    if (item.map) {
      Object.entries(item.map).forEach(([key, value]) => {
        if (key === "Default") {
          defaultValue = value;
        } else {
          rest.push({ key, value });
        }
      });
    }
    setForm({
      isCustom: item.defaultValue !== undefined && item.defaultValue !== "",
      columnName: item.columnName || "",
      headerName: item.headerName || "",
      defaultValue: item.defaultValue || "",
      amountFormat: item.amountFormat || "paisa",
      dateFormat: item.dateFormat || "",
      map: item.map || "",
    });
    setEditingMap([{ key: "Default", value: defaultValue }, ...rest]);
    setEditingIndex(index);
  }

  // Handle delete
  function handleDelete(index) {
    if (!window.confirm("Are you sure you want to delete this item?")) return;
    const updated = [...items];
    updated.splice(index, 1);
    setItems(updated);
    if (editingIndex === index) {
      setForm({
        isCustom: false,
        columnName: "",
        headerName: "",
        defaultValue: "",
        amountFormat: "paisa",
        dateFormat: "",
        map: "",
      });
      setEditingIndex(null);
    }
  }

  // Handle JSON generation
  function handleGenerate() {
    const sorted = [...items].sort((a, b) => a.orderId - b.orderId);
    setGeneratedJSON(JSON.stringify(sorted, null, 2));
    setShowGenerated(true);
  }

  // Handle validation
  function handleValidate() {
    try {
      const parsed = JSON.parse(validationInput);
      if (!Array.isArray(parsed)) throw new Error("Input must be a JSON array");
      setValidationMessage("Valid JSON!");
      // Optionally, you can add more validation here
    } catch (e) {
      setValidationMessage(e.message || "Invalid JSON!");
    }
  }

  // Render
  return (
    <form onSubmit={handleSubmit}>
      <div style={{ display: "flex", gap: "30px", alignItems: "flex-start" }}>
        <div style={{ flex: 1 }}>
          <br />
          <Template
            selectedTemplate={selectedTemplate}
            onTemplateChange={handleTemplateChange}
          />

          <div>
            Is Custom:
            <label>
              <input
                type="radio"
                name="isCustom"
                value="true"
                checked={form.isCustom === true}
                onChange={handleChange}
              />
              True
            </label>
            <label style={{ marginLeft: "10px" }}>
              <input
                type="radio"
                name="isCustom"
                value="false"
                checked={form.isCustom === false}
                onChange={handleChange}
              />
              False
            </label>
          </div>
          <br />

          <div>
            Column Name:
            <CreatableSelect
              options={templateOptions}
              placeholder="Select Column"
              onChange={handleColumnSelect}
              isSearchable
              isDisabled={form.isCustom}
              value={
                form.columnName
                  ? { label: form.columnName, value: form.columnName }
                  : null
              }
            />
          </div>
          <br />

          <div>
            Header Name:
            <input
              name="headerName"
              value={form.headerName}
              placeholder="Header Name"
              onChange={handleChange}
            />
          </div>
          <br />

          <div>
            Default Value:
            <input
              name="defaultValue"
              value={form.defaultValue}
              placeholder="Default Value"
              onChange={handleChange}
              disabled={!form.isCustom}
            />
          </div>
          <br />

          <div>
            Amount Format:
            <label>
              <input
                type="radio"
                name="amountFormat"
                value="paisa"
                checked={form.amountFormat === "paisa"}
                onChange={handleChange}
                disabled={
                  (form.isCustom ===false &&
                    (amountArray.includes(form.columnName)) &&
                      (form.columnName !== ""))
                }
              />
              Paisa
            </label>
            <label style={{ marginLeft: "10px" }}>
              <input
                type="radio"
                name="amountFormat"
                value="rs"
                checked={form.amountFormat === "rs"}
                onChange={handleChange}
                disabled={
                  (form.isCustom ===false &&
                    (amountArray.includes(form.columnName)) &&
                      (form.columnName !== ""))
                }
              />
              Rupee
            </label>
          </div>
          <br />

          <div>
            Date Format:
            <Select
              options={dateFormat}
              placeholder="Select Date"
              isSearchable
              isDisabled={
                form.isCustom ||
                (!dateArray.includes(form.columnName) &&
                  form.columnName !== "")
              }
              value={
                form.dateFormat
                  ? { label: form.dateFormat, value: form.dateFormat }
                  : null
              }
              onChange={handleDateFormatSelect}
            />
          </div>
          <br />

          <Map
            result={handleMapResult}
            reset={mapResetCounter}
            initialInput={editingMap}
          />

          <br />

          <Button type="submit">
            {editingIndex !== null ? "Update" : `Add (${items.length})`}
          </Button>

          {editingIndex !== null && (
            <Button
              type="button"
              style={{ marginLeft: "10px", backgroundColor: "#ccc" }}
              onClick={() => {
                setForm({
                  isCustom: false,
                  columnName: "",
                  headerName: "",
                  defaultValue: "",
                  amountFormat: "paisa",
                  dateFormat: "",
                  map: "",
                });
                setEditingIndex(null);
              }}
            >
              Cancel
            </Button>
          )}

          <Button
            type="button"
            style={{ backgroundColor: "blue", color: "white", marginLeft: "10px" }}
            onClick={handleGenerate}
          >
            Generate
          </Button>

          {showGenerated && (
            <Generated
              generatedJSON={generatedJSON}
              onCopy={async () => {
                try {
                  await navigator.clipboard.writeText(generatedJSON);
                  alert("Copied!");
                } catch {
                  alert("Failed to copy!");
                }
              }}
            />
          )}

          <Button
            type="button"
            onClick={() => setShowValidation((prev) => !prev)}
            style={{ marginTop: "20px", backgroundColor: "grey", color: "white" }}
          >
            {showValidation ? "Hide Validation Box" : "Show Validation Box"}
          </Button>
        </div>

        {showValidation && (
          <ValidationBox
            onValidate={handleValidate}
            onValidateChange={(e) => setValidationInput(e.target.value)}
            value={validationInput}
            message={validationMessage}
          />
        )}

        <div style={{ flex: 1 }}>
          <h3>Added Items:</h3>
          <SubmitList
            items={items}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        </div>
      </div>
    </form>
  );
}