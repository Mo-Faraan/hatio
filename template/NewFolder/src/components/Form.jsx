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

    // State for template selection
    const [selectedTemplate, setSelectedTemplate] = useState("template1");



    // State for the list of added items
    const [items, setItems] = useState([]);
    // State for editing
    const [editingIndex, setEditingIndex] = useState(null);
    
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

    function handleSubmit(){
        console.log("jsdch");
    }

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

    function handleColumnSelect(option) {
        setForm((prev) => ({
          ...prev,
          columnName: option.value,
        }));
    }

    function handleDateFormatSelect(option) {
      setForm((prev) => ({
        ...prev,
        dateFormat: option ? option.value : "",
      }));
    }

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
            </div>
        </div>

        <br></br>

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
                  form.isCustom ===false &&
                  (amountArray.includes(form.columnName)) &&
                    (form.columnName !== "")
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
                  form.isCustom ===false &&
                  (amountArray.includes(form.columnName)) &&
                    (form.columnName !== "")
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
                form.isCustom===false &&
                (dateArray.includes(form.columnName)) &&
                  (form.columnName !== "")
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



    </form>
    );
}